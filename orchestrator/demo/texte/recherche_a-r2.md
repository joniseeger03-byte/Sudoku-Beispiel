# Recherche A: Rätsel erzeugen (überarbeitet)

## Empfehlung
1. Vollständiges Gitter per Backtracking mit zufälliger Ziffernfolge füllen. Zuerst das Feld mit den wenigsten Kandidaten wählen.
2. Felder in zufälliger Reihenfolge leeren.
3. Nach jedem Leeren die Lösungen zählen, mit Abbruch bei 2. Bei mehr als einer Lösung das Feld zurücksetzen.
4. Wird die Zielzahl nicht erreicht, mit einem neuen Gitter erneut versuchen.

## Annahmen
- Hinweise: leicht 38, mittel 32, schwer 26. Das erreicht zufälliges Leeren zuverlässig in unter einer Sekunde.

## Quellen
- McGuire et al. (2012): 17 Hinweise sind die bewiesene Untergrenze, kein praktisches Ziel.
