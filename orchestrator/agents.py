"""Ruft Modelle über OpenAI-kompatible Schnittstellen auf und streamt die Antwort an `live`."""
import json
import os
import re
import time
import urllib.error
import urllib.request

# Bei diesen HTTP-Codes darf auf einen anderen Anbieter ausgewichen werden.
# 403 kommt z. B. von Cloudflare-Sperren (Fehler 1010), 429 von Ratenlimits.
AUSWEICHEN_BEI = {403, 429, 500, 502, 503, 504}
MAX_WARTEN = 30  # Sekunden: so lange warten wir bei einem Ratenlimit, bevor wir ausweichen


class ApiFehler(RuntimeError):
    def __init__(self, anbieter, code, detail, warten=None):
        super().__init__(f"{anbieter}: HTTP {code}: {detail}" if code else f"{anbieter}: {detail}")
        self.code, self.warten = code, warten


def nothing(*_):
    pass


def anfrage(cfg, anbieter, nachricht):
    """Beschreibt die HTTP-Anfrage, ohne sie zu senden. Das Dashboard zeigt sie an."""
    a = cfg["anbieter"][anbieter]
    body = {"model": a["modell"], "stream": True, **a.get("parameter", {}),
            "messages": [{"role": "user", "content": nachricht}]}
    return {"url": a["url"].rstrip("/") + "/chat/completions", "key": a["key"], "body": body}


def api_call(cfg, anbieter, nachricht, live=nothing, wechsel=None, ausweichen=True, melde=nothing):
    """Fragt `anbieter`. Bei kurzem Ratenlimit wird gewartet, bei Sperren oder Überlast der nächste
    Anbieter versucht (`wechsel`). `melde` bekommt Hinweise wie "Antwort abgeschnitten"."""
    reihenfolge = [anbieter] + ([n for n in cfg["anbieter"] if n != anbieter] if ausweichen else [])
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
        with urllib.request.urlopen(req, timeout=300) as r:
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
