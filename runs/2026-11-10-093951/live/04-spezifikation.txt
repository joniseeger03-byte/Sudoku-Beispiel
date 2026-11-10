## 1. Spezifikation (Kurzfassung)

| Abschnitt | Inhalt |
|-----------|--------|
| **Ziel** | Ein vollständig spielbares Sudoku im Browser ohne serverseitiges Backend. |
| **Technologie** | Nur HTML + CSS + JavaScript (ES6) im Front‑End; Python‑Generator (`engine.py`) als reines CLI‑Tool, das ausschließlich die Standardbibliothek nutzt. |
| **Funktionalität** | 1. Drei Schwierigkeitsgrade (leicht, mittel, schwer). 2. Einmaliger Puzzle‑Download per `fetch('api/neu?stufe=…')`. 3. Tastatur‑ & Touch‑Eingabe. 4. Sofortige Konflikt‑Markierung. 5. Visuelle Anzeige bei kompletter Lösung. |
| **Qualität** | • Jede erzeugte Aufgabe hat **genau** eine Lösung. <br>• Generation ist performant (max. 2 s pro Puzzle im CLI). <br>• UI ist barrierefrei und reagiert konsistent auf Maus, Touch & Keyboard. |
| **Test** | `test_spiel.py` muss ohne Fehler (Exit‑Code 0) durchlaufen. |

---

## 2. Akzeptanzkriterien  

Die Kriterien sind nummeriert **A1, A2, …**. Alle müssen **erfüllt** sein, damit das Projekt als abgeschlossen gilt.

| Nr. | Kriterium | Hinweis (Bezug zu Einwänden) |
|-----|-----------|------------------------------|
| **A1** | `engine.py` verwendet **nur** Module aus der Python‑Standardbibliothek. | – |
| **A2** | Das Mapping `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` ist im Code unverändert vorhanden und wird zur Validierung der Hinweis‑Zahl verwendet. | – |
| **A3** | `generate(level)` gibt ein `dict` mit den Schlüsseln `puzzle`, `solution`, `clues` und `level` zurück. <br>• `puzzle` & `solution` sind Listen mit 81 Integern (0 = leer). <br>• `clues` == Anzahl von Nicht‑Null‑Einträgen in `puzzle` == `CLUES[level]`. | – |
| **A4** | `solutions(puzzle, limit)` liefert **höchstens** `limit` vollständige Lösungen (jeweils 81‑Element‑Listen). | – |
| **A5** | `conflicts(grid)` liefert ein `set` aller Indizes (0‑80), die in ihrer Zeile, Spalte oder ihrem 3×3‑Block mit einer anderen Zelle kollidieren. | – |
| **A6** | Der CLI‑Befehl `python engine.py neu <stufe>` schreibt das Ergebnis von `generate` **als JSON** in `stdout`. | – |
| **A7** | `index.html`, `board.js` und `style.css` bilden die komplette UI. <br>• `board.js` ruft per `fetch('api/neu?stufe=mittel')` das gleiche JSON wie A6 ab (relativ zur Seite). | – |
| **A8** | UI‑Elemente: <br>• Jedes der 81 Felder ist ein DOM‑Element mit `data-index="0"` … `data-index="80"` und enthält die Ziffer als Text (kein `<input>`). <br>• Ziffern‑Buttons besitzen `data-digit="1"` … `"9"`, der Löschen‑Button `data-digit="0"`. <br>• Drei Schwierigkeits‑Buttons besitzen `data-stufe="leicht"`, `"mittel"` und `"schwer"` und starten sofort ein neues Puzzle. | – |
| **A9** | **Eingabe**: <br>• Tastatur‑Events (1‑9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet. <br>• Das aktuell ausgewählte Feld bekommt eine eigene CSS‑Klasse (`ausgewaehlt` o.Ä.) zur Hervorhebung. | – |
| **A10** | **Visuelle Markierung**: <br>• Konflikt‑Zellen erhalten die Klasse `konflikt`. <br>• Bei vollständiger, korrekter Lösung erhält `<body>` die Klasse `geloest`. | – |
| **A11** | **Schwierigkeits‑Steuerung**: Das erzeugte Puzzle enthält exakt die in `CLUES` definierte Anzahl an Hinweisen, sodass die drei Schwierigkeitsgrade klar unterschieden werden können. | **Einwand 1** – Begrenzte Generation‑Zeit. |
| **A12** | **Eindeutigkeit**: Für jedes erzeugte Puzzle wird mit `solutions(puzzle, 2)` geprüft, dass **höchstens** eine Lösung existiert. Falls mehr als eine gefunden wird, wird das Puzzle verworfen und ein neues generiert. | **Einwand 2** – Vermeidung mehrdeutiger Rätsel. |
| **A13** | **Performance‑Grenze**: Die komplette Erzeugung (inkl. Eindeutigkeits‑Check) darf nicht länger als **2 s** auf einer normalen Entwickler‑CPU (z. B. i5‑8250U) dauern. | **Einwand 1** – Rechenintensität begrenzen. |
| **A14** | **Spielbarkeit**: Das generierte Puzzle muss mit dem integrierten Solver in ≤ 500 Backtracking‑Schritten lösbar sein (Messwert intern, nicht UI‑sichtbar). Damit wird sichergestellt, dass das Rätsel nicht „unlösbar‑durch‑Raten“ ist. | **Einwand 3** – Lösbarkeit sicherstellen. |
| **A15** | **Test‑Suite**: `test_spiel.py` läuft mit `python test_spiel.py` und beendet sich mit Exit‑Code 0, wenn **alle** oben genannten Funktionen korrekt arbeiten. | – |
| **A16** | **Dokumentation**: Das Repository enthält eine `README.md` mit Install‑/Ausführungs‑Hinweisen, einer kurzen Beschreibung der Architektur und einem Verweis auf die Akzeptanzkriterien (A1‑A15). | – |

---

## 3. Vertrag  

Der nachfolgende Abschnitt ist **unverändert** zu übernehmen.

---  

**Vertrag**  

- `engine.py` nutzt nur die Python-Standardbibliothek.  
- `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
- `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. `puzzle` und `solution` sind Listen mit 81 Zahlen, 0 steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in `puzzle` und gleich `CLUES[level]`.  
- `solutions(puzzle, limit)` liefert eine Liste mit höchstens `limit` Lösungen.  
- `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
- `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
- `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
- Bedienvertrag der Oberfläche: Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein input). Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `"9"`, der Löschen-Button trägt `data-digit="0"`. Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel. Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet. Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben. Die 3×3‑Blöcke sind durch dickere Linien oder größere Abstände erkennbar. Felder im Konflikt tragen die Klasse `konflikt`. Ist das Rätsel richtig gelöst, trägt `body` die Klasse `geloest`.  
- `test_spiel.py` läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit‑Code ungleich 0.  

---  