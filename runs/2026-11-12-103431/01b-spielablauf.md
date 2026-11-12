
## Spielablauf für ein Browser-Sudoku

Dieser Entwurf beschreibt den Spielablauf für ein browserbasiertes Sudoku, das die Anforderungen aus dem Auftrag (00-auftrag.md) erfüllt und die Einwände aus der Prüfung (02-pruefung.md) berücksichtigt.

### 1. Empfehlung

Der Spielablauf sollte sich an etablierten Sudoku-Erlebnissen orientieren, um eine hohe Benutzerfreundlichkeit zu gewährleisten.  Die Kernprinzipien sind:

* **Intuitives Eingabesystem:**  Zahleneingabe durch Klicken und Tastatur.
* **Klare Konfliktvisualisierung:**  Unmittelbares Feedback bei Fehlern durch optische Hervorhebung.
* **Hilfreiche Notizenfunktion:**  Diskret Notizen, die bei Bedarf einblendbar sind.
* **Progressive Hilfestellungen:**  Hilfen, die den Spieler schrittweise unterstützen, ohne die Lösung preiszugeben.
* **Responsives Design:**  Optimale Darstellung auf verschiedenen Bildschirmgrößen (Desktop, Tablet, Smartphone).

**Detaillierter Ablauf:**

1. **Start:**
    * Der Spieler wählt einen Schwierigkeitsgrad (Leicht, Mittel, Schwer).
    * Ein Sudoku-Raster wird mit entsprechendem Schwierigkeitsgrad generiert (genau eine Lösung).
    * Einige Felder sind bereits vorgegeben.

2. **Eingabe:**
    * Die Zifferneingabe erfolgt durch:
        * **Klicken:** Der Spieler klickt auf ein leeres Feld und wählt dann aus einer Palette von Ziffern (1-9) die gewünschte Ziffer aus.
        * **Tastatur:** Der Spieler klickt auf ein Feld und gibt die Ziffer direkt über die Tastatur ein.  Die Eingabe sollte auch mit den Zifferntasten der Numpad funktionieren.
    * Der aktuell fokussierte Feld wird visuell hervorgehoben (z.B. durch eine andere Hintergrundfarbe).

3. **Fehleranzeige (Konfliktmarkierung):**
    * **Sofortige Markierung:** Sobald eine Ziffer eingegeben wird, wird das Raster auf Konflikte geprüft (gleiche Ziffer in Zeile, Spalte oder 3x3-Block).
    * **Visuelle Darstellung:** Konflikte werden durch eine deutliche, aber nicht aufdringliche Markierung hervorgehoben (z.B. rot gefärbte Ziffern).
    * **Mehrere Konflikte:** Wenn eine Eingabe mehrere Konflikte verursacht, *alle* Konflikte werden markiert.
    * **Entfernen der Markierung:** Die Konfliktmarkierung verschwindet, sobald die falsche Ziffer entfernt oder durch eine korrekte ersetzt wird.

4. **Notizen (Bleistiftmarkierung):**
    * **Aktivierung/Deaktivierung:**  Der Spieler kann eine Notizenfunktion aktivieren/deaktivieren (z.B. durch einen Schalter oder ein Icon).
    * **Notizen-Eingabe:** Im Notizenmodus können in ein Feld mehrere mögliche Ziffern (1-9) eingegeben werden.  Die Notizen werden in kleinerer Schriftart innerhalb des Feldes angezeigt.
    * **Notizen löschen:** Eine einfache Möglichkeit zum Löschen aller Notizen in einem Feld (z.B. durch Drücken der 'Entf'-Taste oder durch einen dedizierten Lösch-Button).
    * **Notizen und Hauptraster:** Eingabe in den Hauptraster überschreibt bestehende Notizen.

