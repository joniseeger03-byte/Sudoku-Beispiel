"""Ruft Modelle über OpenAI-kompatible Schnittstellen auf und streamt die Antwort an `live`."""
import json
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.request

# Bei diesen HTTP-Codes darf auf einen anderen Anbieter ausgewichen werden.
# 403 kommt z. B. von Cloudflare-Sperren (Fehler 1010), 429 von Ratenlimits.
AUSWEICHEN_BEI = {403, 429, 500, 502, 503, 504}
MAX_WARTEN = 30  # Sekunden: so lange warten wir bei einem Ratenlimit, bevor wir ausweichen

# Claude Code als Agent: darf im Arbeitsordner lesen, schreiben und Python ausführen, sonst nichts.
WERKZEUGE = ["Read", "Edit", "Write", "Glob", "Grep", "Bash(python:*)", "PowerShell(python:*)"]
AGENT_ZEITLIMIT = 600
API_ZEITLIMIT = 120  # Sekunden ohne neue Daten, danach wird ausgewichen


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
    if werkzeuge:
        befehl += ["--permission-mode", "acceptEdits", "--allowedTools", ",".join(WERKZEUGE)]
    return befehl


def anfrage(cfg, anbieter, nachricht, werkzeuge=False):
    """Beschreibt die Anfrage, ohne sie zu senden. Das Dashboard zeigt sie an."""
    a = cfg["anbieter"][anbieter]
    if ist_claude(cfg, anbieter):
        return {"befehl": claude_befehl(a, werkzeuge), "werkzeuge": WERKZEUGE if werkzeuge else [], "modell": a["modell"]}
    body = {"model": a["modell"], "stream": True, **a.get("parameter", {}),
            "messages": [{"role": "user", "content": nachricht}]}
    return {"url": a["url"].rstrip("/") + "/chat/completions", "key": a["key"], "body": body}


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
