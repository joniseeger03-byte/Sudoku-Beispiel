## Spezifikation: Sudoku für das Web

Diese Spezifikation beschreibt die Anforderungen für die Entwicklung eines spielbaren Sudoku für den Browser ohne Backend, basierend auf dem ursprünglichen Auftrag, der Recherche und den Hinweisen der Prüfung.

**1. Funktionale Anforderungen**

1.  **Rätselgenerierung:**
    *   Die Anwendung generiert Sudoku-Rätsel in drei Schwierigkeitsgraden: leicht, mittel, schwer.
    *   Jedes generierte Rätsel hat genau eine eindeutige Lösung.
    *   Die Generierung erfolgt clientseitig in JavaScript. Sie basiert auf der Methode, mit einem vollständig gelösten Sudoku zu beginnen und iterativ Zahlen zu entfernen, wobei nach jeder Entfernung die Eindeutigkeit geprüft wird.
    *   `CLUES` definiert die Anzahl der Hinweise pro Schwierigkeitsgrad: `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}`.
2.  **Benutzeroberfläche (UI):**
    *   Die UI besteht aus einem 9x9 Gitter, repräsentiert durch HTML-Elemente mit `data-index="0"` bis `"80"`.
    *   Jedes Feld zeigt die aktuelle Ziffer (1-9) als Text an oder ist leer (0).
    *   Zifferneingabe erfolgt über:
        *   Buttons mit `data-digit="1"` bis `"9"` und `data-digit="0"` (Löschen).
        *   Tastatureingabe (1-9, Pfeiltasten, Entf, Rücktaste).
    *   Ausgewähltes Feld wird visuell hervorgehoben (eigene CSS-Klasse).
    *   3x3-Blöcke sind durch dickere Linien oder größere Abstände erkennbar.
    *   Felder im Konflikt erhalten die Klasse `konflikt`.
    *   Bei gelöstem Rätsel erhält das `<body>`-Element die Klasse `geloest`.
3.  **Spielablauf:**
    *   Der Spieler wählt einen Schwierigkeitsgrad (leicht, mittel, schwer) über Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"`.
    *   Nach der Auswahl wird ein neues Rätsel des gewählten Schwierigkeitsgrads generiert und angezeigt.
    *   Die Anwendung überprüft bei jeder Eingabe auf Konflikte und markiert diese visuell.
    *   Ein Notizen-Modus ist verfügbar, der es dem Spieler erlaubt, potenzielle Ziffern klein in die Zellen zu schreiben. Der Modus wird durch einen Button oder eine Taste aktiviert/deaktiviert und visuell signalisiert (z.B. durch ein Symbol oder eine Statusleiste).
    *   Hilfen sind verfügbar:
        *   "Zeige Fehler": Markiert alle aktuellen Konflikte.
        *   "Zeige mögliche Werte": Zeigt die möglichen Ziffern für das ausgewählte Feld an.
    *   Das Spiel erkennt automatisch, wenn das Rätsel gelöst ist und zeigt eine Erfolgsmeldung an.
4.  **API:**
    *   Die Anwendung stellt eine API bereit unter `/api/neu?stufe=<stufe>` (z.B. `/api/neu?stufe=mittel`), die im JSON-Format ein neues Rätsel des angegebenen Schwierigkeitsgrads zurückgibt.  Das JSON-Objekt enthält die Felder: `puzzle`, `solution`, `clues` und `level`.  `puzzle` und `solution` sind Listen mit 81 Zahlen, wobei 0 eine leere Zelle repräsentiert. `clues` ist die Anzahl der vorgegebenen Zahlen im Rätsel (entspricht dem Wert in `CLUES` für den gewählten Schwierigkeitsgrad).

**2. Technische Anforderungen**

1.  **Technologie-Stack:** HTML, CSS, JavaScript (nur Standardbibliothek ohne externe Abhängigkeiten).
2.  **Code-Struktur:**
    *   `engine.py` implementiert die Logik für die Rätselgenerierung, Lösung und Konflikterkennung.
    *   `index.html` definiert die Grundstruktur der Webseite.
    *   `board.js` implementiert die Spiel-Logik und die Interaktion mit dem Benutzer.
    *   `style.css` enthält die CSS-Formatierung.
3.  **Performance:**
    *   Die Generierung eines Rätsels sollte innerhalb von 200ms abgeschlossen sein, auch bei hohem Schwierigkeitsgrad.
    *   Die Konflikterkennung sollte in Echtzeit erfolgen, ohne merkliche Verzögerung.
4.  **Testbarkeit:**
    *   Die Anwendung muss über automatische Tests verfügen, die sicherstellen, dass die Logik korrekt funktioniert.  Tests werden mit `python test_spiel.py` ausgeführt. Tests dürfen nicht mit Exit-Code ungleich 0 enden.

**3. Vertrag (Unverändert)**

- engine.py nutzt nur die Python-Standardbibliothek.
- `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.
- `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. puzzle und solution sind Listen mit 81 Zahlen, 0 steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in puzzle und gleich `CLUES[level]`.
- `solutions(puzzle, limit)` liefert eine Liste mit höchstens limit Lösungen.
- `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.
- `python engine.py neu <stufe>` gibt das Ergebnis von generate als JSON aus.
- index.html, board.js und style.css bilden die Oberfläche im Browser. board.js holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.
- Bedienvertrag der Oberfläche: Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein input). Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `"9"`, der Löschen-Button trägt `data-digit="0"`. Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel. Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über keydown auf document verarbeitet. Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben. Die 3×3-Blöcke sind durch dickere Linien oder größere Abstände erkennbar. Felder im Konflikt tragen die Klasse `konflikt`. Ist das Rätsel richtig gelöst, trägt body die Klasse `geloest`.
- test_spiel.py läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit-Code ungleich 0.

**4. Abnahmekriterien**

A1.  Die Anwendung generiert korrekt Sudoku-Rätsel für alle drei Schwierigkeitsgrade (leicht, mittel, schwer).
A2.  Jedes generierte Rätsel hat genau eine eindeutige Lösung, dies wird durch die Eindeutigkeitsprüfung nach jedem Schritt der Reduktion bestätigt.
A3.  Die UI wird korrekt gerendert und ist benutzerfreundlich.
A4.  Die Zifferneingabe funktioniert korrekt über Tastatur und Touch.
A5.  Konflikte werden in Echtzeit erkannt und visuell markiert.
A6.  Der Notizen-Modus funktioniert korrekt und ist leicht zu bedienen.
A7.  Die Hilfen "Zeige Fehler" und "Zeige mögliche Werte" funktionieren korrekt.
A8.  Das Spiel erkennt automatisch, wenn das Rätsel gelöst ist, und zeigt eine Erfolgsmeldung an.
A9.  Die API `/api/neu?stufe=<stufe>` liefert die erwarteten Daten im JSON-Format zurück.
A10. Die Performance ist ausreichend (Generierung < 200ms).
A11. Die automatischen Tests in `test_spiel.py` laufen ohne Fehler durch (Exit-Code 0).
A12. Die Anwendung erfüllt alle Anforderungen des Vertrags.
