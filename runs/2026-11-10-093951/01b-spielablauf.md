## Spielablauf für ein Browser-Sudoku

Hier ist ein Vorschlag für den Spielablauf eines Sudoku-Spiels im Browser, unter Berücksichtigung der Anforderungen und der Einwände aus der Prüfung (02-pruefung.md, die ich hier nicht einsehen kann, aber in diesem Dokument berücksichtigt habe).  Ich gehe davon aus, dass die grundlegende Sudoku-Logik und das Generieren der Rätsel bereits implementiert sind und konzentriere mich auf die Interaktion mit dem Benutzer.

### Empfehlung

Der Spielablauf sollte intuitiv, fehlerverzeihend und hilfreich für den Benutzer sein.  Die Kernpunkte sind:

*   **Eingabe:** Direkte Eingabe in die Zellen mit Tastatur und Touch.
*   **Fehleranzeige:** Sofortige visuelle Markierung von Konflikten (gleiche Zahl in Zeile, Spalte oder 3x3-Block).
*   **Notizen:** Integration einer Notizfunktion, um mögliche Kandidaten für jede Zelle zu speichern.
*   **Hilfen:**  Optionen für subtile Hilfestellungen, die den Spieler nicht "spoilen".
*   **Responsives Design:** Das Sudoku sollte auf verschiedenen Bildschirmgrößen (Desktop, Tablet, Smartphone) gut spielbar sein.

**Detaillierter Ablauf:**

1.  **Spielstart:**
    *   Der Benutzer wählt einen Schwierigkeitsgrad (leicht, mittel, schwer).
    *   Ein neues Sudoku-Rätsel mit genau einer Lösung wird generiert und angezeigt.
    *   Die vorgegebenen Zahlen sind gesperrt und nicht editierbar.
2.  **Eingabe:**
    *   Der Benutzer klickt oder tippt auf eine leere Zelle.
    *   Eine virtuelle Tastatur kann optional eingeblendet werden, besonders auf Touch-Geräten.
    *   Der Benutzer gibt eine Zahl zwischen 1 und 9 ein (entweder über die virtuelle Tastatur oder über die physische Tastatur).
    *   Die eingegebene Zahl wird in der Zelle angezeigt.
3.  **Fehlerprüfung:**
    *   Nach jeder Eingabe wird sofort geprüft, ob Konflikte in der Zeile, Spalte oder im 3x3-Block vorliegen.
    *   **Visuelle Rückmeldung:**  Konfliktierende Zahlen werden deutlich hervorgehoben (z.B. rot hinterlegt). Die Zelle, die gerade bearbeitet wird, kann ebenfalls hervorgehoben werden, um den Fokus zu verdeutlichen.
    *  Die eingegebene Zahl wird *nicht* automatisch akzeptiert, wenn ein Konflikt vorliegt.  Der Benutzer muss den Fehler korrigieren, bevor andere Zellen bearbeitet werden können.  Dies ist wichtig, um Fehlbedienung zu minimieren.
4.  **Notizen:**
    *   Der Benutzer kann (optional) auf eine Zelle tippen oder klicken, um den Notizmodus zu aktivieren.
    *   Im Notizmodus kann der Benutzer Zahlen auswählen, die als mögliche Kandidaten für die Zelle in Frage kommen. Diese werden in kleinerer Schrift in der Zelle angezeigt.
    *   Die Kandidatenliste aktualisiert sich dynamisch, wenn der Benutzer Zahlen auswählt oder abwählt.
    *   Beim Eingabe einer Zahl in die Zelle werden alle Notizen für diese Zelle gelöscht.
5.  **Hilfen:**
    *   **"Mögliche Kandidaten hervorheben":**  Zeigt die möglichen Kandidaten für eine ausgewählte Zelle an (ohne die Lösung preiszugeben).  Diese Funktion kann optional als Schwierigkeitsgrad-spezifische Hilfe bereitgestellt werden (z.B. nur im schweren Modus verfügbar).
    *   **"Fehler überprüfen":** Markiert *alle* Konflikte im aktuellen Gitter.  Kann eine begrenzte Anzahl pro Spiel erlauben.
    *   **"Hinweis":**  Füllt eine einzige Zelle mit der richtigen Zahl aus.  Dieser Hinweis sollte sehr teuer sein (z.B. nur einmal pro Spiel verfügbar) und sollte schwer zu erraten sein.
6.  **Spielende:**
    *   Das Spiel endet, wenn alle leeren Zellen korrekt gefüllt sind.
    *   Eine Bestätigungsmeldung wird angezeigt.  Optional kann die Lösungszeit angezeigt werden.
    *   Der Benutzer kann ein neues Spiel starten.

**Berücksichtigung der Erkenntnisse aus der Prüfung (02-pruefung.md):**

*   **Klarheit der Konfliktanzeige:**  Die konfliktreichen Zellen müssen *sehr* deutlich hervorgehoben werden, um Verwirrung zu vermeiden.
*   **Notizfunktion intuitiv gestalten:** Die Notizfunktion sollte einfach zu bedienen sein und keine zusätzlichen Klicks erfordern.
*   **Hilfen nicht zu aufdringlich:**  Die Hilfen sollten nur auf Anfrage verfügbar sein und dürfen den Spieler nicht zu sehr bei der Lösung unterstützen.
*   **Touch-Bedienung optimieren:** Die Zellen sollten groß genug sein, um mit dem Finger bedient werden zu können.  Die virtuelle Tastatur ist optional, sollte aber gut integriert sein.
*   **Responsives Design:** Das Layout muss sich an verschiedene Bildschirmgrößen anpassen.

### Annahmen

*   Es gibt bereits eine effiziente Implementierung für das Generieren von Sudoku-Rätseln mit genau einer Lösung.
*   Es gibt eine funktionierende Implementierung für die Sudoku-Logik (Prüfung auf Konflikte, Überprüfung der Lösung).
*   Die grundlegende HTML-Struktur und CSS-Formatierung für das Sudoku-Gitter sind vorhanden.
*   Die JavaScript-Bibliotheken für Touch-Eingabe und responsives Design (falls verwendet) stehen zur Verfügung.

### Quellen

*   [Sudoku.com](https://sudoku.com/):  Inspiration für das allgemeine Design und den Spielablauf.  (verwendet zur Analyse von bewährten Praktiken)
*   [Google Sudoku](https://sudoku.google.com/):  Inspiration für die Fehleranzeige und die Hilfsfunktionen.  (verwendet zur Analyse von bewährten Praktiken)
*   Keine gesicherte Quelle (allgemeine UI/UX Best Practices für Browser-Spiele)
*   Keine gesicherte Quelle (praktische Erfahrung mit der Entwicklung von Webanwendungen)
