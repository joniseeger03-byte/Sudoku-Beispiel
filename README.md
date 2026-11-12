# Sudoku-Agenten

Mehrere Sprachmodelle bauen gemeinsam ein Browser-Sudoku. Ein Python-Skript (der Orchestrator) steuert den Ablauf, ein lokales Dashboard zeigt, was gerade passiert: welche Prompt-Datei und welcher Kontext an welches Modell gehen, was der Code drumherum tut und wie der Ablauf als Graph mit Schleifen aussieht.

## Das brauchst du

- [VS Code](https://code.visualstudio.com/)
- [Python 3.10 oder neuer](https://www.python.org/downloads/)
- Für echte Läufe zusätzlich API-Keys für die Anbieter in `config.json` (vorkonfiguriert: Groq und OpenRouter) und ein angemeldetes [Claude Code](https://code.claude.com/docs/en/setup)
- Für den Abnahmetest der Oberfläche Edge oder Chrome. Ohne Browser bleibt die Oberfläche ungeprüft, das Dashboard warnt dann.

Node.js wird nicht benötigt.

## Schritt 1: Demo ohne Kosten

Die Demo spielt einen **aufgezeichneten echten Lauf** ab: echte Modell-Antworten, echte Schleifen, das echte Ergebnis. Dabei antwortet kein Modell, es braucht keine API-Keys und kostet nichts.

1. Öffne den Ordner in VS Code über **Datei → Ordner öffnen**.
2. **Terminal → Run Task → 1 Dashboard starten**, dann <http://localhost:8000> öffnen.
3. Wähle unter **Lauf ▾** die Aufzeichnung (*mit Schleife* zeigt einen Rücksprung im Graphen) und das Tempo.
4. Klicke oben auf **Neuer Lauf → ▶ Demo** (oder **Terminal → Run Task → 2 Demo: Aufzeichnung abspielen**).
5. Am Ende: **Ergebnis spielen**. Die Demo endet an der Stelle, an der im echten Lauf du entscheidest. Zu entscheiden gibt es bei ihr nichts.

**Woher die Aufzeichnungen kommen:** Jeder echte Lauf landet in `runs/<lauf>/`. Dieser Ordner kommt ins Repo, alle Läufe sind also die Beispiele des Projekts. Jeder echte Lauf, der bis zur Freigabe kam, ist als Demo abspielbar, auch auf anderen Rechnern, sobald er committet ist. Gibt es noch keinen, mach zuerst Schritt 2.

Abgespielt wird mit `orchestrator/wiedergabe.py`: Ereignisse, Aufrufe, gestreamte Antworten, Berichte und Ergebnis kommen im Originaltempo oder 2×, 4×, 8× so schnell. Neue Läufe zeichnen auch auf, wann welches Stück einer Antwort kam. Bei älteren Läufen verteilt die Wiedergabe den Text gleichmäßig über die Dauer des Aufrufs.

Jede abgespielte Demo landet als `runs/<zeit>-demo/` und ist in `.gitignore` ausgeschlossen, damit keine Kopien ins Repo kommen. Es bleibt immer nur die neueste Wiedergabe liegen.

## Das Dashboard

Das Dashboard ist für die Vorführung gebaut: Es zeigt wenig und erklärt auf Klick mehr. Bedient wird es nur per Klick. Oben rechts wechselst du die Ansicht:

| Ansicht | Zeigt | Passt zu |
|---|---|---|
| **Teil 1 · Ein Agent** | Einen festen Agenten (die Engine) als Kette von links nach rechts: Prompt + Kontext → Modell → Antwort → Harness. Die Station, an der gerade gearbeitet wird, leuchtet. Ein Klick klappt ihren Inhalt direkt darunter auf. Darüber zeigt eine Leiste den ganzen Lauf in Stufen (Verstehen › Planen › Bauen › Prüfen › Fertigstellen); ein Klick auf einen Schritt wechselt den Agenten. | Prompt, Kontext, Harness |
| **Teil 2 · Loop und Graph** | Den Ablauf als Graph. Ein Klick auf einen Knoten klappt seine Stationen unter dem Graphen auf, der Graph bleibt sichtbar. **Zeitleiste** oder **Live** (solange ein Agent arbeitet) ersetzen ihn, **← Graph** führt zurück. Ein orangefarbenes ! markiert Knoten, bei denen die Harness eingegriffen hat. | Loop, Graph |

- Der **Info-Kreis** klappt Details und Erklärung auf.
- Oben rechts startest du unter **Neuer Lauf** eine **▶ Demo** oder einen **▶ Echten Lauf**, während eines Laufs steht dort **■ Abbrechen**. Ein neuer echter Lauf ist gesperrt, solange ein echter Lauf auf deine Entscheidung wartet. Demos sperren nichts.
- Wartet der angezeigte Lauf, erscheint darunter eine Leiste mit **Ergebnis spielen**, **✓ Freigeben** und **✕ Verwerfen**. Gestartet wird `orchestrator/run.py` (echt) oder `orchestrator/wiedergabe.py` (Demo) im Hintergrund, die Ausgabe steht in `runs/_prozess.log`. Es läuft immer höchstens ein Lauf aus dem Dashboard. Startbefehle nimmt das Dashboard nur von der eigenen Seite an, fremde Webseiten können keinen Lauf auslösen.
- **Lauf ▾** enthält Laufauswahl, die Aufzeichnung und das Tempo für die Demo, Startbefehl und Protokoll. Das Dashboard folgt immer dem neuesten Lauf, bis du dort einen älteren wählst. Den Agenten für Teil 1 wählst du in der Stufen-Leiste.
- Technische Befehle stehen zugeklappt bei den Bausteinen Modell und Harness.

## Schritt 2: Echter Lauf

1. Kopiere `.env.example` nach `.env` und trage deine Keys ein.
2. Prüfe die Modellnamen in `config.json`.
3. Passe die Aufgabe in `auftrag.md` an.
4. **2b Verbindung testen**. Jeder Anbieter muss `OK` melden. Das kostet nur wenige Tokens.
5. Im Dashboard **Neuer Lauf → ▶ Echter Lauf** (fragt wegen der Kosten nach) oder **3 Echten Lauf starten**. **■ Abbrechen** im Dashboard oder Ctrl+C im Terminal bricht ab.

Alles, was ein Lauf erzeugt, liegt in einem Ordner: `runs/<lauf>/`, das fertige Spiel in `runs/<lauf>/ergebnis/`. Der Orchestrator benutzt kein Git. Ins Repo kommt der Lauf mit deinem nächsten Commit.

Danach im Dashboard: **Ergebnis spielen**, dann **✓ Freigeben** oder **✕ Verwerfen** (oder Task **4 Lauf freigeben** / **4b Lauf verwerfen**). Beides hält nur deine Entscheidung im Lauf fest, Dateien werden nicht verschoben oder gelöscht. Ein freigegebener oder verworfener Lauf bleibt vollständig als Beispiel und Demo erhalten.

Du hast nur einen Anbieter? Trage ihn unter `rollen` in `config.json` überall ein. Nur `integration` braucht Claude Code, weil dieser Agent selbst Dateien ändert. Ohne Claude Code wählt `design` außerdem ohne Websuche aus dem Modellwissen.

### Wer macht was

| Rollen | Ausführung | Warum |
|---|---|---|
| Recherche, Prüfung, Spezifikation, Tests | Sprachmodell über HTTP (Groq, OpenRouter) | Ein Aufruf, eine Antwort. Die Harness schreibt das Ergebnis in Dateien. |
| Engine, Oberfläche | Claude Code ohne Werkzeuge | Der Code muss von Hand spielbar sein. Die Harness übernimmt die Codeblöcke. |
| Testcheck | Claude Code ohne Werkzeuge | Urteilt nur über den mitgegebenen Kontext. |
| Design | Claude Code nur mit `WebSearch` und `WebFetch` | Sucht selbst nach Gestaltungsoptionen und entscheidet sich für eine, ändert aber keine Dateien. |
| Korrektur, Integration | Claude Code mit Werkzeugen | Arbeitet selbst im Projektordner des Laufs: liest, ändert und führt Python aus. Erlaubt sind nur die Werkzeuge in `WERKZEUGE` in `orchestrator/agents.py`. |

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
| `orchestrator/wiedergabe.py` | Die Demo: spielt einen aufgezeichneten echten Lauf ab, ohne Modelle |
| `orchestrator/dashboard.py` / `.html` | Zeigt die Läufe an, liest nur `runs/` |
| `runs/<lauf>/` | Die Beispiele, im Repo: `start.json`, `events.jsonl`, `aufrufe/` (Prompt und Kontext je Aufruf), `live/` (Antworten und ihr Takt), Markdown-Berichte, `ergebnis/`. Demo-Wiedergaben (`*-demo`) sind ausgeschlossen. |

## Gut zu wissen

- **Design:** Der Design-Agent sucht im Web nach Optionen, vergleicht sie und entscheidet sich für eine (`prompts/design.md`). Die Namen der letzten acht Designs bekommt er als Hinweis, damit er etwas anderes wählt. Das Ergebnis samt Quellen steht in `runs/<lauf>/design.md` und geht als Kontext an Oberfläche und Integration.
- **Abnahmetest:** `orchestrator/ui_check.py` spielt das Rätsel im Headless-Browser bis zum Sieg: sichtbare Auswahl, Setzen und Löschen auf allen Wegen, Stufenwahl, Blöcke, Konflikte.
- **Kosten:** Ein echter Lauf verbraucht Guthaben bei jedem Anbieter. Setze dort ein Limit.
- **Daten:** Auftrag und Zwischenergebnisse gehen an die Anbieter. Keine Passwörter oder vertraulichen Daten eintragen.
- **Keys:** `.env` steht in `.gitignore`. Lade diese Datei nie hoch.
- **Ausweichen:** Bei einem kurzen Ratenlimit (429) wartet der Orchestrator einmal. Bei 403, 429 oder 5xx versucht er danach den nächsten Anbieter. Das steht als ⚠ im Dashboard. `--check` weicht nie aus.
- **Harness-Regeln:** Unbrauchbarer Code (Syntaxfehler, fehlende Datei, abgeschnittene Antwort) führt zu genau einer Nachfrage mit dem Fehler als „Hinweis der Harness“. Alle Agenten arbeiten in einem Projektordner, jeder nur an seinen eigenen Dateien. Engine, Oberfläche und Tests schreiben nicht selbst, die Harness übernimmt ihre Codeblöcke. Die Korrektur darf nur `engine.py` ändern, die Integration nicht `test_spiel.py`. Alles andere setzt die Harness danach zurück und meldet es als ⚠. Der Testcheck darf den Test nur einmal pro Lauf ändern, und nur mit einer tatsächlich geänderten, gültigen Datei. Das Test-Gate bricht nach `test_zeitlimit` Sekunden ab (`config.json`, Standard 90).
- **Modell-Parameter:** Unter `anbieter.<name>.parameter` in `config.json` gehen zusätzliche Felder in jede Anfrage, z. B. `reasoning_effort` und `max_completion_tokens` für Reasoning-Modelle.
- **Rechte:** Test-Gate, Abnahmetest und Dashboard führen den erzeugten Python-Code aus, Claude Code darf im Projektordner des Laufs Dateien ändern und Python ausführen. Das ist kein Sandbox-Schutz, nutze es nur für Aufträge, denen du vertraust.
- **Kein Sicherheitsnetz:** Scheitern die Modelle, scheitert der Lauf sichtbar. Es gibt keinen versteckten Ersatzcode.
- **Recherche:** Die Recherche-Modelle antworten ohne Websuche aus ihrem Wissen. Quellen können falsch sein.
- **Port belegt?** Ändere `PORT` in `orchestrator/dashboard.py`.
