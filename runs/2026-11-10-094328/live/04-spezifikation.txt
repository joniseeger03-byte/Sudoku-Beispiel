**Spezifikation – Sudoku für den Browser**  
*Stand: 2026‑11‑10*  

---  

## 1. Ziel  

Ein komplett clientseitiges Sudoku‑Spiel, das im Browser läuft und :

* drei Schwierigkeitsgrade (leicht, mittel, schwer) anbietet,  
* per Tastatur (1‑9, Pfeiltasten, Entf/Backspace) und Touch‑Eingabe bedienbar ist,  
* Konflikte in Echtzeit markiert,  
* die eindeutige Lösbarkeit jedes erzeugten Rätsels garantiert,  
* über eine minimalistische UI (HTML + CSS + JavaScript) verfügt,  
* über automatisierte Tests (`test_spiel.py`) verifiziert wird.  

---  

## 2. Funktionsumfang  

| Feature | Beschreibung |
|--------|--------------|
| **Generator** | `engine.py` erzeugt per `generate(level)` ein Sudoku‑Rätsel als JSON. Nur Standard‑Python‑Bibliothek wird benutzt. |
| **Löser / Uniqueness‑Check** | `solutions(puzzle, limit)` liefert bis zu `limit` gültige Lösungen. Wird intern genutzt, um die Eindeutigkeit zu prüfen. |
| **Konflikterkennung** | `conflicts(grid)` liefert ein `set` von Indizes (0‑80), die in Zeile, Spalte oder Block kollidieren. |
| **Web‑UI** | `index.html`, `board.js`, `style.css` bilden die Oberfläche. `board.js` ruft per `fetch('api/neu?stufe=mittel')` das JSON vom Engine‑Endpoint ab. |
| **Interaktion** | – jedes Feld ist ein Element `data-index="0"` … `data-index="80"` (Text, kein `<input>`). <br>– Ziffern‑Buttons `data-digit="1"` … `data-digit="9"`, Löschen‑Button `data-digit="0"`. <br>– Schwierigkeits‑Buttons `data-stufe="leicht|mittel|schwer"` starten ein neues Rätsel. <br>– Tastatureingaben (1‑9, Pfeiltasten, Entf, Rücktaste) über `keydown` auf `document`. |
| **Visuelles Feedback** | – ausgewähltes Feld bekommt eine extra CSS‑Klasse (z. B. `selected`). <br>– 3×3‑Blöcke sind durch dickere Linien bzw. Abstand erkennbar. <br>– Zellen im Konflikt erhalten die Klasse `konflikt`. <br>– Bei vollständig gelöstem Rätsel wird `body` die Klasse `geloest` erhalten. |
| **Test‑Suite** | `test_spiel.py` wird mit `python test_spiel.py` ausgeführt. Jeder Fehltest beendet das Skript mit einem Exit‑Code ≠ 0. |

---  

## 3. Technische Rahmenbedingungen  

* **Python‑Engine** – ausschließlich Standardbibliothek, keine externen Pakete.  
* **JSON‑Schnittstelle** – `engine.py neu <stufe>` schreibt das Ergebnis von `generate(level)` als JSON auf `stdout`.  
* **Frontend** – reine HTML/CSS/JS, keine Server‑Side‑Komponente.  
* **Kompatibilität** – aktuelle Versionen von Chrome, Firefox, Safari, Edge.  

---  

## 4. Abnahmekriterien  

