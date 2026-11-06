"""Bedient die Oberfläche wirklich: Headless-Browser, Klicks und Tastendrücke nach dem Bedienvertrag.

Aufruf: python ui_check.py <ordner mit index.html und engine.py>
Exit-Code: 0 bestanden, 1 nicht bestanden, 3 kein Browser gefunden.

Bedienvertrag aus prompts/spezifikation.md:
- Jedes Feld hat data-index="0" bis "80", seine Ziffer steht als Text darin.
- Ziffernfeld-Buttons haben data-digit="1" bis "9".
- Felder im Konflikt tragen die Klasse "konflikt".
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

WARTEN = 30
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8"}

# Läuft im Browser, nach dem Laden der Seite. Meldet das Ergebnis an /__bericht.
PRUEFUNG = r"""
<script>
(() => {
  const fehler = [];
  window.addEventListener('error', e => fehler.push(String(e.message)));
  const pause = ms => new Promise(r => setTimeout(r, ms));
  const feld = i => document.querySelector(`[data-index="${i}"]`);
  const text = i => (feld(i).textContent || '').trim();
  const taste = key => document.dispatchEvent(new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true }));
  const zeile = i => Math.floor(i / 9);
  async function pruefe() {
    const out = [], ok = (name, wert, info = '') => out.push({ name, ok: !!wert, info });
    for (let i = 0; i < 100 && document.querySelectorAll('[data-index]').length < 81; i++) await pause(100);
    for (let i = 0; i < 100 && !(feld(0) && [...Array(81).keys()].some(n => text(n))); i++) await pause(100);
    const anzahl = document.querySelectorAll('[data-index]').length;
    ok('81 Felder mit data-index', anzahl === 81, `${anzahl} gefunden`);
    if (anzahl !== 81) return out;
    const alle = [...Array(81).keys()], vorgaben = alle.filter(i => text(i)), leer = alle.filter(i => !text(i));
    ok('Rätsel wird angezeigt', vorgaben.length >= 17 && leer.length > 0, `${vorgaben.length} Vorgaben`);
    if (!vorgaben.length || leer.length < 3) return out;

    // Konfliktfrei setzen: eine Ziffer, die in der Zeile noch nicht vorkommt
    const frei = i => [1, 2, 3, 4, 5, 6, 7, 8, 9].find(d => !alle.some(j => zeile(j) === zeile(i) && text(j) === String(d)));
    const a = leer[0], da = frei(a);
    feld(a).click(); await pause(60);
    const knopf = document.querySelector(`[data-digit="${da}"]`);
    ok('Ziffernfeld vorhanden', knopf);
    if (knopf) { knopf.click(); await pause(60); }
    ok('Ziffer per Klick setzen', text(a) === String(da), `Feld ${a} zeigt "${text(a)}", erwartet ${da}`);

    const b = leer.find(i => zeile(i) !== zeile(a)) ?? leer[1], db = frei(b);
    feld(b).click(); await pause(60); taste(String(db)); await pause(60);
    ok('Ziffer per Tastatur setzen', text(b) === String(db), `Feld ${b} zeigt "${text(b)}", erwartet ${db}`);

    taste('Delete'); await pause(60);
    ok('Ziffer löschen', text(b) === '', `Feld ${b} zeigt "${text(b)}"`);

    const v = vorgaben[0], wert = text(v), anders = wert === '1' ? '2' : '1';
    feld(v).click(); await pause(60); taste(anders); await pause(60);
    ok('Vorgaben sind geschützt', text(v) === wert, `Feld ${v} zeigt "${text(v)}", erwartet ${wert}`);

    // Konflikt erzwingen: Wert einer Vorgabe in ein leeres Feld derselben Zeile
    const c = leer.find(i => i !== a && i !== b && vorgaben.some(j => zeile(j) === zeile(i)));
    if (c === undefined) { ok('Konflikt wird markiert', false, 'kein passendes Feld gefunden'); return out; }
    const gleich = text(vorgaben.find(j => zeile(j) === zeile(c)));
    feld(c).click(); await pause(60); taste(gleich); await pause(100);
    ok('Konflikt wird markiert', feld(c).classList.contains('konflikt'), `Feld ${c} mit ${gleich}, Klassen: "${feld(c).className}"`);
    return out;
  }
  window.addEventListener('load', async () => {
    let out = [];
    try { out = await pruefe(); } catch (e) { fehler.push(String(e)); }
    fehler.forEach(f => out.push({ name: 'Kein JavaScript-Fehler', ok: false, info: f }));
    await fetch('/__bericht', { method: 'POST', body: JSON.stringify(out) });
  });
})();
</script>
"""


def browser():
    for name in ("msedge", "chrome", "google-chrome", "chromium", "chromium-browser"):
        if shutil.which(name):
            return shutil.which(name)
    for basis in (os.environ.get("PROGRAMFILES(X86)"), os.environ.get("PROGRAMFILES"), os.environ.get("LOCALAPPDATA")):
        for teil in (r"Microsoft\Edge\Application\msedge.exe", r"Google\Chrome\Application\chrome.exe"):
            if basis and (Path(basis) / teil).exists():
                return str(Path(basis) / teil)
    for pfad in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                 "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"):
        if Path(pfad).exists():
            return pfad
    return None


def pruefe(ordner):
    fertig, bericht = threading.Event(), []

    class Handler(BaseHTTPRequestHandler):
        def send(self, body, ctype, code=200):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            bericht.extend(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
            self.send(b"{}", "application/json")
            fertig.set()

        def do_GET(self):
            url = urlparse(self.path)
            name = url.path.strip("/") or "index.html"
            if name == "api/neu":
                stufe = parse_qs(url.query).get("stufe", ["mittel"])[0]
                r = subprocess.run([sys.executable, "engine.py", "neu", stufe], cwd=ordner, capture_output=True, timeout=60)
                return self.send(r.stdout, "application/json", 200 if r.returncode == 0 else 500)
            datei = ordner / name
            if "/" in name or not datei.is_file():
                return self.send(b"", "text/plain", 404)
            body = datei.read_bytes()
            if name == "index.html":
                html = body.decode("utf-8", "replace")
                body = (html.replace("</body>", PRUEFUNG + "</body>") if "</body>" in html else html + PRUEFUNG).encode("utf-8")
            self.send(body, TYPES.get(datei.suffix, "application/octet-stream"))

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profil:
        p = subprocess.Popen([browser(), "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={profil}",
                              f"http://127.0.0.1:{server.server_address[1]}/index.html"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            fertig.wait(WARTEN)
        finally:
            p.kill()
            p.wait()
            server.shutdown()
    return bericht if fertig.is_set() else [{"name": "Seite meldet Ergebnis", "ok": False, "info": f"keine Antwort nach {WARTEN} s"}]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ordner = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not browser():
        print("Kein Browser gefunden (Edge oder Chrome). Oberfläche nicht geprüft.")
        sys.exit(3)
    bericht = pruefe(ordner)
    for c in bericht:
        print(f"{'OK    ' if c['ok'] else 'FEHLER'} {c['name']}{'' if c['ok'] else ': ' + c['info']}")
    sys.exit(0 if bericht and all(c["ok"] for c in bericht) else 1)


if __name__ == "__main__":
    main()
