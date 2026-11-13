

## Spielablauf für ein Browser-Sudoku

Hier ein Vorschlag für den Spielablauf eines Sudoku-Spiels im Browser, unter Berücksichtigung der Anforderungen aus der Auftragsbeschreibung und den Einwänden aus der Test-Datei (02-pruefung.md).

### 1. Eingabe

*   **Zellenauswahl:**
    *   **Maus:** Klick auf eine Zelle wählt diese aus.  Die ausgewählte Zelle sollte visuell hervorgehoben werden (z.B. durch eine andere Hintergrundfarbe).
    *   **Touch:** Tippen auf eine Zelle wählt diese aus.  Die gleiche visuelle Hervorhebung wie bei der Mausbedienung.
    *   **Navigation:**  Pfeiltasten zur Navigation zwischen den Zellen.  Speichern der aktuellen Zelle für die Eingabe.  `Shift` + Pfeiltasten könnten die Navigation in Blöcken (3x3) ermöglichen, ist aber optional.
*   **Zahlen-Eingabe:**
    *   **Tastatur:**  Zifferntasten (1-9) füllen die ausgewählte Zelle mit der entsprechenden Zahl.  `Backspace` oder `Delete` leeren die Zelle.
    *   **Touch:**  Eine numerische Tastatur (entweder virtuell als Overlay oder als separate Schaltfläche, die ein Panel öffnet) ermöglicht die Eingabe der Ziffern.
*   **Eingabebeschränkungen:**
    *   Es sollte nicht möglich sein, eine bereits vorgegebene Zelle zu bearbeiten.  Diese Zellen sollten visuell klar von den spielbaren Zellen unterschieden sein (z.B. durch andere Farbe oder Fettdruck).
    *   Die Eingabe sollte auf Ziffern von 1 bis 9 beschränkt sein. Andere Eingaben sollten ignoriert werden.

### 2. Fehleranzeige (Konflikte)

*   **Sofortige Überprüfung:** Jede Eingabe wird sofort auf Konflikte geprüft (gleiche Zahl in Zeile, Spalte oder 3x3-Block).
*   **Visuelle Markierung:** Konflikte werden direkt im Spielbrett visuell dargestellt.  Es gibt mehrere Optionen:
    *   **Hervorhebung:** Die konfliktträchtigen Zellen (die Gerichtete Zelle und alle Zellen, die den Konflikt verursachen) werden hervorgehoben (z.B. rot).
    *   **Symbol:** Ein kleines Konfliktsymbol (z.B. ein rotes X) wird in den konfliktträchtigen Zellen angezeigt.
*   **Fehlermeldung (Optional):** Eine subtile Fehlermeldung (z.B. "Konflikt!") könnte angezeigt werden, ist aber weniger wichtig als die visuelle Markierung. Vermeide aufdringliche Popups.
*   **Aufhebung der Markierung:** Die Markierung verschwindet, sobald der Konflikt durch Korrektur der Eingabe behoben ist.

### 3. Notizen (Stift-Modus)

*   **Aktivierung:** Ein "Notizen"-Modus wird durch einen Schalter/Button aktiviert.
*   **Eingabe:** Im Notizen-Modus bewirken Zifferneingaben, dass die Ziffer *klein* in der Zelle als Notiz angezeigt wird.
*   **Mehrere Notizen:**  Es sollen mehrere Notizen pro Zelle möglich sein (z.B. durch wiederholtes Klicken auf die gleiche Ziffer oder durch eine virtuelle Tastatur mit "Add/Remove"-Funktion für Notizen). Es ist wichtig, die Notizen gut sichtbar und unterscheidbar von der eigentlichen Zelle zu platzieren.
*   **Löschen von Notizen:**  `Backspace` oder `Delete` im Notizen-Modus löschen die zuletzt eingegebene Notiz in der Zelle.
*   **Deaktivierung:**  Der Notizen-Modus wird durch erneutes Klicken auf den Schalter/Button deaktiviert. Im normalen Modus werden die Notizen zuerst gelöscht oder überdeckt.
*   **Klare visuelle Unterscheidung:** Notizen müssen deutlich von den eigentlichen Zahlen unterschieden sein (z.B. kleinere Schrift, andere Farbe, andere Position innerhalb der Zelle).

