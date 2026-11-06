Du bist der Oberflächen-Agent in einem Team, das ein Browser-Sudoku baut.
Setze aus der Spezifikation unten nur index.html, board.js und style.css um. engine.py schreibt ein anderer Agent, nutze nur den vereinbarten Vertrag.

- board.js holt ein Rätsel mit `fetch('api/neu?stufe=' + stufe)`, relativ zur Seite.
- Auswahl des Schwierigkeitsgrads, Eingabe per Tastatur (1–9, Pfeiltasten, Entf) und per Touch über ein Ziffernfeld.
- Vorgegebene Zahlen sind nicht änderbar. Konflikte in Zeile, Spalte und Block werden sofort markiert.
- Kein Framework, keine externen Dateien.

Antworte mit genau drei Codeblöcken in dieser Reihenfolge: ```html für index.html, ```javascript für board.js, ```css für style.css.
