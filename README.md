# Sudoku-Agenten

Mehrere Sprachmodelle bauen gemeinsam ein Browser-Sudoku. Ein Python-Skript (der Orchestrator) steuert den Ablauf, ein lokales Dashboard zeigt, was gerade passiert: welche Prompt-Datei und welcher Kontext an welches Modell gehen, was der Code drumherum tut und wie der Ablauf als Graph mit Schleifen aussieht.

## Das brauchst du

- [VS Code](https://code.visualstudio.com/)
- [Python 3.10 oder neuer](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- Für echte Läufe zusätzlich API-Keys für die Anbieter in `config.json` (vorkonfiguriert: Groq und OpenRouter) und ein angemeldetes [Claude Code](https://code.claude.com/docs/en/setup)
- Für die Abnahme der Oberfläche Edge oder Chrome. Ohne Browser bleibt die Oberfläche ungeprüft, das Dashboard warnt dann.

Node.js wird nicht benötigt.

## Schritt 1: Demo ohne Kosten

1. Öffne den Ordner in VS Code über **Datei → Ordner öffnen**.
2. **Terminal → Run Task → 1 Dashboard starten**, dann <http://localhost:8000> öffnen.
3. **Terminal → Run Task → 2 Demo ohne API-Keys**.

Der Demo-Lauf dauert etwa 45 Sekunden. Statt der Modelle antworten vorbereitete Texte aus `orchestrator/demo/`. Alles andere ist echt: Git-Worktrees, Commits, Merges und Tests. Der Lauf zeigt beide Schleifen:

- Die Prüfung lehnt die erste Recherche ab, die Recherche läuft ein zweites Mal.
- Die erste Engine ist absichtlich fehlerhaft. Das Test-Gate schlägt fehl, der Testcheck gibt der Engine die Schuld, die Korrektur repariert sie, und Runde 2 besteht.

Danach findet der Integrations-Agent einen Fehler im Zusammenspiel: Die Oberfläche erwartet leere Felder als `undefined`, die Engine liefert `0`, also lässt sich keine Ziffer setzen. Die Abnahme bedient das Ergebnis anschließend im Headless-Browser.

4. Klicke im Dashboard auf **Ergebnis spielen**.
5. **4 Lauf freigeben**. Erst dann landet das Ergebnis in `main` unter `arbeitsbereich/projekt`.

Vor einer Vorführung räumt **0 Alles zurücksetzen** alte Läufe und den Arbeitsbereich ab.

## Das Dashboard

Das Dashboard ist für die Vorführung gebaut: Es zeigt wenig und erklärt auf Klick mehr. Bedient wird es nur per Klick. Oben rechts wechselst du die Ansicht:

| Ansicht | Zeigt | Passt zu |
|---|---|---|
| **Teil 1 · Ein Agent** | Einen festen Agenten (die Engine) als Kette: Prompt + Kontext → Modell → Antwort → Harness. Ein Klick zeigt genau diesen Baustein. | Prompt, Kontext, Harness |
| **Teil 2 · Loop und Graph** | Nur den Ablauf als Graph. Ein Klick auf einen Knoten, **Zeitleiste** oder **Live** (solange ein Agent arbeitet) ersetzt ihn, **← Graph** führt zurück. Ein orangefarbenes ! markiert Knoten, bei denen die Harness eingegriffen hat. | Loop, Graph |

- Der **Info-Kreis** klappt Details und Erklärung auf.
- **Lauf ▾** enthält Laufauswahl, den Agenten für Teil 1, **Live folgen**, Startbefehl und Protokoll.
- Technische Befehle stehen zugeklappt bei den Bausteinen Modell und Harness.

## Schritt 2: Echter Lauf

1. Kopiere `.env.example` nach `.env` und trage deine Keys ein.
2. Prüfe die Modellnamen in `config.json`.
3. Passe die Aufgabe in `auftrag.md` an.
4. **2b Verbindung testen**. Jeder Anbieter muss `OK` melden. Das kostet nur wenige Tokens.
5. **3 Echten Lauf starten**. Ctrl+C im Terminal bricht ab.

Du hast nur einen Anbieter? Trage ihn unter `rollen` in `config.json` überall ein. Nur `integration` braucht Claude Code, weil dieser Agent selbst Dateien ändert. Ohne Claude Code wählt `design` außerdem ohne Websuche aus dem Modellwissen.

### Wer macht was

| Rollen | Ausführung | Warum |
|---|---|---|
| Recherche, Prüfung, Spezifikation, Tests | Sprachmodell über HTTP (Groq, OpenRouter) | Ein Aufruf, eine Antwort. Die Harness schreibt das Ergebnis in Dateien. |
| Engine, Oberfläche | Claude Code ohne Werkzeuge | Der Code muss von Hand spielbar sein. Die Harness übernimmt die Codeblöcke. |
| Testcheck | Claude Code ohne Werkzeuge | Urteilt nur über den mitgegebenen Kontext. |
| Design | Claude Code nur mit `WebSearch` und `WebFetch` | Sucht selbst nach Gestaltungsoptionen und entscheidet sich für eine, ändert aber keine Dateien. |
| Korrektur, Integration | Claude Code mit Werkzeugen | Arbeitet selbst im Worktree: liest, ändert und führt Python aus. Erlaubt sind nur die Werkzeuge in `WERKZEUGE` in `orchestrator/agents.py`. |

Modelle ohne Werkzeuge korrigieren blind. In echten Läufen pendelten sie zwischen Fehlern, weil sie ihren Code nie ausführen konnten.

## Aufbau

| Ort | Aufgabe |
|---|---|
| `auftrag.md` | Deine Aufgabe |
| `config.json` | Welcher Anbieter welche Rolle übernimmt, `max_runden` je Schleife |
| `prompts/` | Eine Rollenanweisung je Agent |
| `orchestrator/graph.py` | Der Ablauf als Daten: Knoten mit Prompt, Kontext und Ausgabe, Kanten und Schleifen |
| `orchestrator/run.py` | Führt den Graphen aus: Modell-Aufrufe, Harness, Schleifen |
| `orchestrator/agents.py` | HTTP-Aufruf an OpenAI-kompatible Schnittstellen und Start von Claude Code |
| `orchestrator/ui_check.py` | Spielt die Oberfläche im Headless-Browser bis zum Sieg |
| `orchestrator/dashboard.py` / `.html` | Zeigt die Läufe an, liest nur `runs/` |
| `runs/<lauf>/` | `start.json`, `events.jsonl`, `aufrufe/` (Prompt und Kontext je Aufruf), `live/`, Markdown-Ergebnisse |
| `arbeitsbereich/` | Zielprojekt und Git-Worktrees je Agent |

## Gut zu wissen

- **Design:** Der Design-Agent sucht im Web nach Optionen, vergleicht sie und entscheidet sich für eine (`prompts/design.md`). Die Namen der letzten acht Designs bekommt er als Hinweis, damit er etwas anderes wählt. Das Ergebnis samt Quellen steht in `runs/<lauf>/design.md` und geht als Kontext an Oberfläche und Integration. In der Demo antwortet ein vorbereiteter Text.
- **Abnahme:** `orchestrator/ui_check.py` spielt das Rätsel im Headless-Browser bis zum Sieg: sichtbare Auswahl, Setzen und Löschen auf allen Wegen, Stufenwahl, Blöcke, Konflikte.
- **Kosten:** Ein echter Lauf verbraucht Guthaben bei jedem Anbieter. Setze dort ein Limit.
- **Daten:** Auftrag und Zwischenergebnisse gehen an die Anbieter. Keine Passwörter oder vertraulichen Daten eintragen.
- **Keys:** `.env` steht in `.gitignore`. Lade diese Datei nie hoch.
- **Ausweichen:** Bei einem kurzen Ratenlimit (429) wartet der Orchestrator einmal. Bei 403, 429 oder 5xx versucht er danach den nächsten Anbieter. Das steht als ⚠ im Dashboard. `--check` weicht nie aus.
- **Harness-Regeln:** Unbrauchbarer Code (Syntaxfehler, fehlende Datei, abgeschnittene Antwort) führt zu genau einer Nachfrage mit dem Fehler als „Hinweis der Harness“. Der Testcheck darf den Test nur einmal pro Lauf ändern, und nur mit einer tatsächlich geänderten, gültigen Datei. Das Test-Gate bricht nach `test_zeitlimit` Sekunden ab (`config.json`, Standard 90).
- **Modell-Parameter:** Unter `anbieter.<name>.parameter` in `config.json` gehen zusätzliche Felder in jede Anfrage, z. B. `reasoning_effort` und `max_completion_tokens` für Reasoning-Modelle.
- **Rechte:** Test-Gate, Abnahme und Dashboard führen den erzeugten Python-Code aus, Claude Code darf in den Worktrees Dateien ändern und Python ausführen. Das ist kein Sandbox-Schutz, nutze es nur für Aufträge, denen du vertraust.
- **Kein Sicherheitsnetz:** Scheitern die Modelle, scheitert der Lauf sichtbar. Es gibt keinen versteckten Ersatzcode.
- **Recherche:** Die Recherche-Modelle antworten ohne Websuche aus ihrem Wissen. Quellen können falsch sein.
- **Port belegt?** Ändere `PORT` in `orchestrator/dashboard.py`.