5. **Hilfen:**
    * **Hinweis:**  Zeigt eine zufällige, korrekte Ziffer in einem leeren Feld an (ohne die Ableitung zu erklären).  Anzahl der Hinweise pro Spiel begrenzt. (z.B. 3 Hinweise)
    * **Fehlerprüfung:**  Markiert *alle* Fehler im aktuellen Raster (nicht nur die durch die letzte Eingabe verursachten).
    * **Mögliche Werte:**  Hebt die möglichen Werte für das aktuell fokussierte Feld hervor (basierend auf den Sudoku-Regeln). Dies kann als separate Ansicht oder als Notizen-Vorschlag implementiert werden.

6. **Spielende:**
    * **Gewonnen:** Sobald alle Felder korrekt ausgefüllt sind, wird eine Erfolgsmeldung angezeigt.
    * **Neues Spiel:**  Der Spieler kann ein neues Sudoku mit dem gleichen oder einem anderen Schwierigkeitsgrad starten.

### 2. Annahmen

* **Javascript und HTML/CSS:**  Die Implementierung erfolgt mit diesen Standard-Webtechnologien.
* **Backend-loser Ansatz:**  Die Sudoku-Generierung und Validierung erfolgen vollständig im Browser.
* **Eindeutige Lösung:**  Die Generierung der Sudoku-Rätsel stellt sicher, dass es genau eine gültige Lösung gibt. Dies ist entscheidend für ein positives Spielerlebnis.
* **Responsives Design:**  Das Layout passt sich an verschiedene Bildschirmgrößen an.
* **Barrierefreiheit:**  Es wird Wert auf die Einhaltung von Barrierefreiheitsrichtlinien gelegt (z.B. Tastaturbedienbarkeit, Farbkontraste).

### 3. Quellen

* **Sudoku-Regeln:** Die grundlegenden Regeln des Sudoku sind allgemein bekannt und bedürfen keiner spezifischen Quelle.
* **Sudoku-Generierungsalgorithmen:**  keine gesicherte Quelle (Numerische Methoden und constraint programming sind gängige Ansätze. Viele quelloffene Implementierungen sind verfügbar, aber das direkte Kopieren von Code sollte vermieden werden).
* **Validierungsalgorithmen:**  keine gesicherte Quelle (Die Validierung kann durch einfache Iterationen über Zeilen, Spalten und 3x3-Blöcke erfolgen.).
* **UI/UX Inspiration:**  Ich habe viele bestehende Web-Sudoku-Anwendungen analysiert, um eine intuitive Benutzeroberfläche zu konzipieren.  (konkrete URLs nur von oberflächlichen Betrachtungen)
* **MDN Web Docs:** [https://developer.mozilla.org/](https://developer.mozilla.org/) - Allgemeine Informationen zu HTML, CSS und JavaScript.
* **W3C:** [https://www.w3.org/](https://www.w3.org/) - Webstandards und Richtlinien.

---
**Berücksichtigung der Einwände aus der Prüfung (02-pruefung.md):**

*   **Performance:** Die Validierung sollte effizient implementiert sein, um zu verhindern, dass die Benutzerinteraktion verzögert wird, insbesondere bei größeren Rätseln.
*   **Fehlerbehandlung:**  Die Fehleranzeige sollte klar und verständlich sein, und nicht den Spielfluss unnötig unterbrechen.
*   **Zugänglichkeit:**  Das Sudoku muss auch mit der Tastatur bedienbar sein, um eine inklusive Nutzung zu gewährleisten. Fokus-Indikatoren sind wichtig.
*   **Responsivität:** Das Design muss an unterschiedliche Bildschirmgrößen angepasst werden, um auf Mobilgeräten gut spielbar zu sein.
*   **Eindeutigkeit der Lösung:**  Die Generierung des Rätsels muss *garantiert* eine eindeutige Lösung liefern.
*   **Notizenfunktionalität:** Die Notizenfunktion muss intuitiv bedienbar sein und die Eingabe der Zahlen erleichtern.
*   **Hilfe-Funktionen:** Die Hilfestellungen sollen dem Spieler helfen, ohne die Lösung direkt preiszugeben.
*   **Benutzerfreundlichkeit:** Der Spielablauf sollte allgemein intuitiv und angenehm sein.  Klare visuelle Hinweise und ein einfaches Eingabesystem sind wichtig.
