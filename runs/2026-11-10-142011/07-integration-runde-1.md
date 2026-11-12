# Integrationsbericht

**Was war kaputt:** Nichts, das die Abnahme gefunden hat. Die Oberfläche und die Engine passen zusammen. Ein leeres Feld (`0` in der Engine) wird in `board.js` als leerer Text dargestellt (`v ? String(v) : ''`). Auch das Löschen mit `0` setzt das Feld wieder leer. `index.html` und `board.js` stimmen bei allen Vertragsattributen überein: `data-index`, `data-digit` 0–9, `data-stufe`, `data-hint` und `data-show-solution`. Die Klassen `selected`, `konflikt`, `vorgegeben` und `geloest` sowie der `keydown`-Handler auf `document` sind ebenfalls vorhanden.

**Was ich geändert habe:** Nichts. Ich habe keine Datei angefasst. Das Herbarium-Design blieb unverändert.

**Prüfung:**
- `python ../../../orchestrator/ui_check.py .` lief in allen 26 Prüfpunkten ohne Fehler durch. Dazu gehören Konflikt markieren und wieder entfernen, Tastatur-, Klick- und Löschen-Eingabe, Pfeiltasten, geschützte Vorgaben, alle drei Stufen und die Siegerkennung.
- `python test_spiel.py` meldet "Alle Tests erfolgreich": CLI-Aufruf und Struktur für alle drei Stufen, 10 Rätsel je Stufe, `conflicts()` und `solutions()`.

**Offene Punkte aus der Spezifikation, die keine Prüfung abdeckt:** Ich habe sie nicht geändert, weil sie den Bedienvertrag nicht betreffen.
- `api/neu.py` aus Abschnitt 5 existiert in diesem Ordner nicht. Die Abnahme stellt `api/neu` selbst bereit, deshalb lädt das Spiel dort. Beim Öffnen von `index.html` ohne einen Server, der `api/neu` bedient, erscheint der Fehler-Toast.
- Das Ergebnis "gelöst" prüft `board.js` selbst (alle Felder gefüllt und keine Konflikte). Es ruft dafür nicht `solutions(puzzle, 2)` auf, wie A7 es beschreibt.