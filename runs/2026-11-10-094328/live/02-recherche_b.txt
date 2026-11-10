## Spielablauf für ein Browser-Sudoku

Dieser Entwurf beschreibt den Spielablauf für ein Sudoku, das in einem Browser ohne Backend implementiert werden soll. Er berücksichtigt Eingabe, Fehleranzeige, Notizen und Hilfen, und integriert Feedback aus einer hypothetischen Prüfung (02-pruefung.md, deren Einwände hier berücksichtigt werden).

### Empfehlung

Das Spiel sollte einen intuitiven und benutzerfreundlichen Spielablauf bieten.  Hier ist ein Vorschlag:

1.  **Spielbeginn & Schwierigkeitsgrad:** Der Spieler wählt einen Schwierigkeitsgrad (leicht, mittel, schwer) aus einem Menü. Das Sudoku-Raster wird entsprechend generiert oder aus einer vorgefertigten Liste geladen.
2.  **Eingabe:**
    *   **Tastatur:** Der Spieler kann Zahlen (1-9) über die Tastatur eingeben. Die Eingabe erfolgt in die aktuell selektierte Zelle.  Pfeiltasten bewegen den Cursor.  'Backspace' oder 'Delete' löschen den Wert der aktuellen Zelle.
    *   **Touch:**  Der Spieler tippt auf eine Zelle, um sie auszuwählen. Ein pop-up-Keyboard mit den Zahlen 1-9 erscheint.  Der Spieler tippt auf die gewünschte Zahl, um sie einzutragen.  Ein "Löschen"-Button im pop-up-Keyboard entfernt den Wert.
3.  **Fehleranzeige:**
    *   **Echtzeit-Konfliktanzeige:**  Sobald der Spieler eine Zahl einträgt, werden sofort Konflikte (gleiche Zahl in Zeile, Spalte oder 3x3-Block) durch eine visuelle Markierung hervorgehoben.  Dies könnte durch eine rote Färbung der Konflikt-Zellen geschehen. Achte hierbei darauf, *alle* beteiligten Zellen zu markieren, nicht nur die zuletzt bearbeitete.
    *   **Hinweis-System:**  Zusätzlich zur direkten Markierung könnte eine kurze Nachricht wie "Konflikt in Zeile X" oder "Konflikt im Block Y" angezeigt werden.
4.  **Notizen:**
    *   **Aktivierbar:** Der Spieler kann einen "Notizen"-Modus aktivieren/deaktivieren.
    *   **Bleistift-Einträge:** Im Notizen-Modus können kleine Zahlen (1-9) in die Zellen geschrieben werden, um mögliche Kandidaten zu notieren. Diese Einträge sollten visuell von den festen Eingaben unterscheidbar sein (z.B. kleinere Schriftgröße, hellere Farbe).
    *   **Löschen von Notizen:**  Notizen können mit einem separaten "Löschen"-Button im Notizen-Modus entfernt werden.
5.  **Hilfen:**
    *   **Hinweis (einmal pro Rätsel):**  Der Spieler kann einen Hinweis anfordern, der eine zufällige, korrekte Zahl in einer leeren Zelle vorschlägt.  Dieser Hinweis sollte erst verfügbar sein, wenn das Rätsel überhaupt lösbar ist.
    *   **Kontrolle:**  Eine Funktion, die prüft, ob die aktuelle Eingabe mit den Regeln des Sudoku übereinstimmt (keine direkten Konflikte).  Dies gibt keine Lösung, sondern bestätigt lediglich, dass die aktuellen Eingaben gültig sind.
6.  **Spielende:** Das Rätsel ist gelöst, wenn alle Zellen gefüllt sind und keine Konflikte mehr vorhanden sind. Eine entsprechende Meldung wird angezeigt.

**Berücksichtigung der Einwände aus 02-pruefung.md:**

*   **Konfliktvisualisierung:**  Wie oben beschrieben, muss die Konfliktvisualisierung *alle* beteiligten Zellen markieren, und nicht nur die zuletzt geänderte. Das macht die Ursache für Konflikte deutlich erkennbar.
*   **Notizen-Modus:** Notizen müssen klar von festen Eingaben unterscheidbar und leicht zu löschen sein.
*   **Hinweise:** Ein einzelner Hinweis pro Rätsel verhindert den Missbrauch der Hilfsfunktion. Der Hinweis sollte nicht trivial sein und nur aktiviert werden, wenn das Rätsel tatsächlich noch eine Lösung hat.
*   **Performanz:** Das Spiel soll ohne Backend ausgeführt werden, daher ist es wichtig, die Generierung der Rätsel und die Konflikterkennung effizient zu gestalten. Priorisiere eine klare Code-Struktur, um die Wartung und Optimierung zu erleichtern.

### Annahmen

*   Die Generierung des Sudoku-Rätsels erfolgt clientseitig.  Es muss gewährleistet sein, dass jedes Rätsel genau eine Lösung hat. Algorithmen zur Sudoku-Generierung sind bekannt und können implementiert werden (z.B. Backtracking).
*   Der Browser unterstützt die erforderlichen JavaScript-APIs für Touch-Ereignisse und DOM-Manipulation.
*   Die Benutzeroberfläche wird mit HTML, CSS und JavaScript erstellt.
*   Das Design ist responsive, um auf verschiedenen Bildschirmgrößen gut darzustellen.

### Quellen

*   **JavaScript Dokumentation (MDN):**  [https://developer.mozilla.org/de/docs/Web/JavaScript](https://developer.mozilla.org/de/docs/Web/JavaScript) -  Für die Implementierung der Logik,  Event Listener, DOM-Manipulation.
*   **HTML Dokumentation (MDN):** [https://developer.mozilla.org/de/docs/Web/HTML](https://developer.mozilla.org/de/docs/Web/HTML) - Für die Struktur der Benutzeroberfläche.
*   **CSS Dokumentation (MDN):** [https://developer.mozilla.org/de/docs/Web/CSS](https://developer.mozilla.org/de/docs/Web/CSS) -  Für das Design und das Responsive Layout.
*   **Algorithmen zur Sudoku-Generierung:** Es gibt viele Ressourcen online, die Algorithmen zur Sudoku-Generierung beschreiben.  Die genaue Implementierung kann variieren. Keine gesicherte Quelle, da viele Blog-Posts und Tutorials darüber existieren, aber das Grundprinzip ist etabliert.
*   **keine gesicherte Quelle:** Verschiedene Online-Beispiele für Sudoku-Spiele im Browser, die zur Inspiration für die Benutzeroberfläche und den Spielablauf verwendet wurden.
