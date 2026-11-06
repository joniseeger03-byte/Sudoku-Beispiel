"""Lokales Dashboard: liest den Ordner runs/ und zeigt ihn im Browser. Startet selbst keine Agenten."""
import json
import os
import re
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import graph

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
PAGE = Path(__file__).resolve().parent / "dashboard.html"
PORT = 8000
RUN_ID = re.compile(r"^[0-9-]+$")
FILE_NAME = re.compile(r"^[\w.-]+$")
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8"}


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
        self.send(b"Nicht gefunden", "text/plain; charset=utf-8", 404)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"Dashboard: http://localhost:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
