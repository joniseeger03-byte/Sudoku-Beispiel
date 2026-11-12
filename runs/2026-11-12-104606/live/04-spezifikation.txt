**Spezifikation – Sudoku‑Webapp**  
*(Kurz und knapp, alle Vorgaben aus Auftrag, Recherche & Prüfung berücksichtigt)*  

---  

## 1. Überblick  
Die Anwendung besteht ausschließlich aus Front‑End‑Dateien (`index.html`, `board.js`, `style.css`) und einer reinen Python‑Engine (`engine.py`).  
Sie liefert pro Anforderung ein Sudoku‑Rätsel mit exakt einer Lösung, markiert Konflikte in Echtzeit und signalisiert die Vollständigkeit.

---

## 2. Technische Anforderungen  

| Bereich | Anforderung | Hinweis |
|---------|-------------|--------|
| **Engine** | Nur Python‑Standardbibliothek benutzen. | `engine.py` enthält keine externen Pakete. |
| **Hinweis‑Zahl** | `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` | Gibt die erwartete Anzahl gefüllter Felder im Ausgangsrätsel an. |
| **Generator** | `generate(level)` → `dict` mit Schlüsseln `puzzle`, `solution`, `clues`, `level`. <br> * `puzzle` & `solution`: Listen mit 81 Zahlen (0 = leer). <br> * `clues` = Anzahl von Nicht‑0‑Einträgen in `puzzle` **und** muss `CLUES[level]` entsprechen. | Garantiert eindeutige Lösung (Backtracking‑Eindeutigkeitstest). |
| **Löser** | `solutions(puzzle, limit)` → Liste ≤ `limit` Lösungen. | Wird intern für Eindeutigkeitsprüfung verwendet. |
| **Konflikt‑Erkennung** | `conflicts(grid)` → `set` von Indizes (0‑80) die in Zeile/Spalte/Block kollidieren. | Wird nach jeder Eingabe aufgerufen. |
| **CLI** | `python engine.py neu <stufe>` gibt das JSON von `generate` auf `stdout`. | Wird von `board.js` per `fetch` abgefragt. |
| **Frontend** | `index.html`, `board.js`, `style.css` bilden die UI. <br> `board.js` holt Rätsel via `fetch('api/neu?stufe=mittel')`. | Relative Pfadangabe, kein Server‑Side nötig. |
| **UI‑Elemente** | *Zellen* → `<div data-index="0" …>` (81 Stück). <br> *Ziffern‑Buttons* → `data-digit="1"` … `data-digit="9"`, Lösch‑Button `data-digit="0"`. <br> *Schwierigkeits‑Buttons* → `data-stufe="leicht|mittel|schwer"`. | Keine `<input>`‑Felder, Textinhalt ist die Ziffer. |
| **Eingabe** | Keyboard → `keydown` auf `document` (1‑9, Pfeile, Entf/Backspace). <br> Touch → Klick auf Ziffern‑Button. | Das aktuell gewählte Feld erhält eigene CSS‑Klasse (`selected`). |
| **Visuals** | 3×3‑Blöcke erkennbar durch dickere Linien/Abstände. <br> Konflikt‑Zellen erhalten Klasse `konflikt`. <br> Bei vollständiger, korrekter Lösung: `<body class="geloest">`. |
| **Tests** | `test_spiel.py` läuft via `python test_spiel.py`. <br> Bei irgendeinem Fehler beendet sich das Skript mit Exit‑Code ≠ 0. | CI‑freundlich. |

---

## 3. Akzeptanzkriterien  

| Kriterium | Beschreibung | Prüfung |
|-----------|--------------|--------|
| **A1 – Engine‑Unabhängigkeit** | `engine.py` importiert ausschließlich Module aus der Python‑Standardbibliothek. | `import ast; assert not any(m.module not in stdlib for m in ast.parse(open('engine.py').read()).body if isinstance(m, ast.Import))` |
| **A2 – Richtige Hinweis‑Zahl** | `generate(level)` liefert `clues == CLUES[level]`. | Test‑assert in `test_spiel.py`. |
| **A3 – Eindeutige Lösung** | `solutions(puzzle, 2)` gibt **maximal** eine Lösung. | `len(solutions(puzzle,2)) == 1`. |
| **A4 – Korrektes JSON‑CLI** | `python engine.py neu mittel` gibt ein gültiges JSON‑Objekt mit allen geforderten Feldern. | `json.loads(output)` succeeds & keys present. |
| **A5 – UI‑Element‑Struktur** | Im gerenderten DOM existieren 81 Elemente mit `data-index="0"`‑`"80"` und 9 Ziffern‑Buttons (`data-digit`). | Selenium / Playwright‑Check. |
| **A6 – Eingabe‑Handling** | Tastendruck `5` in ausgewählter Zelle schreibt die Ziffer, `Entf` löscht sie; Konflikt‑Klasse wird korrekt gesetzt/entfernt. | Simulierter `keydown` + DOM‑Inspect. |
| **A7 – Konflikt‑Markierung** | Nach einer falschen Eingabe erhalten alle betroffenen Zellen die Klasse `konflikt`. | `conflicts(grid)` Ergebnis ≡ DOM‑Klassen. |
| **A8 – Schwierigkeits‑Buttons** | Klick auf Button `data-stufe="schwer"` löst `fetch('api/neu?stufe=schwer')` aus und rendert neues Rätsel. | Netzwerk‑Mock + DOM‑Update. |
| **A9 – Lösungs‑Erkennung** | Sobald das Raster exakt der `solution` entspricht, erhält `<body>` die Klasse `geloest`. | Vergleich `grid == solution`. |
| **A10 – Test‑Exit‑Code** | `python test_spiel.py` beendet mit Code 0 bei Erfolg, ≠0 bei Fehler. | CI‑Pipeline prüft Rückgabewert. |

---

## 4. Vertrag  

```markdown
**Vertrag**

- `engine.py` nutzt nur die Python‑Standardbibliothek.  
- `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
- `generate(level)` liefert ein `dict` mit `puzzle`, `solution`, `clues` und `level`.  
  - `puzzle` und `solution` sind Listen mit 81 Zahlen, `0` steht für leer.  
  - `clues` ist die Anzahl der Zahlen ≠ 0 in `puzzle` und muss `CLUES[level]` entsprechen.  
- `solutions(puzzle, limit)` liefert eine Liste mit höchstens `limit` Lösungen.  
- `conflicts(grid)` liefert ein `set` der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
- `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
- `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser.  
  - `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
- Bedienvertrag der Oberfläche:  
  - Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein `<input>`).  
  - Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `data-digit="9"`, der Löschen‑Button trägt `data-digit="0"`.  
  - Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel.  
  - Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet.  
  - Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben.  
  - Die 3×3‑Blöcke sind durch dickere Linien oder größere Abstände erkennbar.  
  - Felder im Konflikt tragen die Klasse `konflikt`.  
  - Ist das Rätsel richtig gelöst, trägt `body` die Klasse `geloest`.  
- `test_spiel.py` läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit‑Code ungleich 0.  
```

---

## 5. Hinweis zu den Prüfungseinwänden  

* **Schwierigkeitsdefinition** – Für das Minimal‑MVP wird die Hinweis‑Zahl (`CLUES`) als pragmatischer Proxy verwendet (wie in der Prüfung akzeptiert).  
* **Performance** – Der Generator führt nach jedem Entfernen einen Backtracking‑Eindeutigkeitstest aus; bei Bedarf können spätere Optimierungen (Constraint‑Propagation, Heuristiken) ergänzt werden.  

---  

**Ende der Spezifikation**.