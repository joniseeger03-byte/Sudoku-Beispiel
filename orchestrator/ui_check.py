"""Spielt das Sudoku wirklich: Headless-Browser, Klicks auf die sichtbare Stelle, Tastendrücke, bis zum Sieg.

Aufruf: python ui_check.py <ordner mit index.html und engine.py>
Exit-Code: 0 bestanden, 1 nicht bestanden, 3 kein Browser gefunden.

Bedienvertrag aus prompts/spezifikation.md:
- Jedes Feld hat data-index="0" bis "80", seine Ziffer steht als Text darin.
- Ziffernfeld-Buttons haben data-digit="1" bis "9", der Löschen-Button hat data-digit="0".
- Buttons mit data-stufe="leicht", "mittel", "schwer" starten sofort ein neues Rätsel.
- Das ausgewählte Feld ist dauerhaft sichtbar hervorgehoben (Klasse, nicht :focus).
- Felder im Konflikt tragen die Klasse "konflikt".
- Ist das Rätsel richtig gelöst, trägt body die Klasse "geloest".

Das Aussehen ist frei. Geprüft wird nur, was ein Mensch beim Spielen braucht.
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

WARTEN = 90
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8"}

# Läuft im Browser, nach dem Laden der Seite. Meldet das Ergebnis an /__bericht.
PRUEFUNG = r"""
<script>
(() => {
  const fehler = [];
  window.addEventListener('error', e => fehler.push(String(e.message)));
  const pause = ms => new Promise(r => setTimeout(r, ms));
  const feld = i => document.querySelector(`[data-index="${i}"]`);
  const knopf = d => document.querySelector(`[data-digit="${d}"]`);
  const stufe = s => document.querySelector(`[data-stufe="${s}"]`);
  const text = i => (feld(i).textContent || '').trim();
  const taste = key => document.dispatchEvent(new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true }));
  const zeile = i => Math.floor(i / 9);
  const alle = [...Array(81).keys()];
  const belegt = () => alle.filter(i => text(i));
  const stil = i => {
    const s = getComputedStyle(feld(i));
    return [s.backgroundColor, s.backgroundImage, s.color, s.outlineStyle, s.outlineColor, s.outlineWidth,
            s.boxShadow, s.borderTopColor, s.borderTopWidth, s.transform].join('|');
  };
  const treffer = el => {
    el.scrollIntoView({ block: 'center', inline: 'center', behavior: 'instant' });
    const r = el.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2, r };
  };
  // Wie ein Mensch: Das Ereignis trifft, was an dieser Stelle wirklich oben liegt.
  const klick = el => {
    if (!el) return;
    const { x, y } = treffer(el);
    const ziel = document.elementFromPoint(x, y) || el;
    const o = { bubbles: true, cancelable: true, clientX: x, clientY: y, view: window, button: 0 };
    [[PointerEvent, 'pointerdown'], [MouseEvent, 'mousedown'], [PointerEvent, 'pointerup'], [MouseEvent, 'mouseup'], [MouseEvent, 'click']]
      .forEach(([K, n]) => ziel.dispatchEvent(new K(n, o)));
  };
  const treffbar = el => {
    if (!el) return false;
    const { x, y, r } = treffer(el);
    const oben = document.elementFromPoint(x, y);
    return r.width >= 20 && r.height >= 20 && !!oben && (oben === el || el.contains(oben));
  };
  const wahl = async i => { klick(feld(i)); await pause(50); };

  async function pruefe() {
    const out = [], ok = (name, wert, info = '') => out.push({ name, ok: !!wert, info });
    for (let i = 0; i < 100 && document.querySelectorAll('[data-index]').length < 81; i++) await pause(100);
    for (let i = 0; i < 100 && !(feld(0) && belegt().length); i++) await pause(100);
    const anzahl = document.querySelectorAll('[data-index]').length;
    ok('81 Felder mit data-index', anzahl === 81, `${anzahl} gefunden`);
    if (anzahl !== 81) return out;
    const vorgaben = belegt(), leer = alle.filter(i => !text(i));
    ok('Rätsel wird angezeigt', vorgaben.length >= 17 && leer.length > 0, `${vorgaben.length} Vorgaben`);
    if (!vorgaben.length || leer.length < 6) return out;

    // Darstellung: echtes 9×9-Raster, jedes Bedienelement erreichbar, Blöcke erkennbar
    const box = alle.map(i => feld(i).getBoundingClientRect());
    const links = new Set(box.map(r => Math.round(r.left))), oben = new Set(box.map(r => Math.round(r.top)));
    ok('Felder bilden ein 9×9-Raster', links.size === 9 && oben.size === 9, `${links.size} Spalten, ${oben.size} Zeilen`);
    const nichtTreffbar = alle.filter(i => !treffbar(feld(i)));
    ok('Jedes Feld ist anklickbar', !nichtTreffbar.length, `verdeckt oder zu klein: ${nichtTreffbar.slice(0, 8).join(', ')}`);
    const fehltKnopf = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].filter(d => !treffbar(knopf(d)));
    ok('Ziffernfeld und Löschen-Button erreichbar', !fehltKnopf.length, `data-digit fehlt oder verdeckt: ${fehltKnopf.join(', ')}`);
    const fehltStufe = ['leicht', 'mittel', 'schwer'].filter(s => !treffbar(stufe(s)));
    ok('Stufenwahl erreichbar', !fehltStufe.length, `data-stufe fehlt oder verdeckt: ${fehltStufe.join(', ')}`);
    const breite = (i, seite) => parseFloat(getComputedStyle(feld(i))[`border${seite}Width`]) || 0;
    const rahmen = i => feld(i).getBoundingClientRect();
    const spalte = (a, b) => rahmen(b).left - rahmen(a).right + breite(a, 'Right') + breite(b, 'Left');
    const reihe = (a, b) => rahmen(b).top - rahmen(a).bottom + breite(a, 'Bottom') + breite(b, 'Top');
    ok('3×3-Blöcke sind erkennbar', spalte(2, 3) > spalte(0, 1) && reihe(18, 27) > reihe(0, 9),
       `Linien/Abstände: innen ${spalte(0, 1)}/${reihe(0, 9)}, Blockgrenze ${spalte(2, 3)}/${reihe(18, 27)}`);

    // Auswahl: bleibt sichtbar stehen und wandert mit
    const x = leer[3], y = leer[4];
    await wahl(y); await pause(400);
    const yGewaehlt = stil(y), xVorher = stil(x);
    await wahl(x); await pause(400);
    ok('Ausgewähltes Feld bleibt sichtbar markiert', stil(x) !== xVorher, `Feld ${x} sieht nach dem Klick unverändert aus`);
    ok('Markierung wandert zum neuen Feld', stil(y) !== yGewaehlt, `Feld ${y} bleibt markiert`);

    // Setzen und Löschen auf jedem Weg
    const frei = i => [1, 2, 3, 4, 5, 6, 7, 8, 9].find(d => !alle.some(j => zeile(j) === zeile(i) && text(j) === String(d)));
    const a = leer[0], da = frei(a);
    await wahl(a); klick(knopf(da)); await pause(60);
    ok('Ziffer per Klick setzen', text(a) === String(da), `Feld ${a} zeigt "${text(a)}", erwartet ${da}`);
    klick(knopf(0)); await pause(60);
    ok('Ziffer per Löschen-Button löschen', text(a) === '', `Feld ${a} zeigt "${text(a)}"`);

    const b = leer.find(i => zeile(i) !== zeile(a)) ?? leer[1], db = frei(b);
    await wahl(b); taste(String(db)); await pause(60);
    ok('Ziffer per Tastatur setzen', text(b) === String(db), `Feld ${b} zeigt "${text(b)}", erwartet ${db}`);
    taste('Delete'); await pause(60);
    ok('Ziffer per Entf löschen', text(b) === '', `Feld ${b} zeigt "${text(b)}"`);
    taste(String(db)); await pause(60); taste('Backspace'); await pause(60);
    ok('Ziffer per Rücktaste löschen', text(b) === '', `Feld ${b} zeigt "${text(b)}"`);

    // Pfeiltasten: die nächste Eingabe landet im Nachbarfeld
    const p = leer.find(i => i % 9 < 8 && !text(i + 1));
    if (p !== undefined) {
      await wahl(p); taste('ArrowRight'); await pause(60); taste('5'); await pause(60);
      ok('Pfeiltasten bewegen die Auswahl', text(p + 1) === '5' && text(p) === '', `Feld ${p + 1} zeigt "${text(p + 1)}"`);
      taste('Delete'); await pause(60);
    }

    const v = vorgaben[0], wert = text(v), anders = wert === '1' ? '2' : '1';
    await wahl(v); taste(anders); await pause(60); taste('Delete'); await pause(60); klick(knopf(anders)); await pause(60);
    ok('Vorgaben sind geschützt', text(v) === wert, `Feld ${v} zeigt "${text(v)}", erwartet ${wert}`);

    // Konflikt: Wert einer Vorgabe in ein leeres Feld derselben Zeile, und wieder weg
    const c = leer.find(i => vorgaben.some(j => zeile(j) === zeile(i)));
    if (c === undefined) { ok('Konflikt wird markiert', false, 'kein passendes Feld gefunden'); return out; }
    const gleich = text(vorgaben.find(j => zeile(j) === zeile(c)));
    await wahl(c); taste(gleich); await pause(100);
    ok('Konflikt wird markiert', feld(c).classList.contains('konflikt'), `Feld ${c} mit ${gleich}, Klassen: "${feld(c).className}"`);
    taste('Delete'); await pause(100);
    ok('Konflikt verschwindet nach dem Löschen', !document.querySelector('.konflikt'), 'Klasse konflikt ist noch gesetzt');

    // Stufenwahl: Klick startet sofort ein Rätsel mit der richtigen Hinweiszahl
    for (const [s, n] of [['schwer', 26], ['mittel', 32], ['leicht', 38]]) {
      klick(stufe(s));
      for (let i = 0; i < 150 && belegt().length !== n; i++) await pause(100);
      ok(`Stufe ${s} startet ein neues Rätsel`, belegt().length === n, `${belegt().length} Ziffern, erwartet ${n}`);
    }
    await pause(150);

    // Komplett durchspielen bis zum Sieg, mit der Lösung, die die Engine geliefert hat
    const spiel = await (await fetch('/__letztes')).json();
    ok('Angezeigtes Rätsel stammt aus der Engine', alle.every(i => text(i) === (spiel.puzzle[i] ? String(spiel.puzzle[i]) : '')));
    const offen = alle.filter(i => !spiel.puzzle[i]);
    for (const i of offen.slice(0, -1)) { await wahl(i); taste(String(spiel.solution[i])); await pause(10); }
    ok('Vor der letzten Ziffer noch nicht gelöst', !document.body.classList.contains('geloest'));
    const letzte = offen[offen.length - 1];
    await wahl(letzte); taste(String(spiel.solution[letzte])); await pause(200);
    ok('Rätsel lässt sich vollständig ausfüllen', alle.every(i => text(i) === String(spiel.solution[i])));
    ok('Gelöstes Rätsel ohne Konflikte', !document.querySelector('.konflikt'));
    ok('Sieg wird erkannt', document.body.classList.contains('geloest'), 'body trägt nicht die Klasse geloest');
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
    letztes = [b"{}"]

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
            if name == "__letztes":
                return self.send(letztes[0], "application/json")
            if name == "api/neu":
                stufe = parse_qs(url.query).get("stufe", ["mittel"])[0]
                r = subprocess.run([sys.executable, "engine.py", "neu", stufe], cwd=ordner, capture_output=True, timeout=60)
                if r.returncode == 0:
                    letztes[0] = r.stdout
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
        p = subprocess.Popen([browser(), "--headless=new", "--disable-gpu", "--no-first-run", "--window-size=1280,900",
                              f"--user-data-dir={profil}", f"http://127.0.0.1:{server.server_address[1]}/index.html"],
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
