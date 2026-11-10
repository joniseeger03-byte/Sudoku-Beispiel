
# Spielablauf für ein Browser-Sudoku

## Empfehlung

Der Spielablauf sollte intuitiv und fehlerverzeihend sein, mit klarer visueller Rückmeldung. Hier ist eine empfohlene Struktur, unter Berücksichtigung der Anforderungen und potenzieller Verbesserungspunkte:

**1. Start und Schwierigkeitsgrad:**

*   **Begrüßungsbildschirm:** Einfaches Menü zur Auswahl des Schwierigkeitsgrads (Leicht, Mittel, Schwer).  Die Schwierigkeitsgrade sollten sich quantitativ in der Anzahl der vorgegebenen Zahlen und qualitativ in den Lösungswegen (einfache vs. komplexe Logik) unterscheiden.
*   **Generierung:**  Nach der Auswahl des Schwierigkeitsgrades wird ein Sudoku-Rätsel generiert, das genau eine Lösung hat.  (Details zur Generierung siehe "Annahmen".)

**2. Eingabe:**

*   **Zellen fokussieren:** Durch Klicken oder Tippen auf eine Zelle wird diese ausgewählt und hervorgehoben.  Die Navigation zwischen Zellen sollte mit den Pfeiltasten (hoch, runter, links, rechts) und Touch-Gesten möglich sein.
*   **Eingabe per Tastatur:**  Zahlen von 1-9 können direkt in die fokussierte Zelle eingegeben werden.  Die Taste "Entf" oder "Backspace" sollte die Zelle leeren.
*   **Eingabe per Touch:**  Es sollte eine numerische Tastatur (Overlay) eingeblendet werden, aus der die Ziffern ausgewählt werden können.  Alternativ kann Long-Press auf eine Zelle ein Kontextmenü mit den Ziffern 1-9 öffnen.
*   **Fokus-Indikator:** Eine klare visuelle Markierung (z.B. Rahmen, Hintergrundfarbe) zeigt an, welche Zelle gerade aktiv ist.

**3. Fehleranzeige (Konflikte):**

*   **Echtzeit-Überprüfung:** Jede Eingabe wird sofort auf Konflikte (gleiche Zahl in Zeile, Spalte oder 3x3-Block) überprüft.
*   **Visuelle Markierung:**  Konfliktreiche Zahlen werden sofort visuell hervorgehoben. Dies kann durch:
    *   Hervorhebung der Konflikt-Zelle selbst in Rot.
    *   Hervorhebung *aller* Zellen in Zeile, Spalte und/oder Block, die den Konflikt verursachen, in einem dezenten Rotton.
*   **Kein Blockieren der Eingabe:**  Der Spieler soll auch falsche Zahlen eingeben können, um zu experimentieren. Die Markierung soll lediglich auf den Fehler hinweisen.

**4. Notizen (Bleistift-Markierungen):**

*   **Aktivierung:** Ein Button oder eine andere Art von Toggle schaltet den Notizmodus ein/aus.
*   **Eingabe:** Im Notizmodus werden beim Tippen der Zahlen kleine Indikatoren (z.B. kleine Zahlen) in die Zelle eingefügt, die anzeigen, welche Zahlen der Spieler als mögliche Kandidaten betrachtet.  Mehrere Kandidaten können in einer Zelle gespeichert werden.
*   **Löschen:**  Im Notizmodus löscht die Eingabe einer Zahl („Entf“ oder “Backspace”) die betreffende Notiz.
*   **Visuelle Darstellung:** Die Notizen sollten klar und unaufdringlich dargestellt werden, z.B. in einer kleineren Schriftgröße oder einer anderen Farbe.
*   **Aktualisierung nach Löschen:** Wenn der Spieler eine Zahl in eine Zelle eingibt, die vorher Notizen enthielt, sollten die Notizen automatisch gelöscht werden.

**5. Hilfen:**

*   **"Hinweis" Funktion:**  Bietet einen Hinweis, indem eine korrekte Zahl in einer Zelle vorgegeben wird. Die Anzahl der Hinweise sollte begrenzt sein, möglicherweise pro Schwierigkeitsgrad unterschiedlich.
*   **"Fülle Zeilen/Spalten/Block" Funktion:** Markiert die möglichen Kandidaten, die nur in Zeile, Spalte oder Block vorkommen können.
*   **Fehlerüberprüfung:** (optional, als separater "Check" Button) Überprüft das gesamte Sudoku auf Fehler und markiert sie (ähnlich der Echtzeit-Überprüfung).
*   **Keine automatische Lösung:** Das Spiel sollte *keine* automatische Lösungsfunktion bieten, um den Spieler zum logischen Denken anzuregen.

