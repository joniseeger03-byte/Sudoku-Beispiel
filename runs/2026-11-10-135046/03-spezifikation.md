## Spezifikation – Sudoku‑Web‑App  

### 1. Ziel  
Entwicklung einer komplett im Browser laufenden Sudoku‑Applikation, die über die vorgegebenen Schnittstellen (`engine.py`, HTML/JS/CSS) funktioniert und sämtliche Einwände aus der Prüfung berücksichtigt.

### 2. Kernfunktionen  

| # | Funktion | Beschreibung |
|---|----------|--------------|
| **F1** | **Generator** | `engine.py generate(level)` liefert ein Dict `{puzzle, solution, clues, level}` mit exakt `CLUES[level]` vorgegebenen Zahlen. |
| **F2** | **Solver** | `engine.py solutions(puzzle, limit)` liefert maximal `limit` vollständige Lösungen. |
| **F3** | **Konflikt‑Erkennung** | `engine.py conflicts(grid)` liefert ein Set von Indizes, die in Zeile, Spalte oder Block kollidieren. |
| **F4** | **API** | `python engine.py neu <stufe>` gibt das JSON‑Objekt aus **F1** aus. |
| **F5** | **Frontend‑Abruf** | `board.js` ruft per `fetch('api/neu?stufe=mittel')` das gleiche JSON ab. |
| **F6** | **Board‑Darstellung** | 81 Zellen → `<div data-index="0"> … </div>` … `<div data-index="80">`. Der Inhalt ist Text, kein `<input>`. |
| **F7** | **Eingabe** | Zahlen‑Buttons `data-digit="1"`‑`"9"` und Löschen‑Button `data-digit="0"`. Tastatur‑Eingaben (1‑9, Pfeile, Entf, Backspace) werden über `keydown` auf `document` verarbeitet. |
| **F8** | **Auswahl‑Highlight** | Das aktuell gewählte Feld erhält eine eigene CSS‑Klasse (z. B. `selected`). |
| **F9** | **Block‑Darstellung** | 3×3‑Blöcke sind durch dickere Linien / größere Abstände erkennbar. |
| **F10** | **Konflikt‑Markierung** | Zellen, die in `conflicts` vorkommen, erhalten die Klasse `konflikt`. |
| **F11** | **Lösungs‑Erkennung** | Ist das Puzzle gelöst, bekommt das `<body>` die Klasse `geloest`. |
| **F12** | **Schwierigkeitswahl** | Drei Buttons `data-stufe="leicht"`, `"mittel"`, `"schwer"` starten sofort ein neues Rätsel. |
| **F13** | **Test‑Runner** | `test_spiel.py` wird mit `python test_spiel.py` ausgeführt; jeder Fehltest beendet das Skript mit Exit‑Code ≠ 0. |

### 3. Nicht‑funktionale Anforderungen  

| # | Anforderung | Hinweis |
|---|-------------|--------|
| **N1** | **Nur Standard‑Bibliothek** | `engine.py` darf ausschließlich Module aus der Python‑Standardbibliothek nutzen. |
| **N2** | **Performance** | Generator‑ und Solver‑Algorithmen laufen im Browser (JS) bzw. in Python (CLI) performant genug für leicht/mittel; schwere Level dürfen ggf. länger benötigen, aber < 5 s. |
| **N3** | **Barrierefreiheit** | Vor‑gegebene Zahlen sind fett + andersfarbig; Konflikt‑Markierung erfolgt zusätzlich per rotem Rand, nicht nur Farbe. |
| **N4** | **Undo** | Mindestens 10 Schritte rückgängig machbar (Button + Strg+Z). |
| **N5** | **Timer (optional)** | Schalter im UI kann einen Spiel‑Timer aktivieren/deaktivieren. |
| **N6** | **Fehler‑Detailanzeige** | Bei Konflikt wird ein Tooltip / Pop‑Up mit genauer Meldung („Doppelte 5 in Zeile 3“) angezeigt. |
| **N7** | **Notizen‑Modus** | Umschalter `Notizen On/Off`; Eingaben im Notizen‑Modus fügen kleine Ziffern (1‑9) in die Zelle ein, nicht die eigentliche Zahl. |
| **N8** | **Responsive Layout** | UI funktioniert sowohl auf Desktop als auch auf Touch‑Geräten. |

