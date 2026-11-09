Du bist der Oberflächen-Agent in einem Team, das ein Browser-Sudoku baut.
Setze aus der Spezifikation unten nur index.html, board.js und style.css um. engine.py schreibt ein anderer Agent, nutze nur den vereinbarten Vertrag.

Das Spiel muss sich von Hand spielen lassen:

- board.js holt ein Rätsel mit `fetch('api/neu?stufe=' + stufe)`, relativ zur Seite. Leere Felder haben in `puzzle` den Wert 0.
- Ein Klick wählt ein Feld aus, auch ein vorgegebenes. Das gewählte Feld bleibt über eine eigene Klasse deutlich hervorgehoben, bis ein anderes gewählt wird. Verlasse dich nicht auf `:focus` oder `:hover`.
- Eingabe per Tastatur (1–9, Pfeiltasten, Entf und Rücktaste) und per Klick oder Touch über das Ziffernfeld mit eigenem Löschen-Button.
- Drei Stufen-Buttons starten sofort ein neues Rätsel.
- Vorgegebene Zahlen sind nicht änderbar und sehen anders aus als eigene Eingaben. Konflikte in Zeile, Spalte und Block werden sofort markiert und verschwinden, sobald sie behoben sind.
- Die 3×3-Blöcke sind durch dickere Linien oder größere Abstände an den Feldern oder einer Block-Hülle klar erkennbar.
- Ein richtig gelöstes Rätsel zeigt eine sichtbare Siegmeldung. Das Brett passt auch auf ein Smartphone.
- Halte den Bedienvertrag aus der Spezifikation exakt ein. Ein Skript spielt das Rätsel automatisch bis zum Sieg.
- Kein Framework, keine externen Dateien, keine externen Schriften.

Liegt eine Designrichtung bei, setze sie konsequent um: Farben, Schrift, Anordnung und Stimmung sollen unverkennbar sein. Der Bedienvertrag bleibt davon unberührt.

Antworte mit genau drei Codeblöcken in dieser Reihenfolge: ```html für index.html, ```javascript für board.js, ```css für style.css.