| Kriterium | Beschreibung | Prüfmethode |
|----------|--------------|------------|
| **A1** | `engine.py` verwendet **nur** Module aus der Python‑Standardbibliothek. | Quellcode‑Audit (`import`‑Analyse). |
| **A2** | `CLUES` enthält exakt die Werte `{ "leicht": 38, "mittel": 32, "schwer": 26 }`. | Unit‑Test: `assert CLUES["leicht"] == 38` etc. |
| **A3** | `generate(level)` liefert ein Dict mit Schlüsseln `puzzle`, `solution`, `clues`, `level`; `puzzle` und `solution` sind Listen mit 81 Integers (0 = leer). | Unit‑Test auf Rückgabe‑Struktur und Länge. |
| **A4** | Die Anzahl nicht‑null‑Einträge in `puzzle` entspricht `CLUES[level]`. | `assert sum(1 for v in result["puzzle"] if v != 0) == CLUES[level]`. |
| **A5** | `solutions(puzzle, limit)` gibt **maximal** `limit` gültige Lösungen zurück und liefert **mindestens** eine Lösung, wenn das Puzzle lösbar ist. | Property‑Based‑Test mit verschiedener `limit`. |
| **A6** | `conflicts(grid)` liefert exakt die Indizes, die regelwidrig sind (gleiche Ziffer in Zeile, Spalte oder Block). | Vergleich mit einer Referenz‑Implementierung. |
| **A7** | `python engine.py neu <stufe>` gibt korrektes JSON (Schema aus A3) auf `stdout` aus. | Integrationstest: Prozess‑Aufruf, JSON‑Parse. |
| **A8** | `board.js` ruft das JSON über `fetch('api/neu?stufe=mittel')` ab und rendert das Raster ohne Fehlermeldungen. | End‑to‑End‑Test im Headless‑Browser (z. B. Playwright). |
| **A9** | Jede Zelle besitzt das Attribut `data-index="0"` … `"80"` und zeigt die aktuelle Ziffer als Text‑Content. | DOM‑Query‑Test. |
| **A10** | Ziffern‑Buttons besitzen `data-digit="1"` … `"9"`; Löschen‑Button `data-digit="0"`. | DOM‑Query‑Test. |
| **A11** | Schwierigkeits‑Buttons besitzen `data-stufe="leicht|mittel|schwer"` und starten sofort ein neues Rätsel. | Klick‑Simulation + Prüfung neuer Puzzle‑Daten. |
| **A12** | Tastatur‑Events (1‑9, Pfeiltasten, Entf/Backspace) ändern das selektierte Feld und markieren Konflikte über `conflicts`. | Simulierte `keydown`‑Events, anschließend Prüfung der Klassen `selected` und `konflikt`. |
| **A13** | Konflikt‑Zellen erhalten die CSS‑Klasse `konflikt`; bei korrekter Lösung erhält `body` die Klasse `geloest`. | Sichtbarkeits‑ und Klassentest nach vollständiger Lösung. |
| **A14** | 3×3‑Blöcke sind optisch erkennbar (z. B. dickere Rahmen). | Visueller Regressionstest (Screenshot‑Vergleich). |
| **A15** | `test_spiel.py` läuft ohne Fehler; bei erstem Fehler beendet es mit Exit‑Code ≠ 0. | Ausführen des Test‑Scripts und prüfen des Rückgabecodes. |
| **A16** | Performance‑Grenze: Generierung eines „schwer“ Rätsels (26 Clues) dauert ≤ 2 s auf einem durchschnittlichen Laptop (Intel i5‑ oder vergleichbar). | Zeitmessung im Unit‑Test. |

---  

## 5. Annahmen & Einschränkungen  

* Der Generator garantiert **eindeutige** Lösungen durch wiederholtes Aufrufen von `solutions(..., limit=2)` während des Entfernens von Ziffern.  
* Der Schwierigkeitsgrad wird ausschließlich über die Anzahl vorgegebener Ziffern (`CLUES`) definiert – weitere Logik‑Schritte werden nicht gemessen.  
* Keine serverseitige Persistenz; das Spiel startet jedes Mal mit einem neu generierten Puzzle.  

---  

## 6. Vertrag  

> - `engine.py` nutzt nur die Python-Standardbibliothek.  
> - `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
> - `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. `puzzle` und `solution` sind Listen mit 81 Zahlen, 0 steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in `puzzle` und gleich `CLUES[level]`.  
> - `solutions(puzzle, limit)` liefert eine Liste mit höchstens `limit` Lösungen.  
> - `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
> - `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
> - `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
> - Bedienvertrag der Oberfläche: Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein input). Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `"9"`, der Löschen-Button trägt `data-digit="0"`. Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel. Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet. Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben. Die 3×3-Blöcke sind durch dickere Linien oder größere Abstände erkennbar. Felder im Konflikt tragen die Klasse `konflikt`. Ist das Rätsel richtig gelöst, trägt `body` die Klasse `geloest`.  
> - `test_spiel.py` läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit-Code ungleich 0.  

---  

*Ende der Spezifikation.*