
## Spielablauf für ein Browser-Sudoku

Dieser Dokument beschreibt den empfohlenen Spielablauf für ein Browser-basiertes Sudoku, unter Berücksichtigung des Auftrags und der Einwände aus der Prüfung (02-pruefung.md).

### Empfehlung

Der Spielablauf soll sich an klassischen Sudoku-Spielen orientieren, aber für eine komfortable Nutzung im Browser optimiert werden.

1. **Spielstart & Schwierigkeitsgrad:**
   - Der Spieler wählt beim Start einen Schwierigkeitsgrad (leicht, mittel, schwer).
   - Ein entsprechendes Sudoku-Rätsel wird generiert und im 9x9-Gitter angezeigt.  Die Rätsel sollen *genau eine* Lösung haben (dies ist essentiell und muss sichergestellt werden).
   - Die bereits vorgegebenen Zahlen sind nicht editierbar und optisch klar vom bedienbaren Feld abgegrenzt (z.B. durch andere Farbe, Fettdruck oder Rahmen).

2. **Eingabe:**
   - **Tastatur:**  Ziffern 1-9 füllen das aktuell selektierte Feld.  Die Pfeiltasten navigieren durch die Felder.  `Entf` oder `Backspace` löschen den Inhalt des aktuellen Feldes.
   - **Touch:**  Ein Tipp auf ein Feld selektiert es.  Anschließend kann über eine virtuelle Tastatur (Ziffern 1-9 und Löschtaste) eingegeben werden. Alternativ soll die direkte Eingabe über Touch (also direkt auf das Feld schreiben) ebenfalls möglich und intuitiv sein.
   - **Selektierung:** Das aktuell selektierte Feld wird visuell hervorgehoben (z.B. durch einen Rahmen oder eine Hintergrundfarbe).
   - **Eingabefeld-Fokus:** Der Fokus sollte automatisch auf das erste leere Feld gesetzt werden.

3. **Fehleranzeige (Konfliktprüfung):**
   - **Echtzeit-Validierung:** Bei jeder Eingabe wird geprüft, ob Konflikte in der Zeile, Spalte oder im 3x3-Block entstehen.
   - **Visuelle Markierung:**  Konflikte werden *sofort* durch eine klare visuelle Markierung angezeigt.  Empfehlung:  Die betreffenden Felder (sowohl das aktuell editierte Feld als auch die mit ihm in Konflikt stehenden Felder) werden rot umrandet oder rot hervorgehoben. Die Markierung soll während eines Eingabevorgangs bestehen bleiben, bis der Konflikt behoben ist, oder der Nutzer das Feld verlässt.
   - **Keine blockierende Meldung:**  Es soll *keine* Popup-Meldung oder ähnliches erscheinen, die die Eingabe unterbricht. Die visuelle Markierung ist ausreichend.

4. **Notizen (Bleistiftmarkierungen):**
   - **Aktivierung/Deaktivierung:**  Eine Schaltfläche oder ein Tastenkürzel toggelt den "Notizen-Modus".
   - **Eingabe:** Im Notizen-Modus führt die Eingabe einer Ziffer in ein Feld dazu, dass diese als kleine, gedämpfte Zahl in der oberen linken Ecke des Feldes angezeigt wird. Mehrere Ziffern können in einem Feld notiert werden.
   - **Löschen:** Im Notizen-Modus löscht `Entf` oder `Backspace` die aktuelle Notiz in dem Feld.
   - **Darstellung:** Die Notizen sollen klar von den festen Zahlen unterschieden sein und nicht mit der eigentlichen Eingabe interagieren.
   - **Notizen-Modus-Indikator:**  Ein visueller Indikator (z. B. eine farblich hervorgehobene Schaltfläche) zeigt an, ob der Notizen-Modus aktiv ist.

5. **Hilfen:**
   - **Hinweis:** Eine Schaltfläche "Hinweis" gibt einen Tipp. Der Hinweis soll eine einzige, korrekte Ziffer für ein leeres Feld vorschlagen.  Die vorgeschlagene Ziffer wird kurzzeitig hervorgehoben (z.B. blinkend oder mit einem anderen Hintergrund).
   - **Anzahl Hinweise begrenzt:** Die Anzahl der verfügbaren Hinweise sollte begrenzt sein (z.B. 3 pro Spiel) um den Schwierigkeitsgrad zu wahren.
   - **Auffüllen von Notizen schrittweise:** Eine Hilfefunktion "Notizen vorschlagen" kann mögliche Notizen für leere Felder auflisten, basierend auf den aktuellen Zahlen. Dies sollte nicht automatisch alle Notizen eintragen, sondern dem Benutzer helfen, selbst zu deduzieren.

6. **Spielende:**
   - **Überprüfung auf Lösung:** Eine Schaltfläche "Prüfen" überprüft, ob das Sudoku korrekt gelöst ist.
   - **Gewinn-Animation:** Bei korrekter Lösung erfolgt eine Gewinn-Animation oder eine Meldung.
   - **Neues Spiel:** Möglichkeit, ein neues Spiel mit demselben oder einem anderen Schwierigkeitsgrad zu starten.

**Berücksichtigung der Einwände aus 02-pruefung.md:**

* **Fehler-Visulisierung:** Die Einwände bezüglich der deutlichen Erkennbarkeit der Fehler wurden berücksichtigt. Durch die sofortige und eindeutige rote Markierung von konfliktbehafteten Feldern wird eine deutliche Visualisierung gewährleistet.
* **Notizen-Modus:** Der Notizen-Modus wurde detaillierter definiert, insbesondere hinsichtlich der Eingabe, Löschung und Darstellung, um eine intuitive Bedienung zu bieten.
* **Hilfen:** Die Hilfen wurden auf einen Hinweis und eine "Notizen vorschlagen"-Funktion limitiert, um ein zu leichtes Lösen zu vermeiden.
* **Keine Blockierung der Eingabe:** Es wird keine Modal- oder Alert-Box zur Fehleranzeige verwendet.

### Annahmen

*   Der Browser unterstützt moderne JavaScript-Features.
*   Der Benutzer hat grundlegende Kenntnisse über die Regeln des Sudoku.
*   Es wird kein Backend benötigt, d.h. die Rätselgenerierung und -prüfung erfolgt clientseitig.
*   Es wird ein responsives Design verwendet, so dass das Spiel auf verschiedenen Bildschirmgrößen spielbar ist.

### Quellen

*   [https://de.wikipedia.org/wiki/Sudoku](https://de.wikipedia.org/wiki/Sudoku) – Grundregeln und Informationen zum Sudoku
*   keine gesicherte Quelle (Implementierung von Sudoku-Algorithmen und Benutzeroberflächen, inspiriert von zahlreichen Online-Sudoku-Spielen).
