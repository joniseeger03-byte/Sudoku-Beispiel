"""Lokales Dashboard: liest den Ordner runs/ und zeigt ihn im Browser.
Auf Knopfdruck startet es orchestrator/run.py als eigenen Prozess (Demo oder echter Lauf) und kann ihn abbrechen."""
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import graph

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
PAGE = Path(__file__).resolve().parent / "dashboard.html"
RUN_PY = Path(__file__).resolve().parent / "run.py"
PORT = 8000
RUN_ID = re.compile(r"^[0-9-]+$")
FILE_NAME = re.compile(r"^[\w.-]+$")
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8"}


class Prozess:
    """Der eine Orchestrator-Lauf, den das Dashboard gestartet hat. Ausgabe landet in runs/_prozess.log."""

    def __init__(self):
        self.lock = threading.Lock()
        self.p = None
        self.modus = None
        self.start = 0.0
        self.abgebrochen = False

    @property
    def log(self):
        return RUNS / "_prozess.log"

    def laeuft(self):
        return self.p is not None and self.p.poll() is None

    def starte(self, modus):
        with self.lock:
            if self.laeuft():
                return False
            RUNS.mkdir(exist_ok=True)
            befehl = [sys.executable, "-u", str(RUN_PY)] + (["--demo"] if modus == "demo" else [])
            extra = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True})
            with open(self.log, "w", encoding="utf-8") as out:
                self.p = subprocess.Popen(befehl, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                          env={**os.environ, "PYTHONUTF8": "1"}, **extra)
            self.modus, self.start, self.abgebrochen = modus, time.time(), False
            return True

    def stoppe(self):
        with self.lock:
            if not self.laeuft():
                return False
            # Ganzen Prozessbaum beenden: run.py startet selbst Claude Code, git und Tests.
            if os.name == "nt":
                subprocess.run(["taskkill", "/T", "/F", "/PID", str(self.p.pid)], capture_output=True)
            else:
                os.killpg(self.p.pid, signal.SIGTERM)
            self.p.wait(timeout=15)
            self.abgebrochen = True
            # Sonst stünde der Lauf im Dashboard ewig auf „läuft“.
            laeufe = [d for d in RUNS.iterdir() if d.is_dir() and RUN_ID.match(d.name) and d.stat().st_mtime >= self.start - 1]
            if laeufe:
                e = {"zeit": time.strftime("%H:%M:%S"), "t": round(time.time(), 2), "knoten": "orchestrator", "status": "info",
                     "text": "Im Dashboard abgebrochen"}
                with open(max(laeufe) / "events.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
            return True

    def zustand(self):
        code = None if self.p is None else self.p.poll()
        zeilen = [z for z in (self.log.read_text(encoding="utf-8", errors="replace") if self.p and self.log.exists() else "").splitlines() if z.strip()]
        return {"laeuft": self.laeuft(), "modus": self.modus, "code": code, "abgebrochen": self.abgebrochen,
                "letzte": zeilen[-1] if zeilen else ""}


PROZESS = Prozess()


def offener_echter_lauf():
    """Ein echter Lauf, der noch auf Freigabe oder Verwerfen wartet. Solange er offen ist, startet kein neuer echter Lauf."""
    if not RUNS.exists():
        return None
    for d in sorted((p for p in RUNS.iterdir() if p.is_dir() and RUN_ID.match(p.name)), reverse=True):
        zeilen = [z for z in lies(d / "events.jsonl").splitlines() if z.strip()]
        try:
            letzt, modus = json.loads(zeilen[-1]) if zeilen else {}, json.loads(lies(d / "start.json", "{}")).get("modus")
        except json.JSONDecodeError:
            continue
        if modus == "live" and letzt.get("knoten") == "freigabe" and letzt.get("status") == "run":
            return d.name
    return None


def lies(p, fallback=""):
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else fallback


def lauf(d):
    log = d / "events.jsonl"
    events = [json.loads(x) for x in lies(log).splitlines() if x.strip()]
    aufrufe = {}
    for p in sorted((d / "aufrufe").glob("*.json")):
        try:
            rec = json.loads(lies(p))
        except json.JSONDecodeError:
            continue  # wird gerade geschrieben
        # Für die Übersicht ohne die großen Texte; die holt sich die Seite bei Bedarf einzeln.
        rec["kontext"] = [{"name": c["name"], "quelle": c["quelle"], "zeichen": len(c["text"])} for c in rec.get("kontext", [])]
        rec["prompt_zeichen"] = len(rec.pop("prompt", ""))
        rec.pop("anfrage", None)
        aufrufe[rec["id"]] = rec
    live = {p.stem: lies(p)[-30000:] for p in sorted((d / "live").glob("*.txt"))}
    start = json.loads(lies(d / "start.json", "{}"))
    dateien = {p.name: lies(p) for p in sorted(d.glob("*.md"))}
    return {"start": start, "events": events, "aufrufe": aufrufe, "live": live, "dateien": dateien,
            "ergebnis": (d / "ergebnis" / "index.html").exists()}


class Handler(BaseHTTPRequestHandler):
    def send(self, body, ctype="application/json; charset=utf-8", code=200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def json(self, data):
        self.send(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        parts = self.path.split("?")[0].strip("/").split("/")
        if parts == [""]:
            return self.send(PAGE.read_bytes(), "text/html; charset=utf-8")
        if parts == ["api", "graph"]:
            g = graph.als_json()
            g["prompts"] = {k["prompt"]: lies(ROOT / "prompts" / k["prompt"]) for k in graph.KNOTEN.values() if "prompt" in k}
            return self.json(g)
        if parts == ["api", "runs"]:
            ids = sorted((p.name for p in RUNS.iterdir() if p.is_dir() and RUN_ID.match(p.name)), reverse=True) if RUNS.exists() else []
            return self.json(ids)
        if len(parts) == 3 and parts[:2] == ["api", "run"] and RUN_ID.match(parts[2]) and (RUNS / parts[2]).is_dir():
            return self.json(lauf(RUNS / parts[2]))
        if len(parts) == 4 and parts[:2] == ["api", "aufruf"] and RUN_ID.match(parts[2]) and FILE_NAME.match(parts[3]):
            f = RUNS / parts[2] / "aufrufe" / f"{parts[3]}.json"
            if f.is_file():
                return self.send(f.read_bytes())
        if len(parts) == 3 and parts[0] == "ergebnis" and RUN_ID.match(parts[1]) and FILE_NAME.match(parts[2]):
            f = RUNS / parts[1] / "ergebnis" / parts[2]
            if f.is_file():
                return self.send(f.read_bytes(), TYPES.get(f.suffix, "application/octet-stream"))
        if len(parts) == 4 and parts[0] == "ergebnis" and RUN_ID.match(parts[1]) and parts[2:] == ["api", "neu"]:
            stufe = parse_qs(urlparse(self.path).query).get("stufe", ["mittel"])[0]
            d = RUNS / parts[1] / "ergebnis"
            if stufe in ("leicht", "mittel", "schwer") and (d / "engine.py").exists():
                r = subprocess.run([sys.executable, "engine.py", "neu", stufe], cwd=d, env={**os.environ, "PYTHONUTF8": "1"},
                                   capture_output=True, encoding="utf-8", errors="replace", timeout=60)
                if r.returncode == 0:
                    return self.send(r.stdout.encode("utf-8"))
        if parts == ["api", "prozess"]:
            return self.json({**PROZESS.zustand(), "offen_live": offener_echter_lauf()})
        self.send(b"Nicht gefunden", "text/plain; charset=utf-8", 404)

    def do_POST(self):
        # Nur die eigene Seite darf Läufe starten: Ohne diese Prüfung könnte jede Webseite im Browser
        # per Formular an localhost einen echten (kostenpflichtigen) Lauf auslösen. Der eigene Header
        # erzwingt bei fremden Seiten eine CORS-Vorabfrage, die hier nie beantwortet wird.
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0]
        if self.headers.get("X-Dashboard") != "1" or host not in ("localhost", "127.0.0.1"):
            return self.send(b"Verboten", "text/plain; charset=utf-8", 403)
        parts = self.path.split("?")[0].strip("/").split("/")
        if parts == ["api", "start"]:
            laenge = min(int(self.headers.get("Content-Length") or 0), 1000)
            modus = json.loads(self.rfile.read(laenge) or b"{}").get("modus")
            if modus not in ("demo", "live"):
                return self.send(b"modus: demo oder live", "text/plain; charset=utf-8", 400)
            offen = offener_echter_lauf() if modus == "live" else None
            if offen:
                return self.send(f"Der echte Lauf {offen} wartet noch auf Freigabe oder Verwerfen.".encode("utf-8"), "text/plain; charset=utf-8", 409)
            if not PROZESS.starte(modus):
                return self.send("Es läuft schon ein Lauf.".encode("utf-8"), "text/plain; charset=utf-8", 409)
            return self.json(PROZESS.zustand())
        if parts == ["api", "stopp"]:
            PROZESS.stoppe()
            return self.json(PROZESS.zustand())
        if parts in (["api", "freigabe"], ["api", "verwerfen"]):
            laenge = min(int(self.headers.get("Content-Length") or 0), 1000)
            lauf_id = json.loads(self.rfile.read(laenge) or b"{}").get("lauf", "")
            if not RUN_ID.match(lauf_id or ""):
                return self.send(b"lauf fehlt", "text/plain; charset=utf-8", 400)
            if PROZESS.laeuft():
                return self.send("Erst den laufenden Lauf abwarten".encode("utf-8"), "text/plain; charset=utf-8", 409)
            # Genau wie die Tasks „4 Lauf freigeben“ und „4b Lauf verwerfen“, nur für den Lauf, der im Dashboard zu sehen ist.
            r = subprocess.run([sys.executable, str(RUN_PY), f"--{parts[1]}", lauf_id], cwd=ROOT, capture_output=True,
                               encoding="utf-8", errors="replace", env={**os.environ, "PYTHONUTF8": "1"}, timeout=120)
            return self.json({"ok": r.returncode == 0, "ausgabe": (r.stdout + r.stderr).strip()})
        self.send(b"Nicht gefunden", "text/plain; charset=utf-8", 404)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"Dashboard: http://localhost:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
