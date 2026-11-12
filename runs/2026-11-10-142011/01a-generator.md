## Sudoku Generator für das Web

Dieses Dokument beschreibt die Forschungsphase für die Entwicklung eines Sudoku Generators, der Rätsel mit genau einer Lösung erzeugt, im Rahmen eines Webprojekts ohne Backend.

### Empfehlung

Die Erzeugung von Sudoku-Rätseln, die garantiert genau eine Lösung haben, ist ein komplexes Problem.  Der empfohlene Ansatz ist ein zweistufiger Prozess:

1. **Erzeugung eines vollständigen, korrekten Sudoku-Gitters:** Zuerst wird ein vollständig ausgefülltes, valides Sudoku-Gitter generiert.  Dies kann durch Backtracking-Algorithmen erfolgen.
2. **Entfernung von Zahlen zur Erzeugung des Rätsels:**  Anschließend werden systematisch Zahlen aus dem vollständigen Gitter entfernt, wobei nach jeder Entfernung geprüft wird, ob das resultierende Rätsel noch immer nur eine Lösung besitzt.  Hier kommt ein Backtracking-Löser zum Einsatz.  Die Anzahl der zu entfernenden Zahlen bestimmt die Schwierigkeit.

**Schwierigkeitsgrade:**

*   **Leicht:**  Ein großer Anteil an vorgegebenen Zahlen (z.B. 36-40).
*   **Mittel:**  Ein moderater Anteil an vorgegebenen Zahlen (z.B. 30-34).
*   **Schwer:**  Ein geringer Anteil an vorgegebenen Zahlen (z.B. 24-28). 

**Wichtige Algorithmen/Techniken:**

*   **Backtracking:** Sowohl für die Generierung des vollständigen Gitters als auch für die Überprüfung der Eindeutigkeit der Lösung.
*   **Pseudozufallszahlengenerator (PRNG):** Zur Abwechslung bei der Generierung des anfänglichen Gitters, um verschiedene Rätsel zu erzeugen.
*   **Eindeutigkeitsprüfung:** Der wichtigste Teil. Nach dem Entfernen einer Zahl muss überprüft werden, ob das resultierende Rätsel immer noch nur eine Lösung hat. Dies geschieht durch einen Backtracking-Löser, der stoppt, sobald er mehr als eine Lösung findet.

### Annahmen

*   **JavaScript als primäre Programmiersprache:** Da die Anwendung im Browser laufen soll, wird JavaScript die Hauptsprache sein.
*   **Kein Backend:** Die gesamte Logik, einschließlich der Rätselgenerierung, muss im Browser ablaufen.
*   **Vertretbare Performance:** Obwohl die Rätselgenerierung rechenintensiv sein kann, wird erwartet, dass sie innerhalb akzeptabler Zeit (z.B. weniger als einer Sekunde) ausgeführt werden kann.  Optimierungen des Backtracking-Algorithmus werden ggf. notwendig sein.
*   **Benutzerfreundliche Eingabe:** Die Eingabe per Tastatur und Touch sollte intuitiv und einfach sein.
*   **Konfliktmarkierung in Echtzeit:** Die Anwendung soll dem Benutzer sofort anzeigen, welche Felder einen Konflikt verursachen.
*   **Eindeutigkeit der Lösung:** Das wichtigste Kriterium ist, dass jedes generierte Rätsel genau eine Lösung hat. Die Prüfung hievon ist der zeitaufwändigste Teil und muss robust implementiert werden.

### Einbeziehung der Einwände aus 02-pruefung.md

Die Prüfung (02-pruefung.md) wies auf folgende Punkte hin, die in der Planung berücksichtigt werden müssen:

*   **Effizienz des Backtrackings:**  Backtracking kann sehr ineffizient sein, insbesondere bei schwierigen Rätseln.  
    *   **Antwort:** Optimierungen des Backtracking-Algorithmus sind notwendig. Dazu gehören z.B. die Auswahl des Feldes mit der geringsten Anzahl möglicher Werte als nächstes zu prüfendes Feld (Minimum Remaining Values – MRV).  Weiter optimieren kann man die Kandidatenlisten für jedes Feld.
*   **Sicherstellung der Eindeutigkeit:**  Die Prüfung der Eindeutigkeit ist rechenintensiv.
    *   **Antwort:** Die Überprüfung der Eindeutigkeit muss nach *jeder* Entfernung einer Zahl erfolgen. Dies ist zwar aufwendig, aber notwendig, um die geforderte Anforderung zu erfüllen.  Frühzeitiges Abbrechen des Backtrackings, sobald eine zweite Lösung gefunden wird, ist entscheidend, um Rechenzeit zu sparen.
*   **Schwierigkeitsgrade relativ zur Lösungstechnik:** Die Schwierigkeitsgrade sollten nicht nur auf der Anzahl der vorgegebenen Zahlen basieren, sondern auch auf den benötigten Lösungsstrategien.
    *   **Antwort:**  Die Anzahl der vorgegebenen Zahlen ist ein guter Startpunkt, aber zusätzliche Metriken sollten berücksichtigt werden, z. B. die Komplexität der Logik, die für die Lösung des Rätsels erforderlich ist (z. B. versteckte Paare, X-Wing).  Dies ist jedoch ein fortgeschritteneres Thema und kann für eine erste Implementierung vernachlässigt werden.  Der Fokus liegt zunächst auf der garantieren eindeutigen Lösung.

### Quellen

*   **Donald Knuth, "The Art of Computer Programming, Volume 4A: Combinatorial Algorithms":**  Eine umfassende Referenz für algorithmische Probleme, einschließlich Backtracking. (Bekannte Quelle)
*   **Wikipedia – Sudoku:** Hintergrundinformationen zum Sudoku und seinen Regeln. (Bekannte Quelle)

*keine gesicherte Quelle* für spezifische Implementierungen eines robusten und effizienten Sudoku-Generators in JavaScript. Die Implementierung wird auf den oben genannten Prinzipien basieren und durch Testen und Optimierung verfeinert werden.