### 4. Hilfen

*   **Überprüfung (Check):** Eine "Check"-Funktion, die das gesamte Sudoku auf Fehler überprüft und alle Konflikte markiert.  Sollte nicht unendlich oft verfügbar sein (z.B. limitierte Anzahl pro Spiel, abhängig vom Schwierigkeitsgrad).  Ergänzung: Ein Check, der nur die aktuell ausgewählte Zelle prüft, kann ebenfalls nützlich sein.
*   **Hinweis:**  Eine "Hinweis"-Funktion, die eine korrekte Zahl in einer (zufällig gewählten) leeren Zelle vorschlägt.  Sollte sehr limitiert sein (z.B. nur einer pro Spiel).
*   **Farbliche Markierung:**  Eine Option, um die Zeilen, Spalten und 3x3-Blöcke, in denen eine bestimmte Ziffer vorkommt, farblich hervorzuheben. Dies hilft dem Spieler, mögliche Positionen für die Ziffer zu finden.  Die aktive Ziffer sollte über einen Satz von Schaltflächen oder durch Anklicken einer Ziffer im Sudoku ausgewählt werden können.

### 5. Schwierigkeitsgrade

*   **Leicht:** Viele vorgegebene Zahlen, einfache Logik erforderlich.
*   **Mittel:** Weniger vorgegebene Zahlen, erfordert etwas mehr Logik und Strategie.
*   **Schwer:**  Sehr wenige vorgegebene Zahlen, erfordert fortgeschrittene Sudoku-Strategien.

Die Generierung der Sudokus muss sicherstellen, dass jedes Rätsel genau eine eindeutige Lösung hat.  Dies ist eine separate, komplexe Aufgabe.

### Umgang mit Einwänden aus 02-pruefung.md

*   **Eingabe mit Touch:** Die Anforderung ist integriert.
*   **Klare Abgrenzung vorgegebene Zahlen:**  Vorgegebene Zahlen werden visuell deutlich abgesetzt (Farbe, Fettdruck).
*   **Sofortige Fehleranzeige:**  Implementiert, wie oben beschrieben.
*   **Möglichkeit zum Löschen:** `Backspace`/`Delete` löschen die Eingabe.
*   **Notizenmodus:** Vollständig integriert, inklusive der Möglichkeit, mehrere Notizen pro Zelle zu speichern.
*   **Nicht-Numerische Eingabe:** Abgefangen und ignoriert.



### Empfehlung

Ich empfehle, mit einer einfachen, visuellen Fehleranzeige zu beginnen (z.B. rote Hervorhebung).  Die Notizenfunktion ist ein wichtiges Feature, das frühzeitig implementiert werden sollte. Die Hilfen sollten sparsam eingesetzt werden, um den Schwierigkeitsgrad nicht zu unterschätzen.  Die Usability sollte auf verschiedenen Browsern und Geräten (Desktop, Tablet, Smartphone) getestet werden.

### Annahmen

*   Es wird ein Framework oder eine Bibliothek für die UI-Entwicklung verwendet (z.B. React, Vue.js, Angular oder einfach Vanilla JavaScript).
*   Die Sudoku-Generierung erfolgt serverseitig oder durch einen separaten Algorithmus.
*   Der Fokus liegt auf der Client-seitigen Implementierung des Spielablaufs.

### Quellen

*   keine gesicherte Quelle.  Der Spielablauf basiert auf allgemeinem Wissen über Sudoku-Spiele und Best Practices im Bereich der User Experience. Online Sudokus (z.B. auf websudoku.com) wurden zur Inspiration herangezogen, aber nicht als direkte Quellen im Sinne einer Dokumentation.
