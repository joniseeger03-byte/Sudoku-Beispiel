**Spezifikation – Sudoku‑Spiel für den Browser**  
*(Kurzfassung aus Auftrag, Recherche und Prüfung)*  

---  

## 1. Ziel  
Ein vollständig spielbares Sudoku‑Web‑App ohne serverseitiges Backend.  

* drei Schwierigkeitsgrade (leicht, mittel, schwer)  
* Eingabe per Tastatur, Maus und Touch  
* jedes Rätsel besitzt **genau eine** Lösung  
* Konflikte werden visuell markiert  

---  

## 2. Technische Grundlagen  

| Komponente | Beschreibung |
|------------|--------------|
| **engine.py** | Python‑Modul, benutzt **nur** die Standardbibliothek. |
| `CLUES` | `{"leicht": 38, "mittel": 32, "schwer": 26}` – Anzahl vorgegebener Zahlen pro Schwierigkeitsgrad. |
| `generate(level)` | Liefert ein `dict` mit den Keys `puzzle`, `solution`, `clues`, `level`. <br>`puzzle` und `solution` sind Listen von 81 Zahlen (0 = leer). <br>`clues` = Anzahl non‑zero‑Einträge in `puzzle` und muss `CLUES[level]` entsprechen. |
| `solutions(puzzle, limit)` | Gibt bis zu `limit` verschiedene Lösungen zurück (Liste von 81‑Zahlen‑Listen). |
| `conflicts(grid)` | Liefert ein `set` von Indizes (0‑80), die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren. |
| **CLI** | `python engine.py neu <stufe>` → gibt das JSON‑Ergebnis von `generate` aus. |
| **Frontend** | `index.html`, `board.js`, `style.css` bilden die UI. |
| **API‑Aufruf** | `board.js` ruft `fetch('api/neu?stufe=mittel')` (relativ zur Seite) und erwartet das gleiche JSON‑Format wie oben. |

---  

## 3. UI‑Verhalten  

* **Zellen** – jedes der 81 Felder ist ein HTML‑Element mit `data-index="0"` … `"80"`. Der aktuelle Inhalt (Zahl 1‑9 oder leer) steht als reiner Text (kein `<input>`).  
* **Digit‑Buttons** – 9 Buttons mit `data-digit="1"` … `"9"` und ein Löschen‑Button `data-digit="0"`.  
* **Stufen‑Buttons** – drei Buttons `data-stufe="leicht"`, `data-stufe="mittel"`, `data-stufe="schwer"` starten sofort ein neues Rätsel.  
* **Tastatur** – `keydown` auf `document` verarbeitet:  
  * Ziffern 1‑9 → Eingabe in das aktuell markierte Feld  
  * `Backspace` / `Delete` → Löschen (entspricht `data-digit="0"` )  
  * Pfeiltasten → Navigation zum nächsten Feld (Klasse `ausgewaehlt` hält das markierte Feld)  
* **Visuelle Markierungen**  
  * Aktive Zelle → eigene CSS‑Klasse (z. B. `ausgewaehlt`).  
  * 3×3‑Blöcke → durch dickere Linien bzw. größere Abstände erkennbar.  
  * Konfliktfelder → Klasse `konflikt`.  
  * Vollständig gelöstes Rätsel → `<body>` bekommt Klasse `geloest`.  
* **Touch** – gleiche Logik wie Maus‑Klicks; Buttons und Zellen reagieren auf `touchstart`.  

---  

## 4. Test‑ und Qualitätsanforderungen  

* `test_spiel.py` wird mit `python test_spiel.py` ausgeführt. Jeder fehlgeschlagene Test muss den Prozess mit einem **Exit‑Code ≠ 0** beenden.  

---  

## 5. Abnahmekriterien  

