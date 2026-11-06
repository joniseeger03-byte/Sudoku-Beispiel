"""Orchestrator: normaler Code, der den Graphen aus graph.py abläuft.

Er startet die Modell-Aufrufe (Prompt + Kontext), übernimmt ihre Antworten in Dateien,
führt Tests aus und entscheidet anhand der Urteile, welche Kante als Nächstes dran ist.
Alles, was er tut, landet in runs/<lauf>/ und ist im Dashboard sichtbar.
"""
import argparse
import ast
import json
import os
import random
import re
import shutil
import stat
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import agents
from graph import KNOTEN

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
WORK = ROOT / "arbeitsbereich"
TARGET = WORK / "projekt"
DEMO = Path(__file__).resolve().parent / "demo"
GIT = ["git", "-c", "user.name=Agentenlauf", "-c", "user.email=agent@localhost"]

# Demo: Diese Code-Dateien spielt das "Modell" als Antwort zurück, jeweils als Codeblock.
DEMO_CODE = {
    "engine": ["engine_fehlerhaft.py"],
    "korrektur": ["engine.py"],
    "ui": ["index.html", "board.js", "style.css"],
    "tests": ["test_spiel.py"],
}
SPRACHE = {".py": "python", ".html": "html", ".js": "javascript", ".css": "css"}


# ---------------------------------------------------------------- Hilfen

def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def load_cfg():
    return json.loads((ROOT / "config.json").read_text(encoding="utf-8"))


