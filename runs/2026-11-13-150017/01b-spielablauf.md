
## Spielablauf für ein Browser-Sudoku

Dieses Dokument beschreibt einen empfohlenen Spielablauf für ein browserbasiertes Sudoku, unter Berücksichtigung der im Auftrag genannten Anforderungen und der Einwände aus der Prüfung (02-pruefung.md).

### Empfehlung

Der Spielablauf sollte wie folgt aussehen:

1.  **Rätselauswahl:**
    *   Der Spieler wählt einen Schwierigkeitsgrad (leicht, mittel, schwer) aus.
    *   Ein entsprechendes Sudoku-Rätsel wird generiert und im Gitter dargestellt. Die Generierung muss sicherstellen, dass das Rätsel *genau eine* Lösung hat.
    *   Optional: Ein Button zum Generieren eines neuen Rätsels desselben Schwierigkeitsgrades.

2.  **Eingabe:**
    *   **Zellen-Auswahl:** Der Spieler kann Zellen über Tastatur (Pfeiltasten/Tab) oder durch Klicken/Tippen auswählen.  Die aktuell ausgewählte Zelle sollte optisch hervorgehoben sein (z.B. durch eine farbliche Umrandung).
    *   **Zahlen-Eingabe:**
        *   Tastatur: Eingabe der Zahlen 1-9 über die Tastatur.  Die ausgewählte Zelle wird mit der eingegebenen Zahl befüllt.
        *   Touch:  Ein Zahlenfeld (z.B. als Buttons) wird angezeigt, aus dem der Spieler die Zahl auswählen kann.
        *   Löschen:  Eine Möglichkeit zum Löschen des Wertes in der aktuell ausgewählten Zelle (z.B. mit der Backspace-Taste oder einem "Löschen"-Button).

3.  **Fehleranzeige (Konflikte):**
    *   **Echtzeit-Konflikterkennung:** Während der Eingabe werden Konflikte sofort überprüft.
    *   **Visuelle Markierung:** Bei Konflikten (d.h. wenn eine Zahl in einer Zeile, Spalte oder einem 3x3-Block mehrfach vorkommt) werden die *konfliktierenden* Zellen hervorgehoben (z.B. rot umrandet oder rot gefärbt).  Es sollte klar sein, welche Zellen den Konflikt verursachen.
    *   **Keine explizite Meldung:** Eine explizite Fehlermeldung ("Ungültige Eingabe!") ist *nicht* notwendig, solange die visuelle Markierung klar und deutlich ist.

4.  **Notizen (Bleistiftmarkierungen):**
    *   **Aktivierung/Deaktivierung:** Eine Taste oder ein Button (z.B. "Notizen") schaltet den Notizen-Modus ein und aus.
    *   **Notizen-Eingabe:** Im Notizen-Modus funktionieren die Zahlen-Eingabemethoden wie bei der normalen Eingabe, jedoch werden die Zahlen *klein* und *dezent* in die Zellen geschrieben (z.B. oben rechts in der Zelle).  Diese Notizen repräsentieren mögliche Werte für die Zelle.
    *   **Mehrere Notizen pro Zelle:**  Es sollte möglich sein, mehrere Notizen in einer Zelle zu speichern.
    *   **Notizen-Modus-Anzeige:** Der Spieler sollte visuell erkennen, ob der Notizen-Modus aktiv ist (z.B. durch eine geänderte Cursor-Darstellung oder eine Statusleiste).
    *   **Notizen löschen:** Eine einfache Möglichkeit zum Löschen einzelner Notizen oder aller Notizen in einer Zelle.

5.  **Hilfen:**
    *   **"Zeige Fehler":**  Markiert alle aktuellen Konflikte im Spiel (auch wenn sie gerade nicht aktiv editiert werden).
    *   **"Zeige mögliche Werte":** Zeigt für die aktuell ausgewählte Zelle alle möglichen Werte an, die in diese Zelle eingetragen werden können, ohne einen Konflikt zu verursachen. Diese Werte werden dezent angezeigt (z.B. als kleine Zahlen am Rand der Zelle).
    *   **Keine Lösungsvorschläge:** Das Spiel soll *keine* direkten Lösungsvorschläge geben, sondern lediglich den Spieler bei der Analyse unterstützen.

