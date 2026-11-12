"""Ruft Modelle über OpenAI-kompatible Schnittstellen auf und streamt die Antwort an `live`."""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

# Bei diesen HTTP-Codes darf auf einen anderen Anbieter ausgewichen werden.
# 403 kommt z. B. von Cloudflare-Sperren (Fehler 1010), 429 von Ratenlimits.
AUSWEICHEN_BEI = {403, 429, 500, 502, 503, 504}
MAX_WARTEN = 30  # Sekunden: so lange warten wir bei einem Ratenlimit, bevor wir ausweichen

# Claude Code als Agent: darf im Arbeitsordner lesen, schreiben und Python ausführen, sonst nichts.
WERKZEUGE = ["Read", "Edit", "Write", "Glob", "Grep", "Bash(python:*)", "PowerShell(python:*)"]
AGENT_ZEITLIMIT = 900
API_ZEITLIMIT = 120  # Sekunden ohne neue Daten, danach wird ausgewichen

# Agent über eine normale API: Das Modell ruft Werkzeuge auf, die Harness führt sie aus und gibt das Ergebnis zurück.
# Ein Agent ist nur diese Schleife: Modell → Werkzeugaufruf → Ergebnis → Modell, bis es ohne Werkzeug antwortet.
# Er sieht nur den Projektordner des Laufs und kann nur die zwei Prüfungen ausführen, sonst nichts.
AGENT_SCHRITTE = 30
UI_CHECK = Path(__file__).with_name("ui_check.py")
DATEINAME = re.compile(r"^[\w.-]+$")


def _fn(werkzeug_name, beschreibung, **felder):
    return {"type": "function", "function": {"name": werkzeug_name, "description": beschreibung, "parameters": {
        "type": "object", "properties": {k: {"type": "string", "description": v} for k, v in felder.items()},
        "required": list(felder)}}}


HARNESS_WERKZEUGE = [
    _fn("dateien", "Listet die Dateien im Projektordner."),
    _fn("lesen", "Liest eine Datei aus dem Projektordner.", name="Dateiname ohne Pfad, z. B. engine.py"),
    _fn("ersetzen", "Ersetzt eine Textstelle, die genau einmal in der Datei vorkommt. Für kleine Änderungen.",
        name="Dateiname ohne Pfad", alt="exakter bisheriger Text", neu="neuer Text"),
    _fn("schreiben", "Ersetzt den kompletten Inhalt einer Datei.", name="Dateiname ohne Pfad", inhalt="ganzer neuer Inhalt"),
    _fn("pruefen", "Führt eine Prüfung im Projektordner aus. tests: python test_spiel.py. "
        "oberflaeche: bedient index.html im Headless-Browser (python ui_check.py).", was="tests oder oberflaeche"),
]
AGENT_SYSTEM = ("Du arbeitest mit Werkzeugen im Projektordner. Lies und ändere Dateien mit den Werkzeugen, statt Code nur "
                "zu zeigen. Befehle wie python test_spiel.py führst du mit dem Werkzeug pruefen aus. Wenn du fertig bist, "
                "antworte ohne Werkzeugaufruf mit deinem Bericht.")


class ApiFehler(RuntimeError):
    def __init__(self, anbieter, code, detail, warten=None):
        super().__init__(f"{anbieter}: HTTP {code}: {detail}" if code else f"{anbieter}: {detail}")
        self.code, self.warten = code, warten


def nothing(*_):
    pass


def ist_claude(cfg, anbieter):
    return cfg["anbieter"][anbieter].get("typ") == "claude-code"


def claude_befehl(a, werkzeuge):
    befehl = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--no-session-persistence",
              "--model", a["modell"], "--strict-mcp-config", "--setting-sources", "project"]
    if werkzeuge is True:
        befehl += ["--permission-mode", "acceptEdits", "--allowedTools", ",".join(WERKZEUGE)]
    elif werkzeuge:  # eigene Liste, z. B. nur Websuche: ohne acceptEdits, also keine Dateiänderungen
        befehl += ["--allowedTools", ",".join(werkzeuge)]
    return befehl


