Mache aus Auftrag, Recherche und Prüfung eine knappe Spezifikation in Markdown mit nummerierten Abnahmekriterien (A1, A2, …).
Berücksichtige die Einwände der Prüfung.
Übernimm den folgenden Vertrag unverändert in einen Abschnitt „Vertrag“:

- engine.py nutzt nur die Python-Standardbibliothek.
- `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.
- `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. puzzle und solution sind Listen mit 81 Zahlen, 0 steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in puzzle und gleich `CLUES[level]`.
- `solutions(puzzle, limit)` liefert eine Liste mit höchstens limit Lösungen.
- `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.
- `python engine.py neu <stufe>` gibt das Ergebnis von generate als JSON aus.
- index.html, board.js und style.css bilden die Oberfläche im Browser. board.js holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.
- test_spiel.py läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit-Code ungleich 0.
