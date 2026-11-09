# Spezifikation: Sudoku fürs Web

## Entscheidungen
- Hinweise: leicht 38, mittel 32, schwer 26.
- Konflikte werden sofort markiert. Notizen und Tipps folgen später.

## Vertrag
- engine.py nutzt nur die Python-Standardbibliothek.
- `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.
- `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. 0 steht für leer.
- `solutions(puzzle, limit)` liefert eine Liste mit höchstens limit Lösungen.
- `conflicts(grid)` liefert ein Set der Indizes, die in Konflikt stehen.
- `python engine.py neu <stufe>` gibt das Ergebnis von generate als JSON aus.
- board.js holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`.
- Bedienvertrag der Oberfläche: Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein input). Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `"9"`. Tastatureingaben werden über keydown auf document verarbeitet. Felder im Konflikt tragen die Klasse `konflikt`.
- test_spiel.py endet bei einem Fehler mit Exit-Code ungleich 0.

## Abnahmekriterien
| ID | Kriterium |
|---|---|
| A1 | Lösungsgitter sind gültig |
| A2 | Jedes Rätsel hat genau eine Lösung |
| A3 | Die Hinweiszahl passt zum Schwierigkeitsgrad |
| A4 | Konflikte werden erkannt |
| A5 | Das Rätsel führt zur hinterlegten Lösung |
| A6 | Ein Rätsel entsteht in unter 5 Sekunden |

Aufteilung: `engine`, `ui` und `tests` berühren getrennte Dateien und dürfen parallel laufen.
