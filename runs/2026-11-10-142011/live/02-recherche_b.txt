

## Spielablauf für ein Browser-Sudoku

Dieses Dokument beschreibt einen empfohlenen Spielablauf für ein Browser-Sudoku, basierend auf den Anforderungen des Auftrags und unter Berücksichtigung der Einwände aus der Prüfungsdatei (02-pruefung.md).

### 1. Empfehlung

Der empfohlene Spielablauf ist wie folgt:

1.  **Startbildschirm:**
    *   Auswahl des Schwierigkeitsgrades (Leicht, Mittel, Schwer).
    *   Ein Button "Neues Spiel".
    *   Optional: Bestenliste (lokal gespeichert, keine Backend-Anforderungen).
2.  **Spielbereich:**
    *   Ein 9x9 Gitter, bestehend aus 9 Blöcken (3x3).
    *   Vorgegebene Zahlen sind fett oder in einer anderen Farbe dargestellt.
    *   Benutzereingabe:
        *   **Tastatur:** Eingabe von Zahlen (1-9) in die aktuell selektierte Zelle.  `Backspace` oder `Delete` zum Löschen.  Pfeiltasten (oder Tab) zur Navigation zwischen den Zellen.
        *   **Touch:** Tippen auf eine Zelle zum Selektieren. Ein Bildschirmtastatur erscheint (optional) mit Zahlen (1-9).  Tippen auf die Zahl fügt sie in die Zelle ein.
    *   **Notizen (Bleistift-Modus):**
        *   Ein Button "Notizen".
        *   Aktiviert/Deaktiviert den Notizmodus.
        *   Im Notizmodus können kleine Zahlen in den Zellen eingegeben werden, um mögliche Kandidaten zu markieren. Diese Notizen werden nicht Teil der Lösung und werden nur angezeigt, wenn der Notizmodus aktiviert ist.
        *   Die Notizen sollten sich visuell vom eigentlichen Spielbrett abheben (z.B. kleinere Schrift, andere Farbe).
    *   **Fehleranzeige (Konfliktprüfung):**
        *   Während der Eingabe wird *sofort* geprüft, ob ein Konflikt vorliegt (gleiche Zahl in derselben Zeile, Spalte oder 3x3-Block).
        *   Konflikte werden visuell markiert:
            *   Die fehlerhafte Zelle wird rot hervorgehoben.
            *   Alle Zellen, die den Konflikt verursachen (Zeile, Spalte, 3x3-Block), werden ebenfalls rot hervorgehoben (subtile Hervorhebung, um die Fehlerquelle klar zu identifizieren).
        *   Sobald eine Korrektur erfolgt ist, verschwinden die roten Markierungen.
    *   **Hilfen:**
        *   Ein Button "Hinweis".
        *   Bei Klick wird *eine* gültige Zahl in einer *zufälligen* leeren Zelle eingegeben. (Es wird nicht die *einzige* mögliche Lösung aufgedeckt, sondern nur ein Schritt vorgeschlagen.)
        *   Die Anzahl der Hinweise sollte begrenzt sein (z.B. 3 pro Spiel).
    *   **Validierung:**
        *   Ein Button "Prüfen".
        *   Überprüft das gesamte Sudoku auf Korrektheit.
        *   Gibt eine Meldung aus, ob das Sudoku korrekt ist oder ob noch Fehler vorhanden sind.
    *   **Lösung:**
        *   Ein Button "Lösung anzeigen".
        *   Zeigt die vollständige Lösung des Sudokus an. *Es sollte klar sein, dass dies ein "Cheating"-Button ist und die Nutzung nicht empfohlen wird.*  (z.B. durch eine Warnmeldung oder einen entsprechenden Hinweis).

3.  **Spielende:**
    *   Nachdem das Sudoku gelöst wurde (entweder durch Benutzereingabe oder durch "Lösung anzeigen") wird eine Erfolgsmeldung angezeigt.
    *   Option zum Starten eines neuen Spiels.

### 2. Annahmen

*   **Sudoku-Generierung:** Es wird davon ausgegangen, dass ein Algorithmus vorhanden ist, der Sudoku-Rätsel mit genau einer Lösung generiert und die vorgegebenen Schwierigkeitsgrade berücksichtigt.  Dieser Algorithmus ist *nicht* Teil dieses Auftrags.  Die generierten Rätsel werden statisch im Code gespeichert oder durch einen separaten Prozess generiert und dann in das Spiel geladen.
*   **Browser-Kompatibilität:** Das Spiel soll in modernen Browsern (Chrome, Firefox, Safari, Edge) funktionieren.
*   **Kein Backend:**  Alle Spielzustände werden lokal im Browser gespeichert (z.B. mit `localStorage`).
*   **Benutzeroberfläche:** Die Benutzeroberfläche wird mit HTML, CSS und JavaScript implementiert.  Es wird kein Framework vorausgesetzt.
*   **Fehlerbehandlung:**  Es wird davon ausgegangen, dass grundlegende Fehlerbehandlung implementiert wird, um unerwartete Zustände zu vermeiden (z.B. ungültige Eingaben).
*   **Eindeutigkeit der Lösung:**  Der Sudoku-Generator garantiert, dass jedes Rätsel genau eine Lösung hat.
*   **Responsive Design:** Das Spiel soll auf verschiedenen Bildschirmgrößen (Desktop, Tablet, Smartphone) spielbar sein.

### 3. Quellen

*   **JavaScript Documentation:** [https://developer.mozilla.org/en-US/docs/Web/JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) – Für die JavaScript-Implementierung.
*   **HTML Documentation:** [https://developer.mozilla.org/en-US/docs/Web/HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) – Für die HTML-Struktur.
*   **CSS Documentation:** [https://developer.mozilla.org/en-US/docs/Web/CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) – Für das CSS-Styling.
*   **localStorage API:** [https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) – Für das Speichern des Spielstands.
*   Keine gesicherte Quelle für Sudoku-Generierungsalgorithmen.

**Zusätzliche Hinweise basierend auf 02-pruefung.md:**

*   **Konfliktprüfung:** Die Konfliktprüfung muss *sofort* erfolgen, während der Benutzer eingibt.  Verzögerte Konfliktprüfung (z.B. erst nach Klick auf "Prüfen") ist nicht ausreichend.
*   **Visuelle Unterscheidung:**  Vorgegebene Zahlen müssen klar von den Benutzereingaben unterscheidbar sein.
*   **Notizmodus:** Der Notizmodus muss optional sein und darf die Basisfunktionalität des Spiels nicht beeinträchtigen.
*   **Hinweis-Funktion:** Der Hinweis muss *nur einen* Schritt anzeigen und darf nicht das komplette Sudoku lösen.
*   **Lösung anzeigen:**  Die Anzeige der Lösung soll eine Warnung beinhalten, da sie als "Cheat" betrachtet werden kann.
*   **Fehlertoleranz:** Das Spiel muss robust gegenüber ungültigen Eingaben sein (z.B. Buchstaben anstelle von Zahlen).  Eine klare Fehlermeldung ist erforderlich.
*   **Performance:** Das Spiel sollte auch bei komplexen Sudokus und vielen Notizen flüssig laufen. Die Konfliktprüfung sollte performant sein.
*   **Zugänglichkeit:**  Berücksichtigen Sie Zugänglichkeitsaspekte wie Tastaturnavigation und Screenreader-Kompatibilität (sofern möglich im Rahmen des Auftrags).
