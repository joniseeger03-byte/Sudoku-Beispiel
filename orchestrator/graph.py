"""Der Ablauf als Graph: Phasen, Knoten und Kanten.

run.py führt diesen Graphen aus, das Dashboard zeichnet ihn.

Knotenarten:
- "modell"  ein Sprachmodell-Aufruf. Bekommt prompts/<prompt> plus die Kontext-Dateien.
- "agent"   wie "modell", aber mit Werkzeugen: arbeitet selbst im Worktree (Claude Code).
- "skript"  normaler Code ohne Modell, zum Beispiel das Test-Gate.
- "mensch"  du.

Kontext-Dateien:
- {runde} wird durch die aktuelle Runde ersetzt.
- Ein "?" am Ende heißt: nur mitgeben, wenn die Datei schon existiert.
"""

PHASEN = [
    ("auftrag", "Auftrag"),
    ("recherche", "Recherche"),
    ("pruefung", "Prüfung"),
    ("spezifikation", "Spezifikation"),
    ("umsetzung", "Umsetzung"),
    ("test", "Test"),
    ("ergebnis", "Ergebnis"),
]

KNOTEN = {
    "auftrag": {
        "titel": "Auftrag", "phase": "auftrag", "art": "mensch", "pos": (0, 1),
        "ausgabe": ["00-auftrag.md"],
    },
    "recherche_a": {
        "titel": "Recherche A", "phase": "recherche", "art": "modell", "pos": (1, 0),
        "prompt": "recherche_a.md",
        "kontext": ["00-auftrag.md", "02-pruefung.md?"],
        "ausgabe": ["01a-generator.md"],
    },
    "recherche_b": {
        "titel": "Recherche B", "phase": "recherche", "art": "modell", "pos": (1, 2),
        "prompt": "recherche_b.md",
        "kontext": ["00-auftrag.md", "02-pruefung.md?"],
        "ausgabe": ["01b-spielablauf.md"],
    },
    "pruefung": {
        "titel": "Prüfung", "phase": "pruefung", "art": "modell", "pos": (2, 1),
        "prompt": "pruefung.md",
        "kontext": ["00-auftrag.md", "01a-generator.md", "01b-spielablauf.md"],
        "ausgabe": ["02-pruefung.md"],
    },
    "spezifikation": {
        "titel": "Spezifikation", "phase": "spezifikation", "art": "modell", "pos": (3, 1),
        "prompt": "spezifikation.md",
        "kontext": ["00-auftrag.md", "01a-generator.md", "01b-spielablauf.md", "02-pruefung.md"],
        "ausgabe": ["03-spezifikation.md"],
    },
    "engine": {
        "titel": "Engine", "phase": "umsetzung", "art": "modell", "pos": (4, 0),
        "prompt": "engine.md",
        "kontext": ["03-spezifikation.md"],
        "ausgabe": ["engine.py"],
    },
    "ui": {
        "titel": "Oberfläche", "phase": "umsetzung", "art": "modell", "pos": (4, 1),
        "prompt": "ui.md",
        "kontext": ["03-spezifikation.md"],
        "ausgabe": ["index.html", "board.js", "style.css"],
    },
    "tests": {
        "titel": "Tests", "phase": "umsetzung", "art": "modell", "pos": (4, 2),
        "prompt": "tests.md",
        "kontext": ["03-spezifikation.md"],
        "ausgabe": ["test_spiel.py"],
    },
    "gate": {
        "titel": "Test-Gate", "phase": "test", "art": "skript", "pos": (5, 1),
        "befehl": "python test_spiel.py",
        "ausgabe": ["05-test-gate-runde-{runde}.md"],
    },
    "testcheck": {
        "titel": "Testcheck", "phase": "test", "art": "modell", "pos": (6, 2),
        "prompt": "testcheck.md",
        "kontext": ["03-spezifikation.md", "test_spiel.py", "05-test-gate-runde-{runde}.md"],
        "ausgabe": ["06-testcheck-runde-{runde}.md"],
    },
    "korrektur": {
        "titel": "Korrektur", "phase": "test", "art": "agent", "pos": (5, 2),
        "prompt": "korrektur.md",
        "kontext": ["03-spezifikation.md", "engine.py", "test_spiel.py", "05-test-gate-runde-{runde}.md"],
        "ausgabe": ["engine.py"],
    },
    "integration": {
        "titel": "Integration", "phase": "ergebnis", "art": "agent", "pos": (7, 1),
        "prompt": "integration.md",
        "kontext": ["03-spezifikation.md"],
        "ausgabe": ["07-integration-runde-{runde}.md"],
    },
    "abnahme": {
        "titel": "Abnahme", "phase": "ergebnis", "art": "skript", "pos": (8, 1),
        "befehl": "python test_spiel.py && python ui_check.py",
        "ausgabe": ["08-abnahme-runde-{runde}.md"],
    },
    "freigabe": {
        "titel": "Freigabe", "phase": "ergebnis", "art": "mensch", "pos": (9, 1),
        "befehl": "python orchestrator/run.py --freigabe",
        "ausgabe": ["09-freigabe.md"],
    },
}

# (von, nach, art, beschriftung). art: "" normal, "bedingt" nur bei diesem Urteil, "schleife" zurück
KANTEN = [
    ("auftrag", "recherche_a", "", ""),
    ("auftrag", "recherche_b", "", ""),
    ("recherche_a", "pruefung", "", ""),
    ("recherche_b", "pruefung", "", ""),
    ("pruefung", "spezifikation", "bedingt", "ok"),
    ("pruefung", "recherche_a", "schleife", "nacharbeiten"),
    ("pruefung", "recherche_b", "schleife", "nacharbeiten"),
    ("spezifikation", "engine", "", ""),
    ("spezifikation", "ui", "", ""),
    ("spezifikation", "tests", "", ""),
    ("engine", "gate", "", ""),
    ("ui", "gate", "", ""),
    ("tests", "gate", "", ""),
    ("gate", "integration", "bedingt", "bestanden"),
    ("gate", "testcheck", "bedingt", "nicht bestanden"),
    ("testcheck", "korrektur", "bedingt", "URTEIL: engine"),
    ("testcheck", "tests", "schleife", "URTEIL: test"),
    ("korrektur", "gate", "schleife", "neue engine.py"),
    ("integration", "abnahme", "", ""),
    ("abnahme", "freigabe", "bedingt", "bestanden"),
    ("abnahme", "integration", "schleife", "nicht bestanden"),
]


def als_json():
    return {
        "phasen": [{"id": p, "titel": t} for p, t in PHASEN],
        "knoten": {k: {**v, "pos": list(v["pos"])} for k, v in KNOTEN.items()},
        "kanten": [{"von": a, "nach": b, "art": art, "text": text} for a, b, art, text in KANTEN],
    }
