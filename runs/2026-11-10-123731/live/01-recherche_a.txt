## Sudoku-Rätsel-Generierung mit garantierter Eindeutigkeit

Dieser Bericht fasst die Recherchen zusammen, die für die Erstellung eines Sudoku-Generierungsalgorithmus mit der Anforderung einer eindeutigen Lösung durchgeführt wurden. Es werden verschiedene Ansätze betrachtet, sowie Annahmen und Quellen. Außerdem wird auf Einwände aus der Prüfungsdokumentation (02-pruefung.md) eingegangen.

### Empfehlung

Der empfohlene Ansatz zur Generierung von Sudoku-Rätseln mit garantierter Eindeutigkeit ist eine Kombination aus zwei Phasen:

1. **Vollständige Sudoku-Lösung generieren:** Zuerst wird ein vollständig ausgefülltes, korrektes Sudoku erstellt.  Hierfür eignen sich Algorithmen wie Backtracking, die selbst generieren oder von vorgefertigten Basis-Sudokus ausgehen und diese permutieren (z.B. Zeilentausch, Spaltentausch, Blocktausch).  Das Ziel ist ein valides, gelöstes Sudoku.
2. **Zahlen entfernen und Eindeutigkeit prüfen:**  Anschließend werden systematisch Zahlen aus dem gelösten Sudoku entfernt.  Nach jeder Entfernung wird geprüft, ob das resultierende Rätsel noch immer eine eindeutige Lösung besitzt.  Dies ist der kritische Schritt.  Die Prüfung der Eindeutigkeit erfolgt durch einen Lösungsalgorithmus (Backtracking), der nach allen möglichen Lösungen sucht. Findet dieser Algorithmus mehr als eine Lösung, wird die letzte Entfernung rückgängig gemacht und eine andere Zelle ausgewählt.  Die Schwierigkeit wird über die Anzahl der entfernten Zahlen gesteuert.

Dieser Ansatz gewährleistet die Eindeutigkeit, da jedes Rätsel von einem gelösten Zustand abgeleitet wird und die Eindeutigkeit nach jeder Entfernung überprüft wird.  Das Verwenden von Backtracking sowohl für die Lösung als auch für die Eindeutigkeitsprüfung macht den Algorithmus zwar langsam, jedoch äußerst zuverlässig.  Optimierungen können durch intelligente Zellauswahl (z.B. zufällige Auswahl, aber Priorisierung von Zellen, die am komplexesten sind) und durch die Verwendung heuristischer Algorithmen zur Lösung des Sudokus erreicht werden.

**Berücksichtigung der Prüfung (02-pruefung.md):**

Die Prüfung wies auf das Problem hin, dass das bloße Entfernen von Zahlen *nicht* garantiert, dass ein Rätsel tatsächlich eine eindeutige Lösung hat. Es wurde auch vorgeschlagen, dass das Generieren von Rätseln, die "leicht", "mittel" oder "schwer" sind, subjektiv sein kann. 

* **Eindeutigkeit:** Der hier empfohlene Ansatz adressiert dieses Problem direkt durch explizite Prüfung der Eindeutigkeit *nach jeder* Entfernung.  Nur wenn das Rätsel eindeutig lösbar bleibt, wird die Entfernung beibehalten.
* **Schwierigkeitsgrade:**  Die Schwierigkeit kann durch eine Kombination aus zwei Kriterien gesteuert werden:
    * **Anzahl der gegebenen Zellen:**  Weniger gegebene Zellen = schwieriger.
    * **Verwendete Lösungstechniken:**  Die Komplexität der erforderlichen Lösungstechniken (z.B. Hidden Singles, Naked Pairs, X-Wing) kann analysiert werden.  Rätsel, die fortgeschrittenere Techniken erfordern, sind schwieriger.  Die Analyse der benötigten Techniken ist allerdings komplexer umzusetzen.

### Annahmen

* **Rechenleistung:** Die Prüfung der Eindeutigkeit ist rechenintensiv. Es wird angenommen, dass die Rechenleistung ausreichend ist, um diese Prüfung in akzeptabler Zeit durchzuführen.
* **Backtracking-Effizienz:** Die Effizienz des Backtracking-Algorithmus ist entscheidend für die Gesamtleistung. Eine gute Implementierung und Heuristiken sind wichtig.
* **Zufallszahlengenerator (RNG):** Ein guter RNG ist notwendig, um zufällige, aber gut verteilte Rätsel zu generieren.  Die Qualität des RNG beeinflusst die Diversität der erstellten Rätsel.
* **Definition von Schwierigkeitsgraden:** Die Definition, was ein "leichtes", "mittleres" oder "schweres" Sudoku ausmacht, ist subjektiv. Die hier empfohlene Kombination aus Anzahl der gegebenen Zellen und Komplexität der Lösungstechniken bietet eine praktikable Annäherung.

### Quellen

* **Donald Knuth: *The Art of Computer Programming, Volume 4, Fascicle 3: Combinatorial Algorithms*:** Eine grundlegende Ressource zum Thema Backtracking und kombinatorische Algorithmen.
* **("Sudoku"). Wikipedia, The Free Encyclopedia.** [https://en.wikipedia.org/wiki/Sudoku](https://en.wikipedia.org/wiki/Sudoku) - Bietet einen guten Überblick über Sudoku und seine Geschichte.
* Keine gesicherte Quelle. (Die meiste Information stammt aus allgemeiner Programmierkenntnis und Experimenten mit Backtracking-Algorithmen.)
