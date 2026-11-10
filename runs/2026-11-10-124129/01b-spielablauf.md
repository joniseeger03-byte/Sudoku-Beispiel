## Spielablauf für ein Browser-Sudoku

Hier ein Vorschlag für den Spielablauf eines Browser-Sudokus, der die genannten Anforderungen (Eingabe, Fehleranzeige, Notizen, Hilfen) berücksichtigt und die Einwände aus `02-pruefung.md` einarbeitet.

### 1. Eingabe

*   **Methode:**  Die Eingabe soll sowohl über die Tastatur als auch per Touch möglich sein.
    *   **Tastatur:**  Zahlen 1-9 erlauben das direkte Eintragen in die selektierte Zelle.  Tastaturpfeile und Tab ermöglichen die Navigation zwischen den Zellen, wobei die aktuell selektierte Zelle klar visuell hervorgehoben wird.  "Delete" oder "Backspace" leert die selektierte Zelle.
    *   **Touch:**  Ein Tipp auf eine Zelle selektiert diese.  Ein erneuter Tipp oder das Aufrufen einer virtuellen Tastatur ermöglicht die Eingabe.  Langes Drücken einer Zelle könnte ein Kontextmenü öffnen (siehe Hilfen unten).
*   **Selektion:** Die aktuell selektierte Zelle sollte visuell klar hervorgehoben sein (z.B. durch eine farbliche Umrandung oder einen Schatten).
*   **'Bleistift-Modus' als Standard:**  Beim ersten Tippen sollte automatisch der "Bleistift-Modus" aktiviert werden, d.h. die Ziffer sollte als kleine Notiz in die Zelle eingegeben werden (siehe Notizen-Abschnitt). Nur durch wiederholtes Tippen/Auswahl der gleichen Ziffer in der gleichen Zelle wird die Ziffer "fest" eingetragen. Dies erleichtert das Spiel und vermeidet versehentliches Falscheingeben.

### 2. Fehleranzeige (Konflikte)

*   **Echtzeitprüfung:**  Jede Eingabe (Zahl oder Notiz) wird sofort auf Konflikte geprüft.
*   **Visuelle Markierung:**
    *   **Zeile:**  Zellen in der gleichen Zeile mit der gleichen Zahl werden visuell hervorgehoben (z.B. durch rote Umrandung).
    *   **Spalte:**  Zellen in der gleichen Spalte mit der gleichen Zahl werden visuell hervorgehoben (z.B. durch rote Umrandung).
    *   **Block (3x3):**  Zellen innerhalb des gleichen 3x3-Blocks mit der gleichen Zahl werden visuell hervorgehoben (z.B. durch rote Umrandung).
*   **Schwergrad:** Die Intensität der visuellen Markierung könnte vom Schwierigkeitsgrad abhängen. Bei leichtem Schwierigkeitsgrad wäre die Markierung subtiler (z.B. leichte Umrandung), bei schwerem Schwierigkeitsgrad deutlicher (z.B. rote, blinkende Umrandung).
*   **Keine Fehlermeldung:** Statt einer störenden Fehlermeldung wird nur die visuelle Markierung verwendet. Der Spieler soll selbst erkennen, wo der Fehler liegt.
*   **Deaktivierung der Markierung:** Die Markierung wird automatisch entfernt, sobald der Konflikt behoben ist.

### 3. Notizen (Bleistift-Modus)

*   **Aktivierung/Deaktivierung:** Ein Knopf oder ein Link (z.B. "Notizen") ermöglicht das Umschalten zwischen dem normalen Eingabemodus und dem Bleistift-Modus. Alternativ kann auch automatische Aktivierung beim ersten Tippen implementiert werden.
*   **Eingabe:**  Im Bleistift-Modus können mehrere Ziffern (1-9) in eine Zelle eingegeben werden.  Diese werden als kleine Zahlen innerhalb der Zelle dargestellt.
*   **Löschen von Notizen:**  Eine weitere Eingabe im Bleistift-Modus überschreibt die bestehende Notiz bzw. löscht sie ganz, wenn die Zahl bereits vorhanden ist.  Ein spezieller Löschen-Modus (z.B. durch langes Drücken einer Taste oder eines Icons) könnte eine selektive Entfernung von Notizen ermöglichen.
*   **Hervorhebung beim Tippen:**  Beim Tippen einer Zahl im Bleistift-Modus werden alle Zellen, in denen diese Zahl bereits als Notiz vorhanden ist, kurz hervorgehoben.

### 4. Hilfen

*   **"Anzeigen möglicher Werte"**: Markiert Zellen, die potentiell einen Wert aufnehmen können, basierend auf Ausschlussverfahren (z.B. Werte, die nicht in Zeile, Spalte oder Block vorkommen).  Diese Funktion sollte optional aktiviert werden können, um zu verhindern, dass sie zu stark beim Lösen hilft.
*   **"Hinweis"**:  Gibt einen einzelnen, korrekten Wert für eine ausgewählte Zelle vor.  Die Anzahl der Hinweise sollte begrenzt sein (z.B. 3 pro Spiel) und möglicherweise durch das Ansehen von Werbung freigeschaltet werden können.
*   **"Falsche Ziffer löschen"**: Entfernt eine falsche Ziffer aus dem Sudoku-Feld. (Anzahl der Löschungen begrenzen).
*   **Tastaturkürzel**:  Bei langem Drücken einer Zahlentaste (oder eines Touch-Icons) könnte eine Hilfefunktion für diese Zahl aktiviert werden (z.B. "zeige alle Zellen, in denen diese Zahl möglich ist").
*   **Tutorial (optional):** Ein kurzes Tutorial erklärt die Regeln von Sudoku und die Funktionen der Benutzeroberfläche.

### Schwierigkeitsgrade

*   **Leicht:**  Die Rätsel haben viele bereits ausgefüllte Zellen (z.B. 35-40). Die Lösung ist relativ offensichtlich.
*   **Mittel:**  Weniger vorgegebene Zellen (z.B. 30-35).  Benötigt mehr logisches Denken.
*   **Schwer:**  Nur wenige vorgegebene Zellen (z.B. 25-30).  Erfordert fortgeschrittene Sudoku-Techniken.
*   **Rätselgenerierung:** Die Rätsel sollten algorithmisch generiert werden, um sicherzustellen, dass jedes Rätsel genau eine Lösung hat.

### Empfehlung

Ich empfehle eine klare und intuitive Benutzeroberfläche. Die visuelle Markierung von Konflikten und die Notizfunktion sind essenziell für ein gutes Spielerlebnis.  Der "Bleistift-Modus" sollte standardmäßig aktiviert sein, um die Eingabe zu erleichtern. Die Hilfen sollten sparsam eingesetzt werden, um den Spieler nicht zu entmutigen.  Die Performance sollte auf mobilen Geräten priorisiert werden.

### Annahmen

*   Es wird ein modernes JavaScript-Framework (z.B. React, Vue.js) oder Vanilla JavaScript verwendet.
*   Das Layout wird mit HTML und CSS erstellt, das Responsive Design unterstützt.
*   Die Rätselgenerierung wird mit einem geeigneten Algorithmus implementiert.
*   Es gibt keine Server-Komponente (reines Frontend).

### Quellen

*   [Sudoku.com](https://sudoku.com/) - Gute Beispiele für Sudoku-Interface Designs und Hilfefunktionen.
*   [websudoku.com](https://websudoku.com/) - Simples, aber funktionelles Online-Sudoku.
*   keine gesicherte Quelle