def anfrage(cfg, anbieter, nachricht, werkzeuge=False):
    """Beschreibt die Anfrage, ohne sie zu senden. Das Dashboard zeigt sie an."""
    a = cfg["anbieter"][anbieter]
    if ist_claude(cfg, anbieter):
        return {"befehl": claude_befehl(a, werkzeuge), "werkzeuge": WERKZEUGE if werkzeuge is True else (werkzeuge or []), "modell": a["modell"]}
    if werkzeuge is True:   # Agent über die API, die Werkzeuge stellt die Harness
        body = {"model": a["modell"], **a.get("parameter", {}), "tools": HARNESS_WERKZEUGE,
                "messages": [{"role": "system", "content": AGENT_SYSTEM}, {"role": "user", "content": nachricht}]}
        return {"url": a["url"].rstrip("/") + "/chat/completions", "key": a["key"], "body": body,
                "werkzeuge": [w["function"]["name"] for w in HARNESS_WERKZEUGE]}
    body = {"model": a["modell"], "stream": True, **a.get("parameter", {}),
            "messages": [{"role": "user", "content": nachricht}]}
    return {"url": a["url"].rstrip("/") + "/chat/completions", "key": a["key"], "body": body, "werkzeuge": []}


def api_call(cfg, anbieter, nachricht, live=nothing, wechsel=None, ausweichen=True, melde=nothing):
    """Fragt `anbieter`. Bei kurzem Ratenlimit wird gewartet, bei Sperren oder Überlast der nächste
    Anbieter versucht (`wechsel`). `melde` bekommt Hinweise wie "Antwort abgeschnitten"."""
    reihenfolge = [anbieter] + ([n for n in cfg["anbieter"] if n != anbieter and not ist_claude(cfg, n)] if ausweichen else [])
    letzter, vorher = None, None
    for name in reihenfolge:
        key = os.environ.get(cfg["anbieter"][name]["key"], "").strip()
        if not key:
            letzter = ApiFehler(name, None, f"{cfg['anbieter'][name]['key']} fehlt in der .env")
            if not ausweichen:
                raise letzter
            vorher = name
            continue
        if vorher and wechsel:
            wechsel(vorher, name, str(letzter))
        vorher = name
        for versuch in (1, 2):
            try:
                return _einzeln(cfg, name, nachricht, live, key, melde)
            except ApiFehler as e:
                if e.code not in AUSWEICHEN_BEI:
                    raise
                letzter = e
                if e.code == 429 and versuch == 1 and e.warten is not None and e.warten <= MAX_WARTEN:
                    melde(f"Ratenlimit bei {name}: warte {e.warten:.0f} s und versuche es erneut")
                    time.sleep(e.warten + 1)
                    continue
                break
    raise letzter or ApiFehler(anbieter, None, "kein Anbieter konfiguriert")


def _kurz(werkzeug, eingabe):
    wert = next((eingabe[k] for k in ("command", "file_path", "pattern") if k in eingabe), "")
    return f"\n▶ {werkzeug}: {str(wert)[:140]}\n\n"


def claude_call(cfg, anbieter, nachricht, live=nothing, cwd=None, werkzeuge=False):
    """Startet Claude Code im Ordner `cwd`, die Nachricht geht über stdin. Gibt (text, kosten_usd) zurück."""
    programm = shutil.which("claude")
    if not programm:
        raise ApiFehler(anbieter, None, "Claude Code wurde nicht gefunden (Befehl claude)")
    befehl = [programm] + claude_befehl(cfg["anbieter"][anbieter], werkzeuge)[1:]
    p = subprocess.Popen(befehl, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, encoding="utf-8", errors="replace")
    fehler = []
    threading.Thread(target=lambda: fehler.append(p.stderr.read()), daemon=True).start()
    wachhund = threading.Timer(AGENT_ZEITLIMIT, p.kill)
    wachhund.start()
    ergebnis = None
    try:
        p.stdin.write(nachricht)
        p.stdin.close()
        for zeile in p.stdout:
            try:
                e = json.loads(zeile)
            except json.JSONDecodeError:
                continue
            if e.get("type") == "assistant":
                for b in e["message"]["content"]:
                    if b.get("type") == "text":
                        live(b["text"] + "\n")
                    elif b.get("type") == "tool_use":
                        live(_kurz(b["name"], b.get("input") or {}))
            elif e.get("type") == "result":
                ergebnis = e
        p.wait()
    finally:
        wachhund.cancel()
    if not ergebnis or ergebnis.get("is_error"):
        detail = (ergebnis or {}).get("result") or "".join(fehler)[:300] or f"Exit-Code {p.returncode}"
        raise ApiFehler(anbieter, None, f"Claude Code: {detail}")
    return ergebnis.get("result") or "", ergebnis.get("total_cost_usd")


