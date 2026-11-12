

## Spielablauf für ein Browser-Sudoku

Dieser Entwurf beschreibt einen Spielablauf für ein webbasiertes Sudoku, der auf den im Auftrag genannten Anforderungen basiert. Er behandelt die Eingabe, Fehleranzeige, Notizen und Hilfen.

**1. Empfehlung**

Der empfohlene Spielablauf zielt auf eine intuitive und benutzerfreundliche Erfahrung ab. Er kombiniert visuelle Hinweise mit klarer Fehleranzeige und optionalen Hilfen, um ein angenehmes Sudoku-Erlebnis zu bieten.

* **Startbildschirm:**
    * Auswahl des Schwierigkeitsgrads (Leicht, Mittel, Schwer).
    * Ein "Neues Spiel"-Button, der ein neues Rätsel generiert.
    * (Optional) Ein Button zum Löschen des aktuellen Rätsels.
* **Spielbereich:**
    * Ein 9x9 Raster, bestehend aus Zellen.
    * Zellen sollten visuell klar abgrenzt sein, z.B. durch Linien oder leicht unterschiedliche Hintergrundfarben.
    * Voreingefügte Zahlen sind deutlich hervorgehoben (z.B. fettgedruckt oder in einer anderen Farbe).
* **Eingabe:**
    * **Tastatur:** Ermöglicht die Eingabe von Zahlen (1-9) über die Tastatur.  Beim Drücken einer Ziffer wird diese in die aktuell ausgewählte Zelle eingefügt. Die Backspace-Taste soll die Zelle leeren.
    * **Touch:** Ermöglicht die Eingabe durch Tippen auf die Zellen.  Ein Zahlenfeld (Popup oder in einer separaten Zeile/Spalte) wird angezeigt, aus dem der Benutzer die gewünschte Ziffer auswählen kann.
    * **Zellenauswahl:** Die aktuell ausgewählte Zelle wird visuell hervorgehoben (z.B. durch einen Rahmen oder Hintergrundfarbe). Die Navigation erfolgt durch Pfeiltasten (Tastatur) oder durch Tippen (Touch).
* **Fehleranzeige:**
    * **Echtzeit-Prüfung:** Nach jeder Eingabe wird geprüft, ob Konflikte entstehen (doppelte Zahlen in Zeile, Spalte oder 3x3-Block).
    * **Visuelle Markierung:** Konflikte werden sofort visuell hervorgehoben.  Beispiel: Zellen mit konfliktbedingten Fehlern werden rot gefärbt.  Es sollte klar sein, *welche* Eingabe den Fehler verursacht.
* **Notizen (Bleistift-Modus):**
    * Eine separate "Notizen"-Schaltfläche aktiviert/deaktiviert den Notizen-Modus.
    * Im Notizen-Modus können mehrere kleine Zahlen (1-9) in eine Zelle geschrieben werden. Dies dient dazu, mögliche Kandidaten für die Lösung zu notieren.
    * Die Notizen sollten visuell unterschiedlich dargestellt werden als die eigentlichen, festen Zahlen (z.B. kleiner, grauer).
    * Im Notizen-Modus sollte die Tastatureingabe die Zahlen für die Notizen darstellen und nicht direkt in die Zelle schreiben.
* **Hilfen:**
    * **"Hinweis":**  Zeigt einen möglichen Kandidaten für eine Zelle an. Dies sollte eine begrenzte Anzahl (z.B. 3-5) mal pro Spiel verwendet werden können.
    * **"Alle Notizen":** Füllt automatisch die Notizen aller Zellen mit den möglichen Kandidaten aus.  Sollte nur einmal pro Spiel verwendet werden können.
    * **(Optional) "Überprüfen":** Überprüft das gesamte Spielfeld auf Fehler (wie die Echtzeit-Prüfung) und zeigt eine detaillierte Liste aller Fehler an.

**2. Annahmen**

* **Rätselgenerierung:** Die Generierung von Sudoku-Rätseln mit genau einer Lösung ist ein komplexes Thema. Wir gehen davon aus, dass eine zuverlässige Algorithmus für die Rätselgenerierung verwendet wird, der die geforderte Eindeutigkeit gewährleistet.
* **Frontend-Technologie:** Die Implementierung erfolgt mit HTML, CSS und JavaScript.
* **Keine Backend-Kommunikation:**  Das Spiel läuft vollständig im Browser, ohne Serverinteraktion.
* **Benutzerinterface:** Der Browser ist der einzige interaktionspunkt für den Benutzer.
* **Eindeutigkeit:** Jeder generierte Sudoku-Raetsel hat eine eindeutige Loesung.