### 4. Abnahmekriterien  

| Kriterium | Beschreibung | Prüfung |
|-----------|--------------|--------|
| **A1** | **Generator‑Output** – `engine.py generate(level)` liefert ein Dict mit Schlüsseln `puzzle`, `solution`, `clues`, `level`; `clues` = `CLUES[level]`. | Unit‑Test prüft Dict‑Struktur und `len([x for x in puzzle if x!=0]) == CLUES[level]`. |
| **A2** | **Eindeutige Lösung** – Für jedes erzeugte Rätsel gibt `solutions(puzzle, 2)` maximal **eine** Lösung zurück. | Test erzeugt 10 Rätsel pro Level, ruft `solutions(...,2)` und erwartet Länge ≤ 1. |
| **A3** | **CLI‑API** – `python engine.py neu mittel` gibt gültiges JSON aus, das exakt dem Dict aus **A1** entspricht. | `subprocess.run([...])` → JSON‑Parse, Feld‑Vergleich. |
| **A4** | **Frontend‑Abruf** – `board.js` erhält per `fetch('api/neu?stufe=leicht')` identisches JSON. | Mock‑Server, prüft Response‑Body gegen **A1**. |
| **A5** | **Board‑Markup** – 81 Zellen mit `data-index="0"`‑`"80"` existieren; Inhalt ist Text, nicht `<input>`. | Selenium‑Test prüft DOM‑Struktur. |
| **A6** | **Eingabe‑Mechanik** – Zahlen‑Buttons, Tastatur‑ und Pfeiltasten setzen/löschen Werte, Highlight bleibt korrekt. | Interaktionstest (Selenium/Playwright). |
| **A7** | **Konflikt‑Markierung** – Nach falscher Eingabe erhält die betroffene Zelle die Klasse `konflikt` und zeigt Tooltip mit genauer Fehlermeldung. | Test setzt doppelte Zahl, prüft Klasse & Tooltip‑Text. |
| **A8** | **Lösungs‑Erkennung** – Bei vollständig korrektem Raster erhält `<body>` die Klasse `geloest`. | Vollständiges, korrektes Puzzle einspielen, prüfen Klassen‑Zuweisung. |
| **A9** | **Undo‑Funktion** – Mindestens 10 Schritte rückgängig machbar über UI‑Button oder `Strg+Z`. | Eingaben tätigen, Undo ausführen, Zustand prüfen. |
| **A10** | **Timer‑Option** – Schalter aktiviert Timer, Anzeige läuft, kann gestoppt werden. | UI‑Test schaltet ein, prüft Zeit‑Anzeige. |
| **A11** | **Notizen‑Modus** – Bei aktivem Modus werden Eingaben als kleine Ziffern (Notizen) dargestellt, nicht als Hauptwert. | Modus aktivieren, Zahl eingeben, DOM‑Klassen/Content prüfen. |
| **A12** | **Barrierefreiheit** – Vor‑gegebene Zahlen besitzen fett‑Schrift und andere Farbe; Konflikte zusätzlich roter Rand. | CSS‑Prüfung (computed style). |
| **A13** | **Test‑Suite** – `test_spiel.py` läuft ohne Fehler; bei erstem Fehler beendet es mit Exit‑Code ≠ 0. | CI‑Run, prüfen Rückgabecode. |

### 5. Vertrag  

> **Vertrag**  
> - `engine.py` nutzt nur die Python‑Standardbibliothek.  
> - `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
> - `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. `puzzle` und `solution` sind Listen mit 81 Zahlen, 0 steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in `puzzle` und gleich `CLUES[level]`.  
> - `solutions(puzzle, limit)` liefert eine Liste mit höchstens `limit` Lösungen.  
> - `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
> - `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
> - `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
> - Bedienvertrag der Oberfläche: Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein input). Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `"9"`, der Löschen‑Button trägt `data-digit="0"`. Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel. Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet. Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben. Die 3×3‑Blöcke sind durch dickere Linien oder größere Abstände erkennbar. Felder im Konflikt tragen die Klasse `konflikt`. Ist das Rätsel richtig gelöst, trägt `body` die Klasse `geloest`.  
> - `test_spiel.py` läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit‑Code ungleich 0.  

--- 

*Ende der Spezifikation.*