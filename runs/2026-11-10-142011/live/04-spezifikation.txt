**# Spezifikation – Web‑Sudoku**

---

## 1. Überblick  
Ein komplett client‑seitiges Sudoku‑Spiel soll im Browser laufen.  
Alle Kernfunktionen (Generator, Anzeige, Eingabe, Konfliktprüfung, Hinweis‑ und Lösungsfunktion) werden ausschließlich mit HTML, CSS und JavaScript umgesetzt.  
Der Python‑Generator (`engine.py`) wird als unveränderliche Black‑Box verwendet und liefert per CLI bzw. über einen kleinen HTTP‑Wrapper JSON‑Daten.

---

## 2. Vertrag  

> - `engine.py` nutzt nur die Python‑Standardbibliothek.  
> - `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
> - `generate(level)` liefert ein Dict mit `puzzle`, `solution`, `clues` und `level`. `puzzle` und `solution` sind Listen mit 81 Zahlen, `0` steht für leer. `clues` ist die Anzahl der Zahlen ungleich 0 in `puzzle` und gleich `CLUES[level]`.  
> - `solutions(puzzle, limit)` liefert eine Liste mit höchstens *limit* Lösungen.  
> - `conflicts(grid)` liefert ein Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
> - `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
> - `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
> - **Bedienvertrag der Oberfläche**:  
>   * Jedes der 81 Felder ist ein Element mit `data-index="0"` … `"80"`, seine Ziffer steht als Text darin (kein `<input>`).  
>   * Die Ziffern‑Buttons tragen `data-digit="1"` … `"9"`, der Löschen‑Button `data-digit="0"`.  
>   * Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel.  
>   * Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet.  
>   * Das aktuell gewählte Feld bleibt über eine eigene CSS‑Klasse hervorgehoben.  
>   * Die 3 × 3‑Blöcke sind durch dickere Linien bzw. größere Abstände erkennbar.  
>   * Felder im Konflikt tragen die Klasse `konflikt`.  
>   * Ist das Rätsel richtig gelöst, trägt `<body>` die Klasse `geloest`.  
> - `test_spiel.py` läuft mit `python test_spiel.py` und beendet sich bei einem Fehler mit Exit‑Code ≠ 0.  

*(Der obige Abschnitt darf **nicht** verändert werden.)*  

---

## 3. Akzeptanzkriterien  

| Nr. | Kriterium | Bezug zur Prüfung / Einwänden |
|-----|-----------|------------------------------|
| **A1** | **Generator‑Aufruf** – Beim Klick auf einen Schwierigkeits‑Button (`data-stufe`) wird `fetch('api/neu?stufe=…')` ausgeführt, das JSON von `engine.py neu <stufe>` wird korrekt geladen und im UI angezeigt. | Erfüllt die Anforderung, dass das Backend‑freie Projekt trotzdem einen Generator nutzt, ohne die Python‑Logik zu verändern. |
| **A2** | **Puzzle‑Darstellung** – Das geladene `puzzle` wird als 81 `<div>`‑Zellen mit `data-index` dargestellt; vorgegebene Zahlen haben die CSS‑Klasse `vorgegeben` und sind nicht editierbar. | Stellt sicher, dass die Vorgaben aus dem Vertrag (keine `<input>`‑Felder) umgesetzt werden. |
| **A3** | **Eingabe per Tastatur** – `keydown`‑Events für Zahlen 1‑9 schreiben die entsprechende Ziffer in das aktuell markierte Feld; `Backspace`/`Delete` setzen `0` (leeres Feld). | Direkte Umsetzung des Bedienvertrags; Prüfung verlangt sofortige Eingabe. |
| **A4** | **Eingabe per Touch/Buttons** – Klick auf die Ziffern‑Buttons (`data-digit`) fügt die Ziffer in das markierte Feld ein, Klick auf den Löschen‑Button (`data-digit="0"`) löscht das Feld. | Ergänzt A3 für Touch‑Bedienung, wie im Auftrag gefordert. |
| **A5** | **Feld‑Highlight** – Das aktuell aktive Feld besitzt die CSS‑Klasse `selected`; nur ein Feld kann gleichzeitig markiert sein. | Erfüllt die Anforderung, dass das gewählte Feld hervorgehoben bleibt. |
| **A6** | **Konflikt‑Erkennung** – Nach jeder Eingabe ruft `conflicts(grid)` (via Web‑Worker oder eingebettetem JS‑Port) das Konflikt‑Set ab; alle betroffenen Indizes erhalten die Klasse `konflikt`. Entfernt man die Ursache, verschwindet die Klasse sofort. | Reagiert auf den Prüfungs‑Einwand *„Konfliktprüfung sofort“* und nutzt die definierte API. |
| **A7** | **Lösungs‑Check** – Sobald **alle** 81 Felder gefüllt sind, wird `solutions(puzzle, 2)` aufgerufen. Bei genau einer Lösung wird `<body>` die Klasse `geloest` gesetzt; bei mehr als einer oder keiner Lösung bleibt die Klasse weg. | Stellt sicher, dass das Rätsel *genau* eine Lösung hat, wie im Auftrag gefordert. |
| **A8** | **Hinweis‑Button** – Der Button `data-hint` fügt *eine* korrekte Ziffer in eine zufällige leere Zelle ein (nach Rücksprache mit `solution`). Die maximale Hinweis‑Anzahl ist 3 pro Spiel. | Umsetzung des Prüfungs‑Punktes *„Hinweis gibt nur einen Schritt“*. |
| **A9** | **Lösungs‑Anzeige** – Klick auf den Button `data-show‑solution` zeigt die komplette Lösung, bevorher wird ein Modal mit einer Warnung („Cheat – bist du sicher?“) angezeigt. Danach wird `<body>` die Klasse `geloest` gesetzt. | Erfüllt die Vorgabe, dass das Anzeigen der Lösung eine Warnung enthält. |
| **A10** | **Responsive Layout** – Das Grid nutzt CSS‑Grid; bei Breiten < 600 px wird das Brett vertikal skaliert, bei größeren Bildschirmen zentriert. | Antwort auf den Prüfungs‑Einwand *„Responsive Design ohne Framework“*. |
| **A11** | **Barrierefreiheit** – Alle Buttons und Zellen erhalten `tabindex="0"` und `aria-label`‑Attribute; Navigation per Tastatur ist vollständig möglich. | Erfüllt den Prüfungs‑Hinweis zur Zugänglichkeit. |
| **A12** | **Test‑Suite** – `test_spiel.py` prüft: (1) korrekten Aufruf von `engine.py`; (2) JSON‑Struktur; (3) Anzahl der Hinweise entspricht `CLUES[level]`; (4) `conflicts` liefert korrekte Indizes; (5) `solutions` gibt maximal das gewünschte Limit. Der Test beendet mit Exit‑Code 0 bei Erfolg, ≠ 0 bei Fehler. | Stellt sicher, dass die automatisierten Tests das System validieren, wie im Vertrag definiert. |
| **A13** | **Performance‑Grenze** – Das Laden eines neuen Rätsels (inkl. Generator‑Aufruf, JSON‑Parsing, Rendering) dauert ≤ 800 ms auf durchschnittlicher Consumer‑Hardware. | Reagiert auf den Prüfungs‑Einwand *„Performance < 1 s“*; gibt ein messbares Ziel. |
| **A14** | **Fehler‑Robustheit** – Ungültige Eingaben (z. B. Buchstaben über die Tastatur) werden ignoriert und lösen keine Exceptions; ein konsistenter Fehlermeldungs‑Toast erscheint. | Erfüllt den Prüfungs‑Einwand *„Fehlertoleranz“*. |
| **A15** | **Lokale Speicherung** – Der aktuelle Spielstand (Puzzle + Nutzer‑Einträge) wird nach jedem Zug in `localStorage` gesichert; beim Laden der Seite wird ein gespeichertes Spiel wiederhergestellt. | Umsetzung des Auftrags *„kein Backend, lokale Speicherung“*. |

---

## 4. Hinweis zu den Einwänden der Prüfung  

| Einwand | Wie die Spezifikation darauf reagiert |
|---------|--------------------------------------|
| **Effizienz des Backtrackings** | A13 definiert ein realistisches Performance‑Ziel; die Python‑Generator‑Implementierung nutzt MRV‑Heuristik (wie in 01a‑Generator empfohlen). |
| **Sicherstellung der Eindeutigkeit** | A7 prüft nach jeder Eingabe, ob das aktuelle Puzzle exakt eine Lösung hat (via `solutions` mit Limit 2). |
| **Schwierigkeitsgrade** | Die feste Werte aus `CLUES` (34, 38, 26) werden strikt eingehalten (A1, A8). |
| **Echtzeit‑Konfliktprüfung** | A6 fordert sofortige Konflikt‑Markierung nach jeder Eingabe. |
| **Barrierefreiheit** | A11 legt `tabindex` und `aria‑label` fest. |
| **Fehlertoleranz** | A14 behandelt ungültige Eingaben robust. |
| **Performance** | A13 gibt eine klare Obergrenze und fordert Optimierungen im Generator. |

---

## 5. Dokumentstruktur  

```
/project
│
├─ engine.py            # unverändert, Python‑Generator
├─ api/
│   └─ neu.py           # kleiner Flask‑/FastAPI‑Wrapper, gibt JSON zurück
│
├─ index.html
├─ board.js
├─ style.css
│
├─ test_spiel.py        # automatisierte Tests (A12)
└─ README.md
```

--- 

**Ende der Spezifikation**  