**3. Quellen**

* **JavaScript:** Die Hauptprogrammiersprache für die Logik und Interaktion des Spiels. (Allgemeines Wissen)
* **HTML:** Für die Struktur des Spielbretts und der Bedienelemente. (Allgemeines Wissen)
* **CSS:** Für das Styling des Spielbretts und der Bedienelemente. (Allgemeines Wissen)
* **Sudoku-Algorithmen:** Allgemeine Prinzipien für Sudoku-Lösung und Rätselgenerierung, z.B. Backtracking. (Allgemeines Wissen)
* **keine gesicherte Quelle:** Informationen zu UI/UX Design von Sudoku-Spielen.
* **keine gesicherte Quelle:** Best Practices für Validierung und Fehleranzeige in Webanwendungen.

--- 02-pruefung.md ---

## Einwände und Ergänzungen zum Spielablauf (basierend auf 02-pruefung.md)

Die folgende Liste beinhaltet Einwände und notwendige Ergänzungen zum oben genannten Spielablauf, die aus der Prüfung (02-pruefung.md) hervorgehen.

* **Fehleranzeige Detailtiefe:** Die einfache Rotfärbung von Zellen ist nicht ausreichend.  Die Fehleranzeige muss *präzise* sein und dem Benutzer mitteilen, *welchen* Konflikt die Zelle erzeugt (z.B. "Doppelte Zahl 5 in Zeile 3").
* **Notizen Modus und Eingabe:** Es muss sichergestellt werden, dass im Notizen-Modus die Zahlen nicht versehentlich als "echte" Zelleingaben interpretiert werden.  Ein dedizierter Modus-Umschalter ist entscheidend.
* **Undo-Funktion:** Das Fehlen einer Undo-Funktion wurde bemängelt. Eine Undo-Funktion, die mehrere Schritte zurückgeht, ist erforderlich, um Fehler zu korrigieren.
* **Timer:** Ein Timer kann die Spielerfahrung verbessern. Dies sollte optional sein und kann über eine Einstellung aktiviert/deaktiviert werden.
* **Schwierigkeitsgrade:** Die Implementierung der Schwierigkeitsgrade muss durch eine entsprechende Anpassung der Rätselgenerierung erfolgen (Anzahl der vorgegebenen Zahlen).
* **Visuelle Klarheit:** Die Unterscheidung zwischen vorgegebenen Zahlen und Eingabefeldern muss auch für farbenblindes Publikum zugänglich sein. Verwendung von unterschiedlichen Schriftarten oder -stilen zusätzlich zu Farben.
* **Performance:** Bei der Verwendung von JavaScript muss auf eine optimierte Performance geachtet werden, besonders bei der Echtzeit-Prüfung und der automatischen Notizenerstellung.

**Aktualisierter Spielablauf (Integration der Einwände):**

* **Fehleranzeige (verbessert):** Bei einem Fehler wird ein Popup oder eine kleine Nachricht direkt neben der fehlerhaften Zelle angezeigt, die den Konflikt genau beschreibt (z.B. "Doppelte Zahl 7 in Zeile 5").
* **Notizen Modus (präzisiert):**  Ein klarer Schalter ("Notizen On/Off") aktiviert/deaktiviert den Notizen-Modus.  Die Eingabe im Notizen-Modus erfolgt über eine separate Eingabemaske (virtuelle Tastatur oder Popup) oder durch direktes Tippen/Klicken, wobei die Eingabe *nur* als Notiz interpretiert wird.
* **Undo-Funktion:** Ein "Undo"-Button (oder Tastenkombination) ermöglicht das Rückgängigmachen der letzten Eingabe(n) (z.B. die letzten 10 Züge).
* **Timer (optional):** Ein optionaler Timer kann im Einstellungsmenü aktiviert werden.
* **Schwierigkeitsgrade (verbessert):** Die Rätselgenerierung wird so angepasst, dass leicht, mittel und schwer unterschiedliche Schwierigkeitsgrade durch die Anzahl der vorgegebenen Zahlen realisieren.
* **Visuelle Klarheit (verbessert):**  Vorgegebene Zahlen werden nicht nur durch Farbe, sondern auch durch einen anderen Schriftstil (z.B. fett, serifenlos) gekennzeichnet, um auch für Personen mit Farbsehschwäche erkennbar zu sein.
* **Performance (Hinweis):**  Bei der Implementierung der Echtzeit-Prüfung und der automatischen Notizenerstellung ist auf effizienten JavaScript-Code zu achten, um die Performance zu gewährleisten.