6.  **Spielende:**
    *   **Automatische Überprüfung:** Das Spiel prüft automatisch, ob das Sudoku gelöst ist.
    *   **Erfolgsmeldung:**  Wenn das Sudoku korrekt gelöst wurde, wird eine Erfolgsmeldung angezeigt (z.B. "Glückwunsch! Du hast das Sudoku gelöst!").
    *   **Neues Spiel:** Button zum Starten eines neuen Spiels.

### Annahmen

*   **Browser-Kompatibilität:** Das Spiel soll in modernen Browsern (Chrome, Firefox, Safari, Edge) funktionieren.
*   **Kein Backend:**  Alle Operationen (Rätselgenerierung, Fehlerprüfung, etc.) erfolgen clientseitig.
*   **JavaScript als Haupttechnologie:**  JavaScript wird verwendet, um die Spiellogik und die Interaktion mit dem Benutzer zu implementieren.  CSS wird für das Styling verwendet.  HTML für die Struktur.
*   **Benutzerfreundlichkeit:** Das Design und die Interaktionen sind intuitiv und einfach zu verstehen.
*   **Performance:** Die Generierung und Überprüfung der Rätsel erfolgen schnell genug, um eine flüssige Spielerfahrung zu gewährleisten.

### Quellen

*   **JavaScript MDN Web Docs:** [https://developer.mozilla.org/en-US/docs/Web/JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) (Grundlegende JavaScript-Konzepte)
*   **CSS MDN Web Docs:** [https://developer.mozilla.org/en-US/docs/Web/CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) (Grundlegende CSS-Konzepte)
*   **HTML MDN Web Docs:** [https://developer.mozilla.org/en-US/docs/Web/HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) (Grundlegende HTML-Konzepte)
*   **Sudoku-Algorithmen und -Lösungsstrategien:** Viele Informationen sind online verfügbar, jedoch keine gesicherte Quelle im Sinne einer wissenschaftlichen Arbeit.  Ich habe mich mit verschiedenen Verfahren zur Rätselgenerierung und -prüfung vertraut gemacht (Backtracking, Constraint Programming), ohne diese jedoch vollständig zu implementieren.
*   **Keine gesicherte Quelle** (für Algorithmen und generelle Spielkonzepte)

---

**Berücksichtigung der Einwände aus 02-pruefung.md:**

Die Prüfung (02-pruefung.md) hat folgende Einwände erhoben:

*   **Performance bei Konfliktprüfung:** Die Konfliktprüfung sollte performant sein, insbesondere bei vielen Eingaben.  *Empfehlung:* Die Konfliktprüfung sollte bei jeder Eingabe durchgeführt werden, aber optimiert implementiert werden, um die Performance zu gewährleisten. Ein effizienter Ansatz ist die Überprüfung nur der relevanten Zeilen, Spalten und 3x3-Blöcke bei jeder Eingabe, anstatt das gesamte Gitter zu durchlaufen.
*   **Notizen-Modus ohne klare Kennzeichnung:** Der Notizen-Modus sollte für den Benutzer klar erkennbar sein. *Empfehlung:* Eine visuelle Kennzeichnung (z.B. ein Symbol oder eine Statusleiste) wird hinzugefügt, um den Zustand des Notizen-Modus anzuzeigen.
*   **Hilfen zu umfassend:** Die Hilfen sollten nicht direkt Lösungsvorschläge liefern. *Empfehlung:*  Es wird kein Button zum direkten Erraten der Lösung implementiert.  Die Hilfen "Zeige Fehler" und "Zeige mögliche Werte" werden beibehalten, da sie dem Benutzer helfen, das Rätsel selbst zu lösen.
*   **Fehlende Eingabehilfe für Touch-Geräte:** Eingabe per Touch sollte berücksichtigt werden. *Empfehlung:*  Ein Zahlenfeld mit Touch-freundlichen Buttons wird hinzugefügt.

Diese Einwände wurden in die obige Empfehlung eingearbeitet.
