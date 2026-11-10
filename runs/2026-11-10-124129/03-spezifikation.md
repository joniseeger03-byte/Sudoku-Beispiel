## Spezifikation – Sudoku fürs Web  

**Kurzbeschreibung**  
Ein browserbasiertes Sudoku‑Spiel ohne Backend‑Komponente. Der Generator liefert pro Schwierigkeitsstufe (`leicht`, `mittel`, `schwer`) ein Puzzle mit exakt einer Lösung. Die UI besteht aus `index.html`, `board.js` und `style.css` und unterstützt Tastatur‑ sowie Touch‑Eingaben.  

---  

## 1. Funktionen  

| Funktions‑ID | Beschreibung |
|--------------|--------------|
| **F1** | `engine.py` erzeugt per `generate(level)` ein Puzzle‑Objekt (JSON) mit exakt `CLUES[level]` vorgegebenen Zahlen. |
| **F2** | `engine.py` liefert über `solutions(puzzle, limit)` maximal `limit` Lösungen. |
| **F3** | `engine.py` liefert mit `conflicts(grid)` das Set der indizierten Zellen, die in Zeile, Spalte oder Block kollidieren. |
| **F4** | `python engine.py neu <stufe>` gibt das Ergebnis von **F1** als JSON aus. |
| **F5** | `board.js` ruft per `fetch('api/neu?stufe=mittel')` das Puzzle‑JSON ab (relativ zur Seite). |
| **F6** | UI‑Elemente: jedes der 81 Felder hat `data-index="0"` … `"80"`; die Ziffer wird als Text (keine `<input>`). |
| **F7** | Ziffern‑Buttons besitzen `data-digit="1"` … `"9"`, der Lösch‑Button `data-digit="0"`. |
| **F8** | Drei Schwierigkeits‑Buttons besitzen `data-stufe="leicht"`, `data-stufe="mittel"`, `data-stufe="schwer"` und starten sofort ein neues Puzzle. |
| **F9** | Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über ein globales `keydown`‑Listener auf `document` verarbeitet. |
| **F10** | Das aktuell ausgewählte Feld bleibt über eine eigene CSS‑Klasse hervorgehoben. |
| **F11** | 3×3‑Blöcke sind visuell durch dickere Linien bzw. größere Abstände erkennbar. |
| **F12** | Zellen, die in Konflikt stehen, erhalten die Klasse `konflikt`. |
| **F13** | Wird das Puzzle korrekt gelöst, bekommt das `<body>` die Klasse `geloest`. |
| **F14** | `test_spiel.py` prüft die gesamte Anwendung und beendet sich mit einem Nicht‑0‑Exit‑Code bei Fehlern. |

---  

## 2. Abnahmekriterien  

| Kriterium | Beschreibung | Erfüllungsnachweis |
|-----------|--------------|-------------------|
| **A1** | `engine.py` verwendet **nur** die Python‑Standardbibliothek. | Quellcode‑Review, kein Import von Dritt‑Paketen. |
| **A2** | `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` ist unverändert definiert. | Konstanten‑Check im Code. |
| **A3** | `generate(level)` liefert ein Dict mit Schlüsseln `puzzle`, `solution`, `clues`, `level`. `puzzle` und `solution` enthalten je 81 Zahlen (0 = leer). `clues` entspricht `CLUES[level]`. | Unit‑Test, der alle vier Felder prüft und die Länge von `puzzle`/`solution` = 81 bestätigt. |
| **A4** | `solutions(puzzle, limit)` liefert **höchstens** `limit` vollständige Lösungen. | Test mit `limit=2` – liefert 0, 1 oder 2 Lösungen, nie mehr. |
| **A5** | `conflicts(grid)` gibt ein Set aller Indizes zurück, die in Zeile, Spalte oder Block duplizierte Zahlen enthalten. | Vergleich mit einer manuellen Konflikt‑Berechnung für zufällige Grids. |
| **A6** | Der Aufruf `python engine.py neu <stufe>` gibt das JSON‑Objekt von **A3** exakt aus. | Integrationstest, der die Konsolenausgabe parst und die Struktur prüft. |
| **A7** | `board.js` kann das JSON via `fetch('api/neu?stufe=mittel')` erhalten und rendert das Puzzle korrekt (Ziffern an den richtigen `data-index`‑Feldern). | End‑2‑End‑Test im Browser (z. B. mit Playwright). |
| **A8** | Alle 81 Zellen besitzen das Attribut `data-index="0"` … `"80"` und zeigen die Zahl als Text (kein `<input>`). | DOM‑Inspection‑Test. |
| **A9** | Zahlen‑Buttons (`data-digit`) und Lösch‑Button funktionieren und ändern das selektierte Feld. | UI‑Test: Klick auf Button 5 → Feld enthält „5“, Klick auf Lösch‑Button → Feld wird leer. |
| **A10** | Schwierigkeits‑Buttons (`data-stufe`) starten sofort ein neues Puzzle mit der gewünschten Anzahl von Hinweisen. | Klick auf „leicht“ → `clues` = 38, usw. |
| **A11** | Tastatureingaben (1‑9, Pfeiltasten, Delete/Backspace) ändern das aktuell markierte Feld und bewegen die Auswahl wie spezifiziert. | Keyboard‑Interaction‑Test. |
| **A12** | Das aktuell ausgewählte Feld hat immer die CSS‑Klasse `selected` (oder analog) und ist visuell hervorgehoben. | Screenshot‑Vergleich / CSS‑Class‑Check. |
| **A13** | Konflikt‑Zellen besitzen die Klasse `konflikt`. | Eingabe einer falschen Zahl → betroffene Zellen erhalten Klasse. |
| **A14** | Nach korrekter Lösung erhält `<body>` die Klasse `geloest`. | Vollständiges Puzzle lösen → Klasse vorhanden. |
| **A15** | `test_spiel.py` läuft ohne Fehler (Exit‑Code 0) bei korrekter Implementierung und bricht mit einem Nicht‑0‑Code bei jedem Fehlverhalten ab. | Ausführen des Tests in CI‑Pipeline. |

---  

## 3. Vertrag  

> **Vertrag**  
> 
> - `engine.py` nutzt nur die Python-Standardbibliothek.  
> - `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
> - `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. `puzzle` und `solution` sind Listen mit 81 Zahlen, 0 steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in puzzle und gleich `CLUES[level]`.  
> - `solutions(puzzle, limit)` liefert eine Liste mit höchstens `limit` Lösungen.  
> - `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
> - `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
> - `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
> - Bedienvertrag der Oberfläche: Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein input). Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `"9"`, der Löschen‑Button trägt `data-digit="0"`. Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel. Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet. Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben. Die 3×3‑Blöcke sind durch dickere Linien oder größere Abstände erkennbar. Felder im Konflikt tragen die Klasse `konflikt`. Ist das Rätsel richtig gelöst, trägt `body` die Klasse `geloest`.  
> - `test_spiel.py` läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit‑Code ungleich 0.  

---  

*Ende der Spezifikation.*