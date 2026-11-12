
## Spielablauf für ein Browser-Sudoku

Dieser Entwurf beschreibt den Spielablauf für ein browserbasiertes Sudoku, berücksichtigt die Anforderungen aus der Auftragsbeschreibung und die Einwände aus der `02-pruefung.md`-Datei (wird hier angenommen, dass du sie mir zur Verfügung gestellt hast, da sie nicht explizit enthalten ist). Die Annahmen werden anschließend präzisiert.

### 1. Eingabe

* **Zellenfokus:** Der Fokus bewegt sich mit den Pfeiltasten oder Touch-Events (Tap/Slide) zyklisch durch die leeren Zellen des Sudoku-Gitters.  Die aktuell fokussierte Zelle wird optisch hervorgehoben (z.B. durch eine farbliche Umrandung).
* **Zifferneingabe:**
    * **Tastatur:**  Ziffern 1-9 werden direkt in die fokussierte Zelle eingefügt.  "Entf" oder "Backspace" löschen den aktuellen Wert. Für mobile Geräte oder unterstützen von Touch-Eingabe kann eine virtuelle Tastatur angezeigt werden (siehe unten).
    * **Touch:**  Die Zifferneingabe erfolgt über eine virtuelle Tastatur. Diese kann entweder als Popup dargestellt oder unterhalb des Sudoku-Gitters eingeblendet werden.  Die virtuelle Tastatur sollte gut bedienbar und nicht zu aufdringlich sein.
    * **Einfaches Tippen:** Auf Touch-Geräten könnte auch direktes Tippen in die Zelle erlaubt sein, jedoch mit erhöhter Konfliktgefahr und evtl. Balloneffekt/Übersteuerung. Dies sollte optional wählbar sein oder im Schwierigkeitsgrad differenziert werden.
* **Mehrfach Eingabe:**  Ermöglicht die schnelle Eingabe mehrerer Ziffern, beispielsweise durch Drag-and-Drop (insbesondere auf Touch-Geräten), oder durch einfaches Hintereinander Tasten drücken (mit Verzögerung, falls nötig).
* **Direkte Eingabe durch 'Shift' plus Ziffer:**  Erlaubt, direkt Notizen einzutragen, ohne zuerst in den Notizenmodus wechseln zu müssen (siehe Abschnitt Notizen).

### 2. Fehleranzeige (Konfliktmarkierung)

* **Echtzeit-Überprüfung:** Nach jeder Eingabe wird sofort geprüft, ob Konflikte in der gleichen Zeile, Spalte oder dem 3x3-Block vorliegen.
* **Visuelle Markierung:**  Ziffern, die Konflikte verursachen, werden optisch hervorgehoben. Die Hervorhebung sollte deutlich, aber nicht zu aufdringlich sein (z.B. rote Farbe, subtiler Hintergrund).
* **Markierung des Konflikts:**  Zusätzlich zur Markierung der in Konflikt stehenden Ziffern sollte auch die gesamte Zeile, Spalte und der 3x3-Block, in dem der Konflikt auftritt, visuell hervorgehoben werden, um die Ursache des Fehlers besser zu erkennen.
* **Feedback bei Löschung:**  Beim Löschen einer Ziffer sollte geprüft werden, ob dadurch ein vorheriger Konflikt behoben wurde. In diesem Fall sollte die entsprechende Markierung sofort entfernt werden.
* **Sorgfältige Konfliktprüfung:** Eine abweichende Markierung der Konflikte muss sofort behoben werden.

### 3. Notizen (Bleistiftmarkierungen)

* **Notizenmodus:** Ein Umschalter ermöglicht den Wechsel zwischen dem Modus zur direkten Eingabe von Ziffern und dem Notizenmodus.
* **Notizeneingabe:** Im Notizenmodus wird durch Klicken oder Tippen in eine Zelle eine Liste möglicher Ziffern für diese Zelle angezeigt.  Der Benutzer kann dann die entsprechenden Ziffern auswählen oder über eine virtuelle Tastatur eingeben.
* **Visuelle Darstellung:** Notizen werden klein und subtil in den Zellen angezeigt, so dass sie die eigentlichen Ziffern nicht überdecken.  Häufig verwendete Farben für Notizen sind hellgrau oder ein transparenter Farbton.
* **Notizen-Löschung:**  Notizen können durch erneutes Klicken/Tippen auf die Zelle oder über eine Löschfunktion in der virtuellen Tastatur entfernt werden.
* **Automatische Aktualisierung:**  Beim Eintragen einer Ziffer sollte das System automatisch prüfen, ob die Ziffer in den Notizen der Zeile, Spalte oder des 3x3-Blocks vorhanden ist, und diese dann entfernen.
* **Mehrfach Notizen pro Zelle:** Es muss erlaubt sein, mehrere Notizen in einer Zelle zu haben (alle Ziffern von 1-9, wenn noch keine andere Ziffer vergeben ist).