def git(*args, cwd=TARGET, check=True):
    r = subprocess.run(GIT + list(args), cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        detail = (r.stderr or "").strip() or (r.stdout or "").strip() or "git command failed"
        raise RuntimeError(f"git {' '.join(args)}: {detail}")
    return r


def codebloecke(text):
    """Alle ```-Blöcke einer Antwort als Liste von (sprache, code).

    Zäune zählen nur am Zeilenanfang (```python im Fließtext ist kein Block).
    Ein nicht geschlossener letzter Block (abgeschnittene Antwort) zählt bis zum Ende.
    """
    muster = r"^[ \t]*```([\w.+-]*)[ \t]*\r?\n(.*?)(?:^[ \t]*```[ \t]*$|\Z)"
    return [(lang.lower(), code.strip()) for lang, code in re.findall(muster, text, re.S | re.M)]


def urteil(text, erlaubt):
    m = re.search(r"URTEIL:\s*\**\s*(" + "|".join(erlaubt) + r")\b", text, re.I)
    return m.group(1).lower() if m else None


# ---------------------------------------------------------------- Ein Lauf

class Lauf:
    def __init__(self, lauf_id, demo):
        self.id, self.demo = lauf_id, demo
        self.dir = RUNS / lauf_id
        self.wt = WORK / "worktrees" / lauf_id
        self.lock = threading.Lock()
        self.zaehler = 0

    # --- Protokoll ----------------------------------------------------
    def event(self, knoten, status, text, **extra):
        """status: run, ok, fail (Zustand eines Knotens), harness (Code ohne Modell), kante, info."""
        e = {"zeit": datetime.now().strftime("%H:%M:%S"), "t": round(time.time(), 2), "knoten": knoten, "status": status, "text": text}
        e.update({k: v for k, v in extra.items() if v is not None})
        with self.lock:
            with open(self.dir / "events.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        zeichen = {"harness": "   harness |", "kante": "   kante   |"}.get(status, "")
        print(f"[{e['zeit']}]{zeichen} {knoten}: {text}", flush=True)

    def harness(self, knoten, text, befehl=None, warnung=None):
        """warnung=True: Die Harness hat eingegriffen, z. B. ein Urteil verworfen oder den Anbieter gewechselt."""
        self.event(knoten, "harness", text, befehl=befehl, warnung=warnung)

    def kante(self, von, nach, text):
        self.event(von, "kante", f"{von} → {nach}: {text}", von=von, nach=nach)

    def schreibe(self, name, text):
        (self.dir / name).write_text(text, encoding="utf-8")

    def live(self, aufruf_id):
        d = self.dir / "live"
        d.mkdir(exist_ok=True)

        def write(chunk):
            with open(d / f"{aufruf_id}.txt", "a", encoding="utf-8") as f:
                f.write(chunk)
        return write

    # --- Kontext ------------------------------------------------------
    def kontext(self, knoten, runde, suche):
        """Löst die Kontext-Liste aus graph.py auf: erst runs/<lauf>/, dann die Worktrees in `suche`."""
        out = []
        for eintrag in KNOTEN[knoten].get("kontext", []):
            optional = eintrag.endswith("?")
            name = eintrag.rstrip("?").format(runde=runde)
            datei = next((d / name for d in [self.dir, *suche] if (d / name).is_file()), None)
            if datei is None:
                if optional:
                    continue
                raise RuntimeError(f"{knoten}: Kontext-Datei {name} fehlt")
            out.append({"name": name, "quelle": str(datei.relative_to(ROOT)).replace("\\", "/"),
                        "text": datei.read_text(encoding="utf-8", errors="replace")})
        return out

    # --- Ein Modell-Aufruf ------------------------------------------
    def frage(self, cfg, knoten, runde=1, suche=(), nachtrag=None):
        """Baut die Nachricht aus prompts/<prompt> + Kontext, ruft das Modell und protokolliert alles.
        `nachtrag`: Hinweis der Harness, z. B. der Syntaxfehler der vorigen Antwort."""
        k = KNOTEN[knoten]
        prompt_datei = f"prompts/{k['prompt']}"
        prompt_text = (ROOT / prompt_datei).read_text(encoding="utf-8", errors="replace").strip()
        kontext = self.kontext(knoten, runde, suche)
        if nachtrag:
            kontext.append({"name": "Hinweis der Harness", "quelle": "orchestrator/run.py", "text": nachtrag})
        nachricht = prompt_text + "".join(f"\n\n--- {c['name']} ---\n{c['text']}" for c in kontext)

        anbieter = cfg["rollen"][knoten]
        modell = cfg["anbieter"][anbieter]["modell"]
        with self.lock:
            self.zaehler += 1
            aid = f"{self.zaehler:02d}-{knoten}"
        rec = {
            "id": aid, "knoten": knoten, "runde": runde, "status": "run", "start": time.time(),
            "anbieter": anbieter, "modell": modell, "simuliert": self.demo,
            "prompt_datei": prompt_datei, "prompt": prompt_text, "kontext": kontext,
            "anfrage": agents.anfrage(cfg, anbieter, nachricht),
        }
        self._speichere(rec)
        self.event(knoten, "run", f"Modell-Aufruf, Runde {runde}" if runde > 1 else "Modell-Aufruf",
                   aufruf=aid, runde=runde, anbieter=anbieter, modell=modell)
        out = self.live(aid)
        try:
            if self.demo:
                text = demo_antwort(knoten, runde, out)
            else:
                def wechsel(von, nach, grund):
                    self.harness(knoten, f"Anbieter gewechselt: {von} → {nach} ({grund.strip()[:120]})", warnung=True)
                    rec["anbieter"], rec["modell"] = nach, cfg["anbieter"][nach]["modell"]
                text = agents.api_call(cfg, anbieter, nachricht, out, wechsel,
                                       melde=lambda t: self.harness(knoten, t, warnung=True))
        except Exception as e:
            rec.update(status="fail", dauer=round(time.time() - rec["start"], 1), fehler=str(e))
            self._speichere(rec)
            self.event(knoten, "fail", f"Modell-Aufruf fehlgeschlagen: {e}", aufruf=aid)
            raise
        rec.update(status="ok", dauer=round(time.time() - rec["start"], 1), antwort_zeichen=len(text))
        self._speichere(rec)
        return text, aid

    def _speichere(self, rec):
        d = self.dir / "aufrufe"
        d.mkdir(exist_ok=True)
        (d / f"{rec['id']}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")

    # --- Antwort in Dateien übernehmen (Harness) ----------------------
    def uebernimm(self, knoten, text, ziel, dateien, pflicht):
        """Sucht für jede Datei den passenden Codeblock (nach Sprache, sonst nach Reihenfolge) und schreibt ihn.
        Gibt die gefundenen Probleme zurück (fehlende Pflichtdateien, Syntaxfehler)."""
        probleme = []
        bloecke = codebloecke(text)
        if not bloecke and len(dateien) == 1:
            bloecke = [("", text.strip())]
        frei = list(bloecke)
        for name in dateien:
            sprache = SPRACHE[Path(name).suffix]
            treffer = next((b for b in frei if b[0] in (sprache, Path(name).suffix[1:])), None)
            treffer = treffer or next((b for b in frei if not b[0]), None)
            if treffer is None:
                if name in pflicht:
                    probleme.append(f"Kein Codeblock für {name} in der Antwort.")
                    self.harness(knoten, f"{name}: kein Codeblock in der Antwort", warnung=True)
                else:
                    self.harness(knoten, f"{name}: kein Codeblock in der Antwort, übersprungen")
                continue
            frei.remove(treffer)
            (ziel / name).write_text(treffer[1] + "\n", encoding="utf-8")
            self.harness(knoten, f"Codeblock übernommen → {name} ({len(treffer[1])} Zeichen)")
            if name.endswith(".py"):
                try:
                    ast.parse(treffer[1])
                    self.harness(knoten, f"Syntaxprüfung {name}: ok", befehl="ast.parse")
                except SyntaxError as e:
                    probleme.append(f"{name} hat einen Syntaxfehler in Zeile {e.lineno}: {e.msg}")
                    self.harness(knoten, f"Syntaxprüfung {name}: Fehler in Zeile {e.lineno}: {e.msg}", befehl="ast.parse", warnung=True)
        return probleme

    def commit(self, knoten, pfad, msg):
        git("add", "-A", cwd=pfad)
        if git("status", "--porcelain", cwd=pfad).stdout.strip():
            git("commit", "-m", msg, cwd=pfad)
            self.harness(knoten, f"Commit „{msg}“", befehl=f'git commit -m "{msg}"')


def demo_antwort(knoten, runde, out):
    """Demo: vorbereitete Antwort statt Modell. Alles danach läuft genauso wie echt."""
    datei = next((DEMO / "texte" / n for n in (f"{knoten}-r{runde}.md", f"{knoten}.md") if (DEMO / "texte" / n).exists()), None)
    if datei:
        text = datei.read_text(encoding="utf-8")
    else:
        text = "\n\n".join(f"```{SPRACHE[Path(f).suffix]}\n{(DEMO / 'code' / f).read_text(encoding='utf-8').strip()}\n```"
                           for f in DEMO_CODE[knoten])
    time.sleep(1.2)  # "denkt nach"
    i = 0
    while i < len(text):
        n = random.randint(6, 16)
        out(text[i:i + n])
        i += n
        time.sleep(0.035)
    return text


# ---------------------------------------------------------------- Bausteine

def init_target():
    TARGET.mkdir(parents=True, exist_ok=True)
    if not (TARGET / ".git").exists():
        git("init", "-b", "main")
        (TARGET / "README.md").write_text("# Sudoku\n", encoding="utf-8")
        (TARGET / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
        git("add", "-A")
        git("commit", "-m", "Start")


def worktree(lauf, name):
    pfad = lauf.wt / name
    git("worktree", "add", str(pfad), "-b", f"agent/{lauf.id}/{name}", "main")
    return pfad


def textknoten(lauf, cfg, knoten, runde=1):
    """Ein Modell-Aufruf, dessen Antwort als Markdown-Datei gespeichert wird."""
    text, aid = lauf.frage(cfg, knoten, runde)
    datei = KNOTEN[knoten]["ausgabe"][0].format(runde=runde)
    lauf.schreibe(datei, text)
    lauf.event(knoten, "ok", f"{datei} geschrieben", datei=datei, aufruf=aid)
    return text


def codeknoten(lauf, cfg, knoten, pfad, runde=1, suche=(), pflicht=None):
    """Ein Modell-Aufruf, dessen Codeblöcke in einen Worktree geschrieben und committet werden.
    Ist die Antwort unbrauchbar, fragt die Harness genau einmal mit dem Fehler als Hinweis nach."""
    dateien = KNOTEN[knoten]["ausgabe"]
    text, aid = lauf.frage(cfg, knoten, runde, suche)
    probleme = lauf.uebernimm(knoten, text, pfad, dateien, pflicht or dateien)
    if probleme:
        lauf.harness(knoten, "Antwort unbrauchbar, frage einmal mit Hinweis nach", warnung=True)
        hinweis = ("Deine vorige Antwort war nicht verwendbar:\n- " + "\n- ".join(probleme) +
                   "\nAntworte erneut vollständig und nur im verlangten Format. Halte den Code knapp.")
        text, aid = lauf.frage(cfg, knoten, runde, suche, nachtrag=hinweis)
        probleme = lauf.uebernimm(knoten, text, pfad, dateien, pflicht or dateien)
        missing = [p for p in probleme if p.startswith("Kein Codeblock")]
        if missing:
            raise RuntimeError(f"{knoten}: {missing[0]}")
    lauf.commit(knoten, pfad, f"{KNOTEN[knoten]['titel']}, Runde {runde}")
    lauf.event(knoten, "ok", "Dateien übernommen", aufruf=aid)


def gate(lauf, integ, runde, zeitlimit):
    """Test-Gate: kein Modell. Branches zusammenführen und python test_spiel.py ausführen."""
    lauf.event("gate", "run", f"Test-Gate, Runde {runde}", runde=runde)
    git("reset", "--hard", "main", cwd=integ)
    for n in ("engine", "ui", "tests"):
        r = git("merge", "--no-ff", "-m", f"Merge {n}", f"agent/{lauf.id}/{n}", cwd=integ, check=False)
        if r.returncode != 0:
            raise RuntimeError(f"Merge-Konflikt bei {n}: {r.stdout[:300]}")
        lauf.harness("gate", f"Branch {n} zusammengeführt", befehl=f"git merge --no-ff agent/{lauf.id}/{n}")
    lauf.harness("gate", f"Tests starten, Zeitlimit {zeitlimit} s", befehl="python -u test_spiel.py")
    start = time.time()
    try:
        # -u: ungepuffert, damit bei Zeitüberschreitung die Ausgabe bis dahin erhalten bleibt
        r = subprocess.run([sys.executable, "-u", "test_spiel.py"], cwd=integ, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=zeitlimit)
        code, out = r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()
    except subprocess.TimeoutExpired as e:
        teil = e.stdout.decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        code = "Zeitlimit"
        out = (f"{teil.strip()}\n\nABGEBROCHEN: Die Tests liefen länger als {zeitlimit} Sekunden.\n"
               "Die Spezifikation verlangt ein Rätsel in unter 5 Sekunden. Häufigste Ursache: generate() oder "
               "solutions() sind zu langsam.").strip()
        lauf.harness("gate", f"Zeitlimit von {zeitlimit} s überschritten, Tests abgebrochen", warnung=True)
    lauf.harness("gate", f"Laufzeit {time.time() - start:.1f} s")
    ok = code == 0
    lauf.harness("gate", f"Exit-Code {code}: {'bestanden' if ok else 'nicht bestanden'}", befehl="python test_spiel.py")
    name = KNOTEN["gate"]["ausgabe"][0].format(runde=runde)
    lauf.schreibe(name, f"# Test-Gate, Runde {runde}: {'bestanden' if ok else 'nicht bestanden'}\n\n"
                        f"**Prüfer:** `python test_spiel.py`, kein Sprachmodell. **Exit-Code:** {code}\n\n```text\n{out[-4000:]}\n```\n")
    lauf.event("gate", "ok" if ok else "fail", f"Runde {runde} {'bestanden' if ok else 'nicht bestanden'}", datei=name, runde=runde)
    return ok


# ---------------------------------------------------------------- Der Ablauf

def start(demo):
    load_env()
    cfg = load_cfg()
    if not shutil.which("git"):
        sys.exit("git wurde nicht gefunden. Bitte installieren.")
    lauf = Lauf(datetime.now().strftime("%Y-%m-%d-%H%M%S"), demo)
    lauf.dir.mkdir(parents=True)
    lauf.wt.mkdir(parents=True)
    befehl = "python orchestrator/run.py" + (" --demo" if demo else "")
    (lauf.dir / "start.json").write_text(json.dumps({
        "befehl": befehl, "modus": "demo" if demo else "live", "zeit": datetime.now().isoformat(timespec="seconds"),
        "max_runden": cfg["max_runden"],
        "rollen": {k: {"anbieter": a, "modell": cfg["anbieter"][a]["modell"]} for k, a in cfg["rollen"].items()},
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"$ {befehl}\nLauf {lauf.id}\n", flush=True)
    try:
        ablauf(lauf, cfg)
    except Exception as e:
        lauf.event("orchestrator", "info", f"Abgebrochen: {e}")
        sys.exit(1)


def ablauf(lauf, cfg):
    max_runden = cfg["max_runden"]
    init_target()

    # Auftrag
    lauf.schreibe("00-auftrag.md", (ROOT / "auftrag.md").read_text(encoding="utf-8"))
    lauf.event("auftrag", "ok", "Auftrag abgelegt", datei="00-auftrag.md")

    # Schleife 1: Recherche (parallel) → Prüfung, bis URTEIL: ok
    for runde in range(1, max_runden + 1):
        with ThreadPoolExecutor(2) as ex:
            jobs = [ex.submit(textknoten, lauf, cfg, k, runde) for k in ("recherche_a", "recherche_b")]
            [j.result() for j in jobs]
        text = textknoten(lauf, cfg, "pruefung", runde)
        u = urteil(text, ["ok", "nacharbeiten"])
        lauf.harness("pruefung", f"Urteil gelesen: {u or 'keins gefunden'}", befehl="re.search('URTEIL: …')", warnung=None if u else True)
        if u == "ok":
            lauf.kante("pruefung", "spezifikation", "URTEIL: ok")
            break
        if runde == max_runden:
            raise RuntimeError(f"Prüfung nach {max_runden} Runden nicht bestanden")
        for k in ("recherche_a", "recherche_b"):
            lauf.kante("pruefung", k, f"nacharbeiten, Runde {runde + 1}")

    # Spezifikation
    textknoten(lauf, cfg, "spezifikation")

    # Umsetzung: drei Agenten parallel, jeder in seinem eigenen Git-Worktree
    paths = {}
    for n in ("engine", "ui", "tests", "integration"):
        paths[n] = worktree(lauf, n)
        lauf.harness(n if n != "integration" else "gate", f"Worktree {n} angelegt",
                     befehl=f"git worktree add {paths[n].relative_to(ROOT).as_posix()} -b agent/{lauf.id}/{n}")
    integ = paths["integration"]
    with ThreadPoolExecutor(3) as ex:
        jobs = [ex.submit(codeknoten, lauf, cfg, "engine", paths["engine"]),
                ex.submit(codeknoten, lauf, cfg, "ui", paths["ui"], pflicht=["index.html", "board.js"]),
                ex.submit(codeknoten, lauf, cfg, "tests", paths["tests"])]
        [j.result() for j in jobs]

    # Schleife 2: Test-Gate → Testcheck → Korrektur, bis die Tests bestehen
    test_korrigiert = False
    for runde in range(1, max_runden + 1):
        if gate(lauf, integ, runde, cfg.get("test_zeitlimit", 90)):
            lauf.kante("gate", "integration", "bestanden")
            break
        if runde == max_runden:
            raise RuntimeError(f"Tests nach {max_runden} Runden nicht bestanden")
        lauf.kante("gate", "testcheck", "nicht bestanden")

        text, aid = lauf.frage(cfg, "testcheck", runde, suche=[integ])
        datei = KNOTEN["testcheck"]["ausgabe"][0].format(runde=runde)
        lauf.schreibe(datei, text)
        u = urteil(text, ["engine", "test"]) or "engine"
        lauf.harness("testcheck", f"Urteil gelesen: {u}", befehl="re.search('URTEIL: …')")
        lauf.event("testcheck", "ok", f"Urteil: {u}", datei=datei, aufruf=aid)

        # Harness-Regeln: Das Urteil "test" gilt nur mit einer tatsächlich geänderten Testdatei,
        # und der Test darf höchstens einmal pro Lauf umgeschrieben werden.
        if u == "test":
            neu = next((c for lang, c in codebloecke(text) if lang in ("python", "py", "")), None)
            alt = (paths["tests"] / "test_spiel.py").read_text(encoding="utf-8").strip()
            if test_korrigiert:
                lauf.harness("testcheck", "Urteil „test“ verworfen: Der Test wurde in diesem Lauf schon einmal geändert", warnung=True)
                u = "engine"
            elif not neu or neu.strip() == alt:
                lauf.harness("testcheck", "Urteil „test“ verworfen: keine geänderte test_spiel.py in der Antwort", warnung=True)
                u = "engine"
            else:
                try:
                    ast.parse(neu)
                except SyntaxError as e:
                    lauf.harness("testcheck", f"Urteil „test“ verworfen: neuer Test hat Syntaxfehler in Zeile {e.lineno}", warnung=True)
                    u = "engine"
        if u == "test":
            lauf.uebernimm("testcheck", text, paths["tests"], ["test_spiel.py"], ["test_spiel.py"])
            lauf.commit("testcheck", paths["tests"], f"Test korrigiert, Runde {runde + 1}")
            lauf.kante("testcheck", "tests", f"Test korrigiert, Runde {runde + 1}")
            test_korrigiert = True
        else:
            lauf.kante("testcheck", "korrektur", "URTEIL: engine")
            codeknoten(lauf, cfg, "korrektur", paths["engine"], runde, suche=[paths["engine"], integ])
            shutil.rmtree(paths["engine"] / "__pycache__", ignore_errors=True)
            lauf.kante("korrektur", "gate", f"neue engine.py, Runde {runde + 1}")

    # Integration
    lauf.event("integration", "run", "Ergebnis sammeln")
    ergebnis = lauf.dir / "ergebnis"
    ergebnis.mkdir()
    for f in integ.iterdir():
        if f.is_file() and f.name != ".git":
            shutil.copy(f, ergebnis / f.name)
    lauf.harness("integration", "Dateien nach runs/<lauf>/ergebnis kopiert")
    lauf.schreibe("07-integration.md", "# Integration\n\nAlle Branches sind zusammengeführt und die Tests bestanden.\n\n"
                                       "**Offen:** Starte den Task „4 Lauf freigeben“, um das Ergebnis nach `main` zu übernehmen.\n")
    lauf.event("integration", "ok", "Branches zusammengeführt", datei="07-integration.md")
    lauf.event("freigabe", "run", "Wartet auf deine Freigabe")


# ---------------------------------------------------------------- Weitere Befehle

def check():
    load_env()
    cfg = load_cfg()
    failed = False
    for name in sorted(set(cfg["rollen"].values())):
        try:
            agents.api_call(cfg, name, "Antworte nur mit OK.", ausweichen=False)
            print(f"OK      {name} ({cfg['anbieter'][name]['modell']})")
        except Exception as e:
            failed = True
            print(f"FEHLER  {name}: {e}")
    sys.exit(1 if failed else 0)


def wartend():
    out = []
    for d in sorted(p for p in RUNS.iterdir() if p.is_dir()):
        log = d / "events.jsonl"
        if log.exists() and log.read_text(encoding="utf-8").strip():
            last = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
            if last.get("knoten") == "freigabe" and last.get("status") == "run":
                out.append(d.name)
    return out


def approve(lauf_id):
    offen = wartend()
    if not offen:
        sys.exit("Es wartet kein Lauf auf eine Freigabe.")
    lauf_id = lauf_id or offen[-1]
    if lauf_id not in offen:
        sys.exit(f"Lauf {lauf_id} wartet nicht auf Freigabe. Wartend: {', '.join(offen)}")
    lauf = Lauf(lauf_id, False)
    git("merge", "--no-ff", "-m", f"Lauf {lauf.id} freigegeben", f"agent/{lauf.id}/integration")
    lauf.harness("freigabe", "integration nach main gemergt", befehl=f"git merge --no-ff agent/{lauf.id}/integration")
    for n in ("engine", "ui", "tests", "integration"):
        git("worktree", "remove", "--force", str(lauf.wt / n), check=False)
    lauf.schreibe("08-freigabe.md", "# Freigabe\n\nDer Merge in `main` ist erfolgt.\n")
    lauf.event("freigabe", "ok", "Merge in main freigegeben", datei="08-freigabe.md")
    print(f"Fertig. Das Ergebnis liegt in {TARGET}")
    rest = [o for o in offen if o != lauf_id]
    if rest:
        print(f"Weitere wartende Läufe: {', '.join(rest)}")


def zuruecksetzen():
    print(f"Löscht alle Läufe in {RUNS} und den Arbeitsbereich {WORK} (inklusive Git-Branches dort).")
    if input("Wirklich? Tippe ja: ").strip().lower() != "ja":
        sys.exit("Abgebrochen.")

    def schreibbar(fn, pfad, _):
        os.chmod(pfad, stat.S_IWRITE)
        fn(pfad)
    for d in [*(p for p in RUNS.iterdir() if p.is_dir()), WORK]:
        if d.exists():
            shutil.rmtree(d, onerror=schreibbar)
    print("Zurückgesetzt.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true", help="ohne API-Keys mit vorbereiteten Antworten")
    p.add_argument("--check", action="store_true", help="Keys und Modelle mit einer kurzen Anfrage testen")
    p.add_argument("--freigabe", nargs="?", const="", metavar="LAUF", help="wartenden Lauf nach main übernehmen")
    p.add_argument("--zuruecksetzen", action="store_true", help="alle Läufe und den Arbeitsbereich löschen")
    a = p.parse_args()
    RUNS.mkdir(exist_ok=True)
    if a.check:
        check()
    elif a.freigabe is not None:
        approve(a.freigabe)
    elif a.zuruecksetzen:
        zuruecksetzen()
    else:
        start(a.demo)