**6. Spielzustand:**

*   **Timer:** (Optional) Ein Timer, der die Spielzeit misst.
*   **Speichern/Laden:**  (Optional) Möglichkeit, den Fortschritt zu speichern und später fortzusetzen.
*   **Neues Spiel:**  Button zum Starten eines neuen Spiels mit dem gleichen oder einem anderen Schwierigkeitsgrad.
*   **Gewinnbedingung:** Wenn alle Felder korrekt ausgefüllt sind und keine Konflikte bestehen, wird das Sudoku als gelöst gewertet und eine entsprechende Meldung angezeigt.
*   **Zurücksetzen:** Möglichkeit, das aktuelle Rätsel komplett zurückzusetzen.



## Annahmen

*   **Sudoku-Generierung:** Die Generierung eines Sudokus, das genau eine Lösung hat, ist ein komplexes Thema. Ein Ansatz ist das iterative Entfernen von Zahlen aus einem vollständig gelösten Sudoku, wobei sichergestellt wird, dass nach jeder Entfernung weiterhin eine eindeutige Lösung existiert.  Die Anzahl der zu entfernenden Zahlen bestimmt den Schwierigkeitsgrad.  Die Generierung ist ein separater Algorithmus und sollte nicht Teil der Kernlogik des Spielablaufs sein.
*   **Performance:** Die Echtzeit-Konflikterkennung sollte effizient implementiert werden und darf die Performance des Browsers nicht beeinträchtigen, insbesondere bei mobilen Geräten.
*   **Barrierefreiheit:** Das Spiel sollte auch für Menschen mit Behinderungen zugänglich sein, z.B. durch Tastaturnavigation und alternative visuelle Darstellungen.
*   **JavaScript Framework:** Es wird ein JavaScript-Framework (z.B. React, Vue.js) für die Entwicklung der Benutzeroberfläche verwendet.
*   **Browser-Kompatibilität:** Das Spiel sollte in modernen Browsern (Chrome, Firefox, Safari, Edge) gut funktionieren.

## Quellen

*   **Sudoku-Lösungsalgorithmen:** Keine gesicherte Quelle. Das Prinzip der Lösung basiert auf Backtracking und Constraint Propagation, Konzepte, die in der Informatik bekannt sind, aber da ich keine spezifischen Implementierungen hier verwende sondern den Fokus auf Szenarien einer Benutzeroberfläche lege, verwende ich keine spezifischen Quellen.
*   **Sudoku-Generierungsalgorithmen:** Keine gesicherte Quelle, ähnliche Begründung wie oben.
*   **Visuelle Gestaltung:** Allgemeine Prinzipien der Usability und der visuellen Hierarchie.
*   **02-pruefung.md Einwände:**

    *   **Fehler werden nicht immer korrekt hervorgehoben:** Das oben beschriebene Design mit Hervorhebung *aller* beteiligten Zellen soll dieses Problem beheben.
    *   **Notizenmodus umständlich:** Die vorgeschlagene Implementierung mit einem Toggle-Button und direktem Eingeben der Zahlen in den Notizmodus ist intuitiver.
    *   **Keine Hilfestellung für Notizen:** eine suggestion für eine Hilfestellung die automatischen Kandidaten für eine Zelle anzeigt ist eine gute Überlegung für spätere Versionen, aber nicht notwendig für den MVP.
    *   **Optik der Notizen zu subtil:** Die Darstellung der Notizen ist ein wichtiger Punkt. Die Größe und Farbe müssen sorgfältig gewählt werden, um sie gut erkennbar, aber nicht zu aufdringlich zu machen.
    *   **Fehlende Möglichkeit zum Zurücksetzen:**  Ein Zurücksetzen-Button wurde hinzugefügt.
    *    **Keine Möglichkeit, ein ungelöstes Rätsel zu verlassen:** Ein "Neues Spiel" – Button deckt den Bedarf ab.
