"""Demo: spielt einen aufgezeichneten echten Lauf ab. Ohne Modelle, ohne API-Keys, ohne git.

Jeder echte Lauf zeichnet in runs/<lauf>/ alles auf, was das Dashboard braucht: Ereignisse mit Zeitstempel,
Aufrufe mit Prompt und Kontext, die gestreamten Antworten, Berichte und das fertige Ergebnis. Dieses Skript
schreibt das alles im Originaltempo (oder schneller) in einen neuen Lauf. Das Dashboard zeigt ihn wie einen echten.

Aufruf: python orchestrator/wiedergabe.py [LAUF] [--tempo 2]
Quelle: runs/<LAUF>, ohne LAUF der neueste abspielbare Lauf. Die Wiedergabe landet in runs/<zeit>-demo
und ist in .gitignore ausgeschlossen, damit nicht jede abgespielte Demo als Kopie ins Repo kommt.
Es bleibt immer nur die neueste Wiedergabe liegen, ältere löscht dieses Skript beim Start.
"""
import argparse
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
TEMPI = (1, 2, 4, 8)


def lies_json(p, fallback=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback


def events(d):
    p = d / "events.jsonl"
    return [json.loads(z) for z in p.read_text(encoding="utf-8").splitlines() if z.strip()] if p.exists() else []


def bis_zur_freigabe(ev):
    """Die Aufzeichnung endet dort, wo der Lauf auf die Entscheidung wartet. Was danach kam, gehört nicht dazu."""
    for i, e in enumerate(ev):
        if e.get("knoten") == "freigabe" and e.get("status") == "run":
            return ev[:i + 1]
    return None


def ist_aufzeichnung(d):
    """Abspielbar ist jeder echte Lauf, der bis zum Ende kam (auf die Freigabe gewartet hat)."""
    start = lies_json(d / "start.json", {}) or {}
    return start.get("modus") == "live" and not start.get("quelle") and bis_zur_freigabe(events(d)) is not None


def aufzeichnungen(runs=RUNS):
    """Alle abspielbaren Läufe in runs/, neueste zuerst."""
    out = []
    for d in sorted((p for p in runs.iterdir() if p.is_dir()), key=lambda p: p.name, reverse=True) if runs.exists() else []:
        if not ist_aufzeichnung(d):
            continue
        ev = bis_zur_freigabe(events(d))
        out.append({"id": d.name, "pfad": d,
                    "dauer": round(ev[-1]["t"] - ev[0]["t"]) if ev and "t" in ev[0] else None,
                    "schleifen": sum(1 for e in ev if e.get("status") == "run" and (e.get("runde") or 1) > 1),
                    "ergebnis": (d / "ergebnis" / "index.html").exists()})
    return out


def stuecke(quelle, rec):
    """Wann welches Stück der Antwort kam. Neue Läufe haben das aufgezeichnet (live/<id>.takt),
    bei älteren wird der Text gleichmäßig über die Dauer des Aufrufs verteilt."""
    text = (quelle / "live" / f"{rec['id']}.txt")
    text = text.read_text(encoding="utf-8", errors="replace") if text.exists() else ""
    if not text:
        return []
    takt = quelle / "live" / f"{rec['id']}.takt"
    if takt.exists():
        out, pos = [], 0
        for z in takt.read_text(encoding="utf-8").splitlines():
            try:
                t, n = json.loads(z)["t"], json.loads(z)["n"]
            except (json.JSONDecodeError, KeyError):
                continue
            out.append((t, text[pos:pos + n]))
            pos += n
        if pos < len(text):
            out.append((out[-1][0] if out else rec["start"], text[pos:]))
        return out
    start, dauer = rec["start"], max(rec.get("dauer") or 1, 1)
    von = start + min(2.0, dauer * .2)        # die ersten Sekunden denkt das Modell, bevor Text kommt
    n = max(1, min(400, int((start + dauer - von) / .35)))
    schritt = len(text) / n
    return [(von + (start + dauer - von) * (i + 1) / n, text[round(i * schritt):round((i + 1) * schritt)]) for i in range(n)]


def plan(quelle):
    """Alles, was im Original passiert ist, als zeitlich sortierte Liste: (Zeitpunkt, Reihenfolge, Aktion)."""
    ev = bis_zur_freigabe(events(quelle))
    aufrufe = {}
    for p in sorted((quelle / "aufrufe").glob("*.json")):
        rec = lies_json(p)
        if rec and rec.get("start"):
            aufrufe[rec["id"]] = rec
    benutzt = {e.get("aufruf") for e in ev}
    aktionen = []
    for i, e in enumerate(ev):
        aktionen.append((e["t"], 2, i, ("event", e)))
    for aid, rec in aufrufe.items():
        if aid not in benutzt:
            continue
        aktionen.append((rec["start"], 1, aid, ("aufruf_start", rec)))
        for j, (t, stueck) in enumerate(stuecke(quelle, rec)):
            aktionen.append((t, 3, f"{aid}-{j:05d}", ("live", aid, stueck)))
        aktionen.append((rec["start"] + (rec.get("dauer") or 0), 4, aid, ("aufruf_ende", rec)))
    aktionen.sort(key=lambda a: (a[0], a[1], str(a[2])))
    return ev, aktionen


def abspielen(quelle, tempo):
    ev, aktionen = plan(quelle)
    start_q = lies_json(quelle / "start.json", {})
    # Ältere Wiedergaben sind nur Kopien von Läufen, die ohnehin in runs/ liegen
    for alt in RUNS.glob("*-demo"):
        if alt.is_dir() and alt.parent == RUNS and lies_json(alt / "start.json", {}).get("quelle"):
            shutil.rmtree(alt)
    lauf_id = datetime.now().strftime("%Y-%m-%d-%H%M%S") + "-demo"
    ziel = RUNS / lauf_id
    (ziel / "aufrufe").mkdir(parents=True)
    (ziel / "live").mkdir()
    befehl = f"python orchestrator/wiedergabe.py {quelle.name}" + (f" --tempo {tempo}" if tempo != 1 else "")
    (ziel / "start.json").write_text(json.dumps({**start_q, "befehl": befehl, "modus": "demo", "quelle": quelle.name,
                                                 "tempo": tempo, "zeit": datetime.now().isoformat(timespec="seconds")},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"$ {befehl}\nLauf {lauf_id}: Aufzeichnung von {quelle.name}, {tempo}× so schnell\n", flush=True)

    t0, jetzt0 = aktionen[0][0], time.time()
    neu = lambda t: jetzt0 + (t - t0) / tempo   # Originalzeit → Wiedergabezeit
    for t, _, _, aktion in aktionen:
        warten = neu(t) - time.time()
        if warten > 0:
            time.sleep(warten)
        art = aktion[0]
        if art == "aufruf_start":
            rec = {k: v for k, v in aktion[1].items() if k not in ("dauer", "antwort_zeichen", "kosten_usd", "fehler")}
            rec.update(status="run", start=neu(aktion[1]["start"]), aufzeichnung=quelle.name)
            (ziel / "aufrufe" / f"{rec['id']}.json").write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        elif art == "live":
            with open(ziel / "live" / f"{aktion[1]}.txt", "a", encoding="utf-8") as f:
                f.write(aktion[2])
        elif art == "aufruf_ende":
            rec = dict(aktion[1])
            dauer = rec.get("dauer") or 0
            rec.update(start=neu(rec["start"]), dauer=round(dauer / tempo, 1), dauer_original=dauer, aufzeichnung=quelle.name)
            (ziel / "aufrufe" / f"{rec['id']}.json").write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
        else:
            e = dict(aktion[1])
            if e.get("datei") and (quelle / e["datei"]).exists():
                shutil.copy(quelle / e["datei"], ziel / e["datei"])
            if e.get("knoten") == "freigabe" and e.get("status") == "run" and (quelle / "ergebnis").exists():
                shutil.copytree(quelle / "ergebnis", ziel / "ergebnis")
            e.update(zeit=datetime.now().strftime("%H:%M:%S"), t=round(time.time(), 2))
            with open(ziel / "events.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
            print(f"[{e['zeit']}] {e['knoten']}: {e['text']}", flush=True)
    # Berichte, auf die kein Ereignis zeigt (etwa die Spezifikation), gehören trotzdem dazu
    for p in quelle.glob("*.md"):
        if not (ziel / p.name).exists():
            shutil.copy(p, ziel / p.name)
    return lauf_id


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("lauf", nargs="?", help="aufgezeichneter Lauf, Standard: der neueste")
    a.add_argument("--tempo", type=int, default=1, choices=TEMPI, help="wie viel schneller als im Original")
    args = a.parse_args()
    liste = aufzeichnungen()
    if not liste:
        sys.exit("Noch keine Aufzeichnung. Lass einmal einen echten Lauf bis zur Freigabe laufen, dann ist er als Demo abspielbar.")
    wahl = next((x for x in liste if x["id"] == args.lauf), None) if args.lauf else liste[0]
    if not wahl:
        sys.exit(f"Keine Aufzeichnung {args.lauf}. Vorhanden: {', '.join(x['id'] for x in liste)}")
    RUNS.mkdir(exist_ok=True)
    abspielen(wahl["pfad"], args.tempo)
