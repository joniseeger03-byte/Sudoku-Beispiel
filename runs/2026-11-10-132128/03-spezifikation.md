## Spezifikation – Sudoku‑Web‑App  

**Ziel**  
Implementiere ein vollständig spielbares Sudoku im Browser – ohne serverseitiges Backend – gemäß den Anforderungen (Auftrag, Recherche, Prüfung).  

---

### 1. Funktionsumfang  

| # | Beschreibung |
|---|--------------|
| **F1** | Drei Schwierigkeitsstufen **leicht**, **mittel**, **schwer** mit vorgegebenen Hinweiszahlen `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}`. |
| **F2** | Generierung eines gültigen Sudoku‑Rätsels mit **genau einer Lösung**. Die Generierung muss nach jedem Entfernen einer Zahl prüfen, ob das Rätsel weiterhin eindeutig ist (zwei‑mal‑Backtrack‑Prinzip). |
| **F3** | Front‑End besteht aus `index.html`, `board.js` und `style.css`. Keine weitere Bibliothek wird verwendet (nur native JS/HTML/CSS). |
| **F4** | Jeder der 81 Zellen ist ein Element mit Attribut `data-index="0"` … `data-index="80"`. Der aktuelle Zell‑Fokus wird durch eine eigene CSS‑Klasse (z. B. `focus`) hervorgehoben. |
| **F5** | Eingabe über: <br>• **Tastatur** (Ziffern 1‑9, `Entf`/`Backspace` → Löschen, Pfeiltasten → Navigation). <br>• **Touch** über ein numerisches Overlay, das Buttons mit `data-digit="1"` … `data-digit="9"` und einen Löschen‑Button `data-digit="0"` enthält. |
| **F6** | Drei Buttons `data-stufe="leicht"`, `data-stufe="mittel"`, `data-stufe="schwer"` starten sofort ein neues Rätsel (API‑Aufruf `fetch('api/neu?stufe=…')`). |
| **F7** | Konflikt­erkennung in Echtzeit: nach jeder Eingabe wird `conflicts(grid)` aufgerufen. Alle betroffenen Indizes erhalten die CSS‑Klasse `konflikt`. |
| **F8** | Wenn das komplette Puzzle korrekt ausgefüllt ist (keine Konflikte, Anzahl gefüllter Zellen = 81), erhält das `<body>` die Klasse `geloest`. |
| **F9** | Der CLI‑Befehl `python engine.py neu <stufe>` gibt das aktuelle Rätsel als **JSON** aus, das exakt das von `board.js` erwartete Format (`puzzle`, `solution`, `clues`, `level`). |
| **F10** | Unit‑Tests in `test_spiel.py` laufen mit `python test_spiel.py`. Jeder fehlgeschlagene Test beendet das Skript mit einem Exit‑Code ≠ 0. |

---

### 2. Technische Details (Engine)

| Funktion | Signatur | Erwartetes Verhalten |
|----------|----------|----------------------|
| `generate(level)` | `level ∈ {"leicht","mittel","schwer"}` → `dict` | Liefert ein Dict mit den Schlüsseln `puzzle` (Liste 81, 0 = leer), `solution` (vollständige Liste 81), `clues` (Anzahl gefüllter Felder, muss `CLUES[level]` entsprechen) und `level`. Das erzeugte Rätsel hat **genau eine Lösung**. |
| `solutions(puzzle, limit)` | `puzzle: list[int]`, `limit: int` → `list[dict]` | Gibt bis zu `limit` vollständige Lösungen zurück. Wird intern von `generate` für die Eindeutigkeitsprüfung verwendet. |
| `conflicts(grid)` | `grid: list[int]` → `set[int]` | Liefert die Menge aller Indizes, die in ihrer Zeile, Spalte oder 3×3‑Block mindestens eine gleiche Zahl wie ein anderes Feld besitzen. |
| CLI | `python engine.py neu <stufe>` | Gibt das JSON‑Objekt von `generate(level)` auf `stdout`. |

*Hinweis:* Die Engine nutzt **ausschließlich** die Python‑Standardbibliothek.

---

### 3. Akzeptanzkriterien  