def werkzeug(ordner, name, args):
    """Führt einen Werkzeugaufruf des Modells aus. Gibt immer Text zurück, auch bei Fehlern: Das Modell soll sie lesen."""
    ordner = Path(ordner)
    if not isinstance(args, dict):
        return "Fehler: Die Argumente sind kein gültiges JSON-Objekt."
    if name == "dateien":
        return "\n".join(sorted(f.name for f in ordner.iterdir() if f.is_file()))
    if name == "pruefen":
        befehl = {"tests": [sys.executable, "-u", "test_spiel.py"], "oberflaeche": [sys.executable, str(UI_CHECK), "."]}.get(args.get("was"))
        if not befehl:
            return "Fehler: was muss tests oder oberflaeche sein."
        try:
            r = subprocess.run(befehl, cwd=ordner, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=120, env={**os.environ, "PYTHONUTF8": "1"})
            return f"Exit-Code {r.returncode}\n{((r.stdout or '') + (r.stderr or '')).strip()[-4000:]}"
        except subprocess.TimeoutExpired:
            return "Abgebrochen nach 120 Sekunden. Vermutlich ist etwas zu langsam oder hängt."
        finally:
            shutil.rmtree(ordner / "__pycache__", ignore_errors=True)
    datei = str(args.get("name", ""))
    if not DATEINAME.match(datei):
        return "Fehler: Erlaubt sind nur Dateinamen im Projektordner, ohne Pfad."
    f = ordner / datei
    try:
        if name == "lesen":
            return f.read_text(encoding="utf-8", errors="replace") if f.is_file() else f"Fehler: {datei} gibt es nicht."
        if name == "schreiben":
            f.write_text(str(args.get("inhalt", "")), encoding="utf-8")
            return f"{datei} geschrieben."
        if name == "ersetzen":
            if not f.is_file():
                return f"Fehler: {datei} gibt es nicht."
            text, alt = f.read_text(encoding="utf-8"), str(args.get("alt", ""))
            n = text.count(alt) if alt else 0
            if n != 1:
                return f"Fehler: Die Stelle kommt {n}-mal vor. Sie muss genau einmal vorkommen, nimm mehr Kontext dazu."
            f.write_text(text.replace(alt, str(args.get("neu", ""))), encoding="utf-8")
            return f"{datei} geändert."
    except OSError as e:
        return f"Fehler: {e}"
    return f"Fehler: Das Werkzeug {name} gibt es nicht."


def agent_call(cfg, anbieter, nachricht, live=nothing, cwd=None, melde=nothing):
    """Agent über eine OpenAI-kompatible API mit Function Calling. Gibt den Schlussbericht zurück."""
    a = cfg["anbieter"][anbieter]
    key = os.environ.get(a["key"], "").strip()
    if not key:
        raise ApiFehler(anbieter, None, f"{a['key']} fehlt in der .env")
    nachrichten = anfrage(cfg, anbieter, nachricht, werkzeuge=True)["body"]["messages"]
    ende = time.time() + AGENT_ZEITLIMIT
    for schritt in range(1, AGENT_SCHRITTE + 1):
        if time.time() > ende:
            raise ApiFehler(anbieter, None, f"Agent nach {AGENT_ZEITLIMIT} s nicht fertig")
        try:
            msg = _schritt(cfg, anbieter, key, nachrichten, melde)
        except ApiFehler as e:
            # Kaputter Werkzeugaufruf (z. B. ungültiges JSON): Die Harness sagt es dem Modell, statt abzubrechen.
            if e.code == 400 and "tool" in str(e).lower() and schritt < AGENT_SCHRITTE:
                melde("Ungültiger Werkzeugaufruf, das Modell bekommt den Fehler zurück")
                nachrichten.append({"role": "user", "content": f"Dein letzter Werkzeugaufruf war ungültig: {str(e)[:300]}. Versuche es erneut."})
                continue
            raise
        text = (msg.get("content") or "").strip()
        if text:
            live(text + "\n")
        aufrufe = msg.get("tool_calls") or []
        if not aufrufe:
            if not text:
                raise ApiFehler(anbieter, None, "leere Antwort")
            return text
        nachrichten.append({"role": "assistant", "content": text or None, "tool_calls": aufrufe})
        for c in aufrufe:
            name = c["function"]["name"]
            try:
                args = json.loads(c["function"].get("arguments") or "{}")
            except json.JSONDecodeError:
                args = None
            live(_kurz(name, {"command": (args or {}).get("was") or (args or {}).get("name", "")}))
            nachrichten.append({"role": "tool", "tool_call_id": c["id"], "content": werkzeug(cwd, name, args)})
    raise ApiFehler(anbieter, None, f"Agent nach {AGENT_SCHRITTE} Schritten nicht fertig")