| Kriterium | Beschreibung | Prüfung |
|-----------|--------------|--------|
| **A1 – Engine‑Konformität** | `engine.py` nutzt ausschließlich die Python‑Standardbibliothek und liefert die geforderten Funktionen (`generate`, `solutions`, `conflicts`). | Unit‑Tests importieren das Modul und prüfen `import`‑Fehler sowie Funktionssignaturen. |
| **A2 – Klare Hinweis‑Zahl** | Für jede Stufe liefert `generate(level)` exakt die in `CLUES` definierte Anzahl von Hinweisen. | Test vergleicht `len([x for x in puzzle if x!=0])` mit `CLUES[level]`. |
| **A3 – Eindeutige Lösung** | `solutions(puzzle, 2)` liefert **höchstens** ein Ergebnis (also exakt 1 Lösung). | Aufruf mit `limit=2` muss Liste mit Länge 1 zurückgeben. |
| **A4 – Konflikt‑Erkennung** | `conflicts(grid)` enthält exakt die Indizes, die regelwidrig sind. | Vergleich mit manueller Berechnung für ausgewählte Test‑Grids. |
| **A5 – CLI‑Ausgabe** | `python engine.py neu mittel` gibt ein gültiges JSON‑Objekt mit den Keys `puzzle`, `solution`, `clues`, `level` aus. | Test prüft JSON‑Parsebarkeit und Feld‑Vorhandensein. |
| **A6 – API‑Aufruf** | `board.js` ruft `api/neu?stufe=...` korrekt und verarbeitet das zurückgelieferte JSON. | Integrationstest mit `fetch‑mock` prüft, dass `generate`‑Ergebnis im UI erscheint. |
| **A7 – DOM‑Struktur** | Jede Zelle besitzt das Attribut `data-index` von 0‑80, die Zahl wird als Textknoten dargestellt. | Selenium‑/Playwright‑Test sucht nach allen `[data-index]` und prüft Text‑Inhalt. |
| **A8 – Eingabe‑Handling** | Tastatur‑ und Button‑Eingaben setzen bzw. löschen Zahlen im markierten Feld, ohne vorgegebene Felder zu überschreiben. | Simulierte `keydown`‑ und Klick‑Events prüfen Grid‑State. |
| **A9 – Konflikt‑Highlight** | Nach jeder Eingabe erhalten alle konflikt‑betroffenen Zellen die CSS‑Klasse `konflikt`. | Test prüft DOM‑Klassen nach einer absichtlichen Regelverletzung. |
| **A10 – Lösungs‑Erkennung** | Sobald das Puzzle korrekt gelöst ist, bekommt `<body>` die Klasse `geloest`. | Vollständiges, korrekte Lösungseingabe → Klassen‑Check. |
| **A11 – Test‑Exit‑Code** | `test_spiel.py` beendet sich mit Exit‑Code 0 bei Erfolg und ≠ 0 bei jedem Fehler. | Ausführung via CI‑Pipeline prüft Rückgabecode. |
| **A12 – Vertrag‑Integrität** | Der Abschnitt **„Vertrag“** (unten) ist unverändert in die Spezifikation eingefügt. | Text‑Diff‑Check gegen Original‑Vertrag. |

---  

## 6. Vertrag  

> **Vertrag**  
> 
> - `engine.py` nutzt nur die Python-Standardbibliothek.  
> - `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
> - `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. `puzzle` und `solution` sind Listen mit 81 Zahlen, 0 steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in `puzzle` und gleich `CLUES[level]`.  
> - `solutions(puzzle, limit)` liefert eine Liste mit höchstens *limit* Lösungen.  
> - `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
> - `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
> - `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
> - **Bedienvertrag der Oberfläche:** Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein input). Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `data-digit="9"`, der Löschen‑Button trägt `data-digit="0"`. Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel. Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet. Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben. Die 3×3‑Blöcke sind durch dickere Linien oder größere Abstände erkennbar. Felder im Konflikt tragen die Klasse `konflikt`. Ist das Rätsel richtig gelöst, trägt `body` die Klasse `geloest`.  
> - `test_spiel.py` läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit‑Code ungleich 0.  