| Kriterium | Beschreibung | Erfolgskriterium |
|-----------|--------------|------------------|
| **A1** | **Einzigartige Lösung** – `generate(level)` muss nach dem Entfernen jeder Zahl prüfen, dass `solutions(puzzle, 2)` **maximal ein** Ergebnis liefert. | Der Test `assert len(solutions(puzzle, 2)) == 1` für jedes erzeugte Rätsel besteht. |
| **A2** | **Hinweiszahl** – Das Feld `clues` im Ergebnis entspricht exakt `CLUES[level]`. | `assert result["clues"] == CLUES[level]`. |
| **A3** | **CLI‑Ausgabe** – Der Befehl `python engine.py neu mittel` liefert gültiges JSON, das `puzzle`, `solution`, `clues` und `level` enthält. | `json.loads(output)` liefert ein Dictionary mit allen Schlüsseln und korrekten Typen. |
| **A4** | **Frontend‑Render** – `board.js` erzeugt 81 Zellen mit `data-index="0"` … `"80"` und zeigt die Anfangszahlen korrekt an. | Visueller Test + DOM‑Abfrage `document.querySelectorAll('[data-index]').length == 81`. |
| **A5** | **Eingabe‑Handling** – Tastatur‑ und Touch‑Eingaben ändern das `data-index`‑Element und aktualisieren das interne Grid. | Nach Drücken von `5` auf einem leeren Feld ist `cell.textContent == "5"` und das Grid‑Array an dieser Stelle = 5. |
| **A6** | **Konflikt‑Markierung** – Nach einer falschen Eingabe besitzen alle kollidierenden Zellen die Klasse `konflikt`. | `document.querySelectorAll('.konflikt').length > 0` exakt für die erwarteten Indizes. |
| **A7** | **Lösungs‑Erkennung** – Bei vollständig korrekter Lösung wird `<body>` mit `class="geloest"` versehen. | `document.body.classList.contains('geloest')` ist true, wenn keine Konflikte mehr existieren und alle 81 Felder ≠ 0 sind. |
| **A8** | **Stufen‑Buttons** – Klick auf einen Button mit `data-stufe="schwer"` startet sofort ein neues Rätsel (neuer API‑Call, UI‑Refresh). | Netzwerk‑Request `api/neu?stufe=schwer` wird gesendet, UI zeigt neues Puzzle. |
| **A9** | **Test‑Suite** – `test_spiel.py` enthält mindestens: <br>• Test für eindeutige Lösung, <br>• Test für korrekte Hinweiszahl, <br>• Test für Konflikt‑Erkennung, <br>• Test für CLI‑JSON. | `python test_spiel.py` beendet mit Exit‑Code 0. |
| **A10** | **Prüfungs‑Einwand‑Berücksichtigung** – Die Implementierung verwendet das *zwei‑mal‑Backtrack‑Prinzip* (Suche nach zweiter Lösung), um den in 02‑pruefung.md genannten Einwand zu adressieren. | Code‑Kommentar und Unit‑Test (siehe A1) belegen die doppelte Prüfung. |

---

### 4. Vertrag  

> - `engine.py` nutzt nur die Python‑Standardbibliothek.  
> - `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
> - `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. `puzzle` und `solution` sind Listen mit 81 Zahlen, `0` steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in `puzzle` und gleich `CLUES[level]`.  
> - `solutions(puzzle, limit)` liefert eine Liste mit höchstens *limit* Lösungen.  
> - `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
> - `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
> - `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
> - Bedienvertrag der Oberfläche: Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein input). Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `data-digit="9"`, der Löschen‑Button trägt `data-digit="0"`. Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel. Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet. Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben. Die 3×3‑Blöcke sind durch dickere Linien oder größere Abstände erkennbar. Felder im Konflikt tragen die Klasse `konflikt`. Ist das Rätsel richtig gelöst, trägt `body` die Klasse `geloest`.  
> - `test_spiel.py` läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit‑Code ungleich 0.  

---  

**Hinweis:** Die oben genannten Akzeptanzkriterien bilden die Grundlage für das Abnahme‑Testing. Sie decken sämtliche in Auftrag, Recherche und Prüfung identifizierten Anforderungen sowie die im Vertrag festgelegten Schnittstellen ab.