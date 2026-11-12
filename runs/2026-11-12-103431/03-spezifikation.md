## Spezifikation (Markdown)

### 1. Überblick
Entwicklung eines komplett browser‑basierten Sudoku‑Spiels ohne Backend.  
Die Anwendung besteht aus:

| Komponente | Aufgabe |
|------------|---------|
| **engine.py** | Generiert Sudokus, prüft Lösungen und Konflikte – rein Python‑Standardbibliothek. |
| **index.html / board.js / style.css** | UI im Browser, lädt Rätsel via `fetch('api/neu?stufe=…')`. |
| **test_spiel.py** | Automatisierte Tests, Exit‑Code ≠ 0 bei Fehler. |

Alle Anforderungen aus dem Auftrag, der Recherche und den Prüfungseinwänden werden berücksichtigt.

---

### 2. Vertrag  

> **engine.py nutzt nur die Python-Standardbibliothek.**  
> **`CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}`** gibt die Hinweiszahl je Stufe an.  
> **`generate(level)`** liefert ein `dict` mit den Schlüsseln `puzzle`, `solution`, `clues` und `level`.  
> * `puzzle` & `solution` sind Listen mit 81 Zahlen (0 = leer).  
> * `clues` ist die Anzahl der Nicht‑Null‑Zahlen in `puzzle` und muss exakt `CLUES[level]` sein.  
> **`solutions(puzzle, limit)`** gibt maximal `limit` Lösungen zurück.  
> **`conflicts(grid)`** liefert ein `set` der Indizes (0‑80), die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
> **`python engine.py neu <stufe>`** gibt das Ergebnis von `generate` als JSON aus.  
> **`index.html`, `board.js`, `style.css`** bilden die Oberfläche. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')` (relativ zur Seite) und verarbeitet das gleiche JSON.  
> **UI‑Vertrag:**  
> * Jedes der 81 Felder ist ein Element mit `data-index="0"` … `"80"`. Der Inhalt ist die Ziffer (kein `<input>`).  
> * Ziffern‑Buttons tragen `data-digit="1"` … `"9"`, der Lösch‑Button `data-digit="0"`.  
> * Drei Schwierigkeits‑Buttons besitzen `data-stufe="leicht"`, `"mittel"` und `"schwer"` und starten sofort ein neues Rätsel.  
> * Tastatureingaben (1‑9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet.  
> * Das aktuell gewählte Feld erhält eine eigene Hervorhebungs‑Klasse.  
> * 3×3‑Blöcke sind durch dickere Linien bzw. größere Abstände erkennbar.  
> * Felder im Konflikt erhalten die Klasse `konflikt`.  
> * Bei vollständiger, korrekter Lösung trägt das `<body>` die Klasse `geloest`.  
> **`test_spiel.py`** wird mit `python test_spiel.py` ausgeführt und beendet bei jedem Fehler mit einem Exit‑Code ≠ 0.

---

### 3. Akzeptanzkriterien  

| Kriterium | Beschreibung | Hinweis |
|-----------|--------------|--------|
| **A1 – Generator‑Korrektheit** | `engine.py generate(level)` liefert ein Puzzle mit exakt `CLUES[level]` vorgegebenen Ziffern und eine gültige Lösung. | Test prüft `len([v for v in puzzle if v!=0]) == CLUES[level]` und dass `solutions(puzzle, 2)` = 1. |
| **A2 – Eindeutige Lösung** | Für jedes generierte Puzzle gibt `solutions(puzzle, 2)` **nur** eine Lösung zurück. | Limit = 2, Rückgabe‑Länge = 1. |
| **A3 – Konflikt‑Erkennung** | `conflicts(grid)` liefert exakt die Indizes aller Zellen, die Regelverletzungen (Zeile, Spalte, Block) enthalten. | Verglichen mit einer Referenz‑Implementierung. |
| **A4 – CLI‑Ausgabe** | `python engine.py neu mittel` gibt ein gültiges JSON‑Objekt (wie von `generate`) aus und beendet mit Exit‑Code 0. | JSON‑Schema‑Validierung. |
| **A5 – UI‑Initialisierung** | Beim Laden von `index.html` wird ein Puzzle via `fetch('api/neu?stufe=mittel')` abgerufen und korrekt im Grid angezeigt. | Feld‑`data-index`‑Werte entsprechen den erhaltenen Zahlen. |
| **A6 – Feld‑Interaktion** | Klick auf ein leeres Feld setzt den Fokus; Klick auf einen Ziffern‑Button (`data-digit`) trägt die Ziffer ins Feld ein; `data-digit="0"` löscht den Inhalt. | Visuelle Fokus‑Klasse vorhanden, `data-digit` wirkt. |
| **A7 – Tastatur‑Steuerung** | Eingabe von 1‑9, Pfeiltasten, Entf und Rücktaste verändert das fokussierte Feld wie bei den Buttons. | `keydown`‑Handler testet. |
| **A8 – Konflikt‑Highlighting** | Nach jeder Eingabe werden alle konflikt‑betroffenen Zellen mit der Klasse `konflikt` markiert. | `conflicts(currentGrid)` wird aufgerufen, Klassen‑Update geprüft. |
| **A9 – Lösungs‑Erkennung** | Sobald das Puzzle vollständig und konfliktfrei ist, bekommt `<body>` die Klasse `geloest`. | Test prüft Klasse nach korrekter Eingabe. |
| **A10 – Schwierigkeits‑Buttons** | Klick auf einen Button mit `data-stufe` startet sofort ein neues Puzzle der entsprechenden Stufe und aktualisiert das Grid. | Netzwerk‑Aufruf und UI‑Refresh verifiziert. |
| **A11 – Test‑Suite** | `test_spiel.py` führt mindestens die Tests A1‑A10 aus und beendet mit Exit‑Code 0, wenn alles erfolgreich ist. | CI‑Kompatibel. |
| **A12 – Performance‑Grenze** | Das Generieren eines „schwer“-Rätsels (inkl. Eindeutigkeitsprüfung) dauert im Browser ≤ 2 Sekunden auf einem durchschnittlichen Desktop‑PC. | Zeitmessung im Test. |
| **A13 – Responsives Layout** | Das Grid skaliert korrekt auf Bildschirmbreiten von 320 px bis 1920 px, 3×3‑Blöcke bleiben erkennbar. | Visueller Smoke‑Test. |
| **A14 – Barrierefreiheit** | Alle interaktiven Elemente sind per Tab‑Navigation erreichbar und besitzen sinnvolle `aria-` Attribute. | Axe‑Linter‑Durchlauf ohne Fehler. |

Erfüllte Kriterien A1‑A14 gelten als **Abnahme** des Projekts.