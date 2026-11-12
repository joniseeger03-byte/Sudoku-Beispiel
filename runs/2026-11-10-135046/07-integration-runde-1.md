# Integrationsbericht

## Was war kaputt
Nichts. Ich habe `board.js`, `index.html` und `style.css` gegen den Vertrag gelesen und keinen Bruch zwischen Oberfläche und Engine gefunden.

- **Leeres Feld:** Die Engine liefert `0` für leer. `board.js` wertet `0` als leer und zeigt dann keinen Text an. Das passt zusammen.
- **Markup:** Die Felder sind `div` mit `data-index` 0–80. Die Ziffernknöpfe tragen `data-digit` 0–9 und die Stufenknöpfe `data-stufe`. `keydown` hängt am `document`.
- **Klassen:** Die Klassen `selected`, `konflikt` und `geloest` sind in `style.css` vorhanden. Das Banner „Richtig!“ erscheint über `body.geloest`.
- **Abruf:** `board.js` holt das Rätsel mit `fetch('api/neu?stufe=…')`, relativ zur Seite.

## Was ich geändert habe
Keine Dateien. `test_spiel.py` und `engine.py` blieben unberührt, ebenso die Rechenheft-Gestaltung.

## Prüfung
- `python ../../../../orchestrator/ui_check.py .`: alle 26 Prüfungen OK. Dazu gehören 81 Felder, Auswahl, Klick-, Tastatur-, Lösch- und Pfeiltasteneingabe, Vorgabenschutz und Konflikt-Markierung. Außerdem die drei Stufen, die Herkunft des Rätsels aus der Engine und die Sieg-Erkennung.
- `python test_spiel.py`: A1, A2 und A3 OK.

## Nicht geprüft
Diese Punkte der Spezifikation deckt keine der beiden Prüfungen ab, ich habe sie nur im Code gelesen:
- Undo
- Timer
- Notizen-Modus
- das Aussehen im Detail