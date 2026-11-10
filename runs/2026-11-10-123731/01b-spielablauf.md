
## Spielablauf für ein Browser-Sudoku

### Empfehlung

Der Spielablauf sollte sich an etablierten Sudoku-Erlebnissen orientieren, aber die Besonderheiten des Browsers (Tastatur, Touch) berücksichtigen.  Hier ist ein Vorschlag:

1.  **Startbildschirm:** Auswahl des Schwierigkeitsgrads (leicht, mittel, schwer).  Nach Auswahl wird ein neues Sudoku-Rätsel generiert und angezeigt.  Ein "Neues Spiel"-Button sollte im Spiel verfügbar sein.

2.  **Sudoku-Gitter-Anzeige:**
    *   Ein 9x9 Gitter, das visuell in 3x3 Blöcke unterteilt ist.
    *   Vorhandene Zahlen (gegebene Werte) sind dunkler/fettgedruckt dargestellt und nicht editierbar.
    *   Benutzereingaben sind in einer anderen Farbe und Schriftart.
    *   Aktuell selektierte Zelle wird hervorgehoben (z.B. durch eine Rahmenauszeichnung).

3.  **Eingabe:**
    *   **Tastatur:**  Durch Klicken auf eine Zelle und anschließendes Tippen der Ziffer (1-9) kann der Wert in diese Zelle eingetragen werden.  Die Taste 'Entf' oder 'Backspace' sollte die Zelle leeren.  Pfeiltasten navigieren zwischen den Zellen.
    *   **Touch:** Tippen auf eine Zelle aktiviert sie.  Ein Overlay mit den Ziffern 1-9 erscheint (entweder als numerische Tastatur oder als separate Buttons).  Durch Tippen auf eine Ziffer wird diese in die Zelle eingetragen.  Wischen kann für die Navigation verwendet werden, ist aber optional und potenziell weniger präzise.
    *   **Eingabebeschränkung:**  Nur Ziffern von 1-9 sollten akzeptiert werden.  Alle anderen Eingaben werden ignoriert.

4.  **Fehleranzeige:**
    *   **Sofortige Überprüfung:**  Bei jeder Eingabe wird geprüft, ob sie zu einem Konflikt (gleiche Ziffer in der gleichen Zeile, Spalte oder 3x3 Block) führt.
    *   **Visuelle Markierung:**  Konflikte werden durch visuelle Markierung hervorgehoben.  Beispielsweise können die konfliktbehafteten Zellen rot gefärbt werden.
    *   **Keine Unterdrückung der Eingabe:** Die Eingabe soll nicht verhindert werden, aber der Fehler soll sofort angezeigt werden.  Dies ermöglicht dem Benutzer, Fehler zu erkennen und selbst zu korrigieren.

5.  **Notizen (Bleistiftmarkierungen):**
    *   **Aktivierung/Deaktivierung:**  Ein Button oder ein Toggle-Schalter, um den Notiz-Modus ein- und auszuschalten.
    *   **Eingabe:** Im Notiz-Modus kann durch Klicken auf eine Zelle oder ausschreibenucht mit der Tastatur auf eine Zelle, und anschließendes Tippen der Ziffer, diese als kleine Notiz in die Zelle hinzugefügt werden. Mehrere Notizen können in einer Zelle gespeichert werden.
    *   **Anzeige:** Notizen werden in kleiner Schriftart in den Ecken der Zelle angezeigt.
    *   **Löschen:**  Entfernen von Notizen entweder durch erneutes Klicken oder durch Tippen von 'Entf' / 'Backspace' im Notiz-Modus.

6.  **Hilfen:**
    *   **"Aufdecken"-Hilfe (optional):**  Ein Button, der einen einzelnen, korrekten Wert in einer zufälligen, leeren Zelle aufdeckt.  Begrenzte Anzahl an Aufdeckungen pro Spiel.
    *   **"Hinweis"-Hilfe (fortgeschritten):** (Optional) Zeigt eine logische Ableitung für eine Zelle an (z.B. "Die Ziffer 5 kann nur in dieser Zelle im 3x3 Block sein").  Diese Funktion sollte sehr begrenzt verfügbar sein oder kostenpflichtig sein, um das Lösen des Rätsels nicht zu trivialisieren.

7.  **Spielende:**
    *   **Überprüfung:** Ein "Prüfen"-Button, der das gesamte Sudoku-Gitter auf Korrektheit überprüft.
    *   **Gewinn:**  Wenn das Sudoku korrekt gelöst wurde, wird eine Gewinnmeldung angezeigt.
    *   **Neues Spiel:**  Ein Button, um ein neues Sudoku-Rätsel zu starten.
    *   **Timer (optional):** Anzeige der Spielzeit.

### Annahmen

*   **Browser-Kompatibilität:** Der Code sollte mit modernen Browsern (Chrome, Firefox, Safari, Edge) kompatibel sein.
*   **Kein Backend:** Alle Logik (Rätselgenerierung, Fehlerprüfung, Lösungsprüfung) findet im Browser statt.
*   **Benutzerfreundlichkeit:** Das Design und die Interaktionen sollten intuitiv und einfach zu bedienen sein.
*   **Leistung:**  Die Fehlerprüfung und Rätselgenerierung sollten schnell und effizient sein, um ein flüssiges Spielerlebnis zu gewährleisten.
*   **Einmalige Lösung:** Generierte Rätsel müssen stets eindeutig lösbar sein.

### Quellen

*   **Sudoku-Regeln:**  Allgemein bekanntes Wissen.
*   **JavaScript:** Für die Implementierung der Spiel-Logik und der Benutzerschnittstelle.
*   **HTML/CSS:** Für die Struktur und das Styling der Webseite.
*   **keine gesicherte Quelle:** Online-Sudoku-Spiele (als Inspiration für den Spielablauf und das visuelle Design).
*   **keine gesicherte Quelle:**  Algorithmen zur Sudoku-Rätselgenerierung (beschrieben in verschiedenen Online-Tutorials und Beiträgen – diese sind aber oft unvollständig oder fehlerhaft, daher vorsichtig zu behandeln).

---

**Einbindung der Einwände aus 02-pruefung.md:**

Die Prüfung (02-pruefung.md) wies auf Probleme mit der Eingabemaskierung, der Fehleranzeige und der Speed der Überprüfung hin. Daher sind folgende Anpassungen zu berücksichtigen:

*   **Eingabemaskierung:**  Eingaben, die keine Ziffern sind, sollten sofort verworfen werden, ohne sie im Feld anzuzeigen.  Dies verhindert Verwirrung, falls der Benutzer versehentlich eine ungültige Taste drückt.
*   **Fehleranzeige:**  Die Prüfung bemängelte, dass die Fehleranzeige beim schnellen Tippen nicht immer sofort sichtbar ist.  Die Fehlerprüfung sollte in jedem Fall *nach* jeder abgeschlossenen Eingabe durchgeführt werden, um sicherzustellen, dass der Benutzer immer eine korrekte Rückmeldung erhält. Es ist anzuerstreben, dass die visuelle Markierung *synchron* mit der Eingabe erscheint, auch wenn dies durch Debouncing (kurze Verzögerung) realisiert werden muss.
*   **Speed der Überprüfung:** Die Fehlerprüfung sollte optimiert werden, um schnell zu erfolgen, auch bei komplexen Rätseln.  Die Prüfung sollte nur die relevanten Zeilen, Spalten und 3x3 Blöcke überprüfen, in denen die gerade eingegebene Ziffer vorkommen könnte. Ein optimalisierter Algorithmus ist hier wichtig.  Die Prüfung empfiehlt, die Prüfung nicht nach jeder Taste, sondern erst nach einer vollständigen Zahl (1-9) durchzuführen, um die Last zu reduzieren.

Diese Punkte werden bei der Implementierung berücksichtigt, um die Benutzerfreundlichkeit und Performance zu verbessern.
