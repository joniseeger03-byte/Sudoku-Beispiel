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

Oben rechts wechselst du die Ansicht (Tasten `1` und `2`):

| Ansicht | Zeigt | Passt zu |
|---|---|---|
| **Teil 1 · Ein Agent** | Sieben Schritte nacheinander und *ein* Agent-Panel. Dass mehrere Modelle parallel arbeiten, bleibt verborgen. | Prompt, Kontext, Harness |
| **Teil 2 · Graph** | Den Ablauf als Graph mit parallelen Knoten, bedingten Kanten und Schleifen (mit Anzahl), eine Zeitleiste (wer lief wann, was lief gleichzeitig, wo ist der kritische Pfad) und ein Live-Fenster je gleichzeitig arbeitendem Agenten. Ein orangefarbenes ! markiert Knoten, bei denen die Harness eingegriffen hat. | Loop, Graph |

Oben steht außerdem eine grobe Token-Schätzung für den ganzen Lauf (4 Zeichen ≈ 1 Token), im Panel die Schätzung je Aufruf.

Das Panel hat in beiden Ansichten dieselben Reiter:

- **Prompt:** die Datei aus `prompts/`, genau so, wie sie an das Modell ging.
- **Kontext:** welche Dateien angehängt wurden, wie groß sie sind und wie sich die Nachricht zusammensetzt.
- **Aufruf:** der Startbefehl und die HTTP-Anfrage an den Anbieter (ohne Key).
- **Harness:** was normaler Code danach getan hat: Codeblock übernehmen, Syntax prüfen, committen, mergen, Tests ausführen, Urteil lesen.
- **Ausgabe:** die Antwort, live gestreamt.

**Live folgen** (Taste `F`) springt automatisch zum aktiven Agenten. Ein Klick auf einen Schritt oder Knoten hält die Auswahl fest.

## Schritt 2: Echter Lauf

1. Kopiere `.env.example` nach `.env` und trage deine Keys ein.
2. Prüfe die Modellnamen in `config.json`.
3. Passe die Aufgabe in `auftrag.md` an.
4. **2b Verbindung testen**. Jeder Anbieter muss `OK` melden. Das kostet nur wenige Tokens.
5. **3 Echten Lauf starten**. Ctrl+C im Terminal bricht ab.

Du hast nur einen Anbieter? Trage ihn unter `rollen` in `config.json` überall ein. Nur `integration` braucht Claude Code, weil dieser Agent selbst Dateien ändert.

### Wer macht was

| Rollen | Ausführung | Warum |
|---|---|---|
| Recherche, Prüfung, Spezifikation, Engine, Oberfläche, Tests | Sprachmodell über HTTP (Groq, OpenRouter) | Ein Aufruf, eine Antwort. Die Harness schreibt das Ergebnis in Dateien. |
| Testcheck | Claude Code ohne Werkzeuge | Urteilt nur über den mitgegebenen Kontext. |
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
| `orchestrator/ui_check.py` | Bedient die Oberfläche im Headless-Browser: Ziffern setzen, löschen, Konflikte |
| `orchestrator/dashboard.py` / `.html` | Zeigt die Läufe an, liest nur `runs/` |
| `runs/<lauf>/` | `start.json`, `events.jsonl`, `aufrufe/` (Prompt und Kontext je Aufruf), `live/`, Markdown-Ergebnisse |
| `arbeitsbereich/` | Zielprojekt und Git-Worktrees je Agent |

## Gut zu wissen

- **Kosten:** Ein echter Lauf verbraucht Guthaben bei jedem Anbieter. Setze dort ein Limit.
- **Daten:** Auftrag und Zwischenergebnisse gehen an die Anbieter. Keine Passwörter oder vertraulichen Daten eintragen.
- **Keys:** `.env` steht in `.gitignore`. Lade diese Datei nie hoch.
- **Ausweichen:** Bei einem kurzen Ratenlimit (429) wartet der Orchestrator einmal. Bei 403, 429 oder 5xx versucht er danach den nächsten Anbieter. Das steht als ⚠ im Dashboard. `--check` weicht nie aus.
- **Harness-Regeln:** Unbrauchbarer Code (Syntaxfehler, fehlende Datei, abgeschnittene Antwort) führt zu genau einer Nachfrage mit dem Fehler als „Hinweis der Harness“. Der Testcheck darf den Test nur einmal pro Lauf ändern, und nur mit einer tatsächlich geänderten, gültigen Datei. Das Test-Gate bricht nach `test_zeitlimit` Sekunden ab (`config.json`, Standard 90).
- **Modell-Parameter:** Unter `anbieter.<name>.parameter` in `config.json` gehen zusätzliche Felder in jede Anfrage, z. B. `reasoning_effort` und `max_completion_tokens` für Reasoning-Modelle.
- **Rechte:** Test-Gate, Abnahme und Dashboard führen den erzeugten Python-Code aus, Claude Code darf in den Worktrees Dateien ändern und Python ausführen. Das ist kein Sandbox-Schutz, nutze es nur für Aufträge, denen du vertraust.
- **Kein Sicherheitsnetz:** Scheitern die Modelle, scheitert der Lauf sichtbar. Es gibt keinen versteckten Ersatzcode.
- **Recherche:** Die Modelle antworten ohne Websuche aus ihrem Wissen. Quellen können falsch sein.
- **Port belegt?** Ändere `PORT` in `orchestrator/dashboard.py`.