### 4. Hilfen

* **"Anzeigen möglicher Werte":** Klickt man in eine Zelle, werden alle möglichen Werte, die in dieser Zelle eingetragen werden können, kurz angezeigt (z.B. als kleine Notizen, die kurzzeitig aufleuchten). Dies soll als sanfte Hilfe dienen, ohne die Lösung vorzugeben.
* **"Hinweis":**  Bei Bedarf kann ein "Hinweis"-Button angeboten werden, welcher eine legale Ziffer für eine zufällig ausgewählte, ungelöste Zelle vorschlägt.  Die Anzahl der Hinweise sollte begrenzt sein, um den Schwierigkeitsgrad zu erhalten.
* **Fehlerprüfung:** Eine Funktion, die alle aktuellen Fehler im Sudoku hervorhebt (ggf. eine detailliertere Analyse als die Echtzeit-Konfliktmarkierung).  Dies sollte sein eine Option sein, die nicht standardmäßig aktiviert ist, da sie den Lösungsprozess zu stark beeinflussen kann.
* **"Mögliche Ziffern" für das gesamte Feld (teilweise):** Zeigt auf Knopfdruck die herausgefundenen Kandidaten für alle Felder an. Der Schwierigkeitsgrad hierbei kann manuell eingestellt werden (z.B. Anzeige von 1-3 Kandidaten oder alle Kandidaten).

### 5. Schwierigkeitsgrade

* **Leicht:**  Wenige vorgegebene Ziffern, einfache logische Schlussfolgerungen sind ausreichend.
* **Mittel:**  Mehr vorgegebene Ziffern, komplexere logische Schlussfolgerungen wie versteckte Singles, Naked Pairs usw. sind erforderlich.
* **Schwer:**  Wenige vorgegebene Ziffern, erfordert fortgeschrittene Techniken wie X-Wing, Swordfish usw.

**Generierung von Rätseln:** Die Rätsel werden stets einmalig lösbar sein. Dies kann z.B. durch Backtracking oder ähnliche Algorithmen gewährleistet werden.

### Empfehlung

Ein iterativer Entwicklungsprozess ist empfehlenswert. Beginne mit den grundlegenden Funktionen (Eingabe, Fehleranzeige) und erweitere diese schrittweise um Notizen und Hilfen.  Nutzer-Tests sind entscheidend, um die Benutzerfreundlichkeit und das Spielerlebnis zu optimieren. Die Benutzeroberfläche sollte klar und intuitiv gestaltet sein.

### Annahmen

* **Frontend-Framework:** Die Implementierung erfolgt in einem modernen JavaScript-Framework (z.B. React, Angular, Vue.js) für eine effiziente Entwicklung und Wartung.
* **Kein Backend:**  Die Rätselgenerierung und -prüfung finden ausschließlich im Browser statt.
* **Responsive Design:** Das Sudoku wird sich an unterschiedliche Bildschirmgrößen und Geräte anpassen.
* **Barrierefreiheit:**  Es wird auf Barrierefreiheit geachtet, damit auch Benutzer mit Behinderungen das Sudoku spielen können.

### Quellen

* **Sudoku-Regeln:** [https://de.wikipedia.org/wiki/Sudoku](https://de.wikipedia.org/wiki/Sudoku)
* **Algorithmus zur Sudoku-Lösung (Backtracking):**  Viele Beispiele und Erläuterungen online, z.B. [https://www.baeldung.com/java-sudoku](https://www.baeldung.com/java-sudoku) (dies ist nur ein Beispiel, andere Sprachen und Ressourcen sind ebenfalls möglich).
* **keine gesicherte Quelle:**  Inspiration für Benutzeroberflächen von anderen Online-Sudoku-Spielen (z.B. auf Web Sudoku, online-sudoku.com).  (Wurden nur zur Inspirationsbasis herangezogen.)