def _schritt(cfg, anbieter, key, nachrichten, melde):
    """Ein Modell-Aufruf der Agenten-Schleife, ohne Streaming."""
    a = cfg["anbieter"][anbieter]
    body = {"model": a["modell"], **a.get("parameter", {}), "messages": nachrichten, "tools": HARNESS_WERKZEUGE}
    req = urllib.request.Request(a["url"].rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "sudoku-agenten/1.0"})
    for versuch in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=API_ZEITLIMIT) as r:
                choice = json.load(r)["choices"][0]
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:400]
            warten = _wartezeit(e, detail)
            if e.code == 429 and versuch < 3 and warten is not None and warten <= MAX_WARTEN:
                melde(f"Ratenlimit bei {anbieter}: warte {warten:.0f} s und versuche es erneut")
                time.sleep(warten + 1)
                continue
            raise ApiFehler(anbieter, e.code, detail, warten) from e
        except (urllib.error.URLError, TimeoutError) as e:
            raise ApiFehler(anbieter, 503, f"keine Verbindung: {e}") from e
        if choice.get("finish_reason") == "length":
            melde("Antwort abgeschnitten: Ausgabelimit des Modells erreicht (finish_reason=length)")
        return choice["message"]
    raise ApiFehler(anbieter, 429, "Ratenlimit")


def _wartezeit(e, detail):
    try:
        return float(e.headers.get("retry-after"))
    except (TypeError, ValueError, AttributeError):
        m = re.search(r"try again in (?:(\d+)m)?([\d.]+)s", detail)
        return (int(m.group(1) or 0) * 60 + float(m.group(2))) if m else None


def _einzeln(cfg, anbieter, nachricht, live, key, melde):
    a = anfrage(cfg, anbieter, nachricht)
    req = urllib.request.Request(
        a["url"],
        data=json.dumps(a["body"]).encode("utf-8"),
        # Eigener User-Agent: Cloudflare (z. B. bei Groq) sperrt "Python-urllib/…" mit Fehler 1010.
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "sudoku-agenten/1.0"},
    )
    parts, ende = [], None
    try:
        with urllib.request.urlopen(req, timeout=API_ZEITLIMIT) as r:
            if "text/event-stream" not in r.headers.get("Content-Type", ""):
                choice = json.load(r)["choices"][0]
                text, ende = choice["message"]["content"], choice.get("finish_reason")
                live(text)
                parts.append(text)
            else:
                for raw in r:
                    line = raw.decode("utf-8", "replace").strip()
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    choices = json.loads(data).get("choices") or []
                    if not choices:
                        continue
                    ende = choices[0].get("finish_reason") or ende
                    chunk = (choices[0].get("delta") or {}).get("content")
                    if chunk:
                        parts.append(chunk)
                        live(chunk)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        raise ApiFehler(anbieter, e.code, detail, _wartezeit(e, detail)) from e
    except (urllib.error.URLError, TimeoutError) as e:
        raise ApiFehler(anbieter, 503, f"keine Verbindung: {e}") from e
    if not parts:
        raise ApiFehler(anbieter, None, "leere Antwort")
    if ende == "length":
        melde("Antwort abgeschnitten: Ausgabelimit des Modells erreicht (finish_reason=length)")
    return "".join(parts)
