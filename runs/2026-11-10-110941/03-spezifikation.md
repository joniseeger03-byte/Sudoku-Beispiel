## 1. Kurzfassung (Specification)

| Ziel | Ein Sudoku‑Spiel für den Browser ohne Backend, das die drei Schwierigkeitsgrade **leicht**, **mittel** und **schwer** bereitstellt. |
|------|-------------------------------------------------------------------------------------------------------------------------------------|
| Kern‑Funktionen | • Generierung eindeutiger Rätsel (einzige Lösung)  <br>• Eingabe per Tastatur + Touch  <br>• Echtzeit‑Konflikt‑Markierung  <br>• Hinweis‑Funktion (max. 3)  <br>• Notizen‑Modus  <br>• Visuelle 3×3‑Blöcke  <br>• Erfolgs‑Anzeige (`body.geloest`) |
| Nicht‑Funktionales | • Nur Python‑Standardbibliothek in `engine.py`  <br>• Keine externen Services (alle Daten lokal)  <br>• Tests über `test_spiel.py` mit Exit‑Code ≠ 0 bei Fehlern |
| Einschränkungen (aus Prüfung) | • Schwierigkeitsgrad wird **nur** über die vorgegebene Hinweis‑Zahl (`CLUES`) gesteuert – das reicht für das Projekt, aber ist ein grober Indikator.  <br>• Konflikt‑Markierung wird **nach Eingabe** durchgeführt (nicht beim Löschen von Vorgaben).  <br>• Gewinn‑Animation ist optional – ein einfacher Stilwechsel (`body.geloest`) genügt, um das Kriterium zu erfüllen. |

---

## 2. Vertrag (unverändert)

> - `engine.py` nutzt nur die Python‑Standardbibliothek.  
> - `CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}` gibt die Hinweiszahl je Stufe an.  
> - `generate(level)` liefert ein `Dict` mit `puzzle`, `solution`, `clues` und `level`. `puzzle` und `solution` sind Listen mit 81 Zahlen, `0` steht für leer. `clues` ist die Anzahl der Zahlen ungleich `0` in `puzzle` und gleich `CLUES[level]`.  
> - `solutions(puzzle, limit)` liefert eine Liste mit höchstens `limit` Lösungen.  
> - `conflicts(grid)` liefert ein `Set` der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren.  
> - `python engine.py neu <stufe>` gibt das Ergebnis von `generate` als JSON aus.  
> - `index.html`, `board.js` und `style.css` bilden die Oberfläche im Browser. `board.js` holt ein Rätsel mit `fetch('api/neu?stufe=mittel')`, relativ zur Seite, und bekommt dasselbe JSON zurück.  
> - **Bedienvertrag der Oberfläche:**  
>   • Jedes der 81 Felder ist ein Element mit `data-index="0"` bis `"80"`, seine Ziffer steht als Text darin (kein `<input>`).  
>   • Die Buttons des Ziffernfelds tragen `data-digit="1"` bis `"9"`, der Löschen‑Button trägt `data-digit="0"`.  
>   • Drei Buttons mit `data-stufe="leicht"`, `"mittel"` und `"schwer"` starten sofort ein neues Rätsel.  
>   • Tastatureingaben (1–9, Pfeiltasten, Entf, Rücktaste) werden über `keydown` auf `document` verarbeitet.  
>   • Das gewählte Feld bleibt über eine eigene Klasse sichtbar hervorgehoben.  
>   • Die 3×3‑Blöcke sind durch dickere Linien oder größere Abstände erkennbar.  
>   • Felder im Konflikt tragen die Klasse `konflikt`.  
>   • Ist das Rätsel richtig gelöst, trägt `body` die Klasse `geloest`.  
> - `test_spiel.py` läuft mit `python test_spiel.py` und endet bei einem Fehler mit Exit‑Code ungleich 0.

---

## 3. Abnahmekriterien  

| ID | Kriterium | Messgröße / Test | Hinweis aus Prüfung |
|----|-----------|------------------|---------------------|
| **A1** | **Generator liefert gültiges, eindeutiges Rätsel** | `engine.py neu <stufe>` gibt JSON mit `puzzle` und `solution` zurück. `solutions(puzzle, 2)` liefert **genau eine** Lösung und `len([x for x in puzzle if x!=0]) == CLUES[stufe]`. | Backtracking‑Generator + eindeutige‑Lösungs‑Prüfung (✅) |
| **A2** | **Hinweis‑Zahl stimmt mit Vertrag überein** | `puzzle`‑Anzahl ≠ 0 = `CLUES[stufe]`. | Direkt aus Vertrag |
| **A3** | **Frontend‑Board erzeugt 81 Zellen mit korrektem `data-index`** | DOM‑Abfrage `document.querySelectorAll('[data-index]').length === 81`. | UI‑Spec |
| **A4** | **Schwierigkeits‑Buttons starten neue Rätsel** | Klick auf Button `data-stufe="leicht"` → `fetch('api/neu?stufe=leicht')` wird ausgeführt, neues Puzzle angezeigt. | UI‑Spec |
| **A5** | **Tastatureingabe füllt ausgewähltes Feld** | Nach Auswahl eines Feldes und Drücken von `5` erscheint Text “5” im betreffenden Element. | UI‑Spec |
| **A6** | **Pfeiltasten navigieren zwischen Feldern** | `ArrowRight` bewegt Fokus von Index 0 zu 1, usw. | UI‑Spec |
| **A7** | **Entf/Backspace löscht Inhalt** | Drücken von `Backspace` entfernt den Text im aktuell ausgewählten Feld. | UI‑Spec |
| **A8** | **Konflikt‑Markierung** | Nach Eingabe einer falschen Ziffer (z. B. `5` in einer Zeile, wo bereits `5` steht) erhalten **alle** betroffenen Zellen die Klasse `konflikt`. | Prüfung ✅ |
| **A9** | **Keine Konflikt‑Markierung bei Vorgabefeldern** | Vorgabefelder (die aus `puzzle` stammen) erhalten **nicht** die Klasse `konflikt`, selbst wenn sie Teil eines Konflikts werden (sie dürfen nicht bearbeitet werden). | Prüfung ✅ |
| **A10** | **Hinweis‑Funktion (max. 3 pro Spiel)** | Klick auf “Hinweis” liefert eine korrekte Ziffer für ein leeres Feld; nach drei Klicks ist die Schaltfläche deaktiviert. | UI‑Spec |
| **A11** | **Notizen‑Modus** | Aktivieren → Eingabe einer Ziffer fügt sie als kleine, halbtransparente Zahl im Feld ein; `Backspace` entfernt die letzte Notiz. | UI‑Spec |
| **A12** | **Erfolgs‑Anzeige** | Beim Ausfüllen aller Felder ohne Konflikte wird `body` mit Klasse `geloest` versehen. | UI‑Spec |
| **A13** | **Test‑Suite besteht** | `python test_spiel.py` beendet mit Exit‑Code 0. | Vertrag |
| **A14** | **Performance‑Grenze** | Generierung eines Rätsels (mittlerer Schwierigkeitsgrad) dauert ≤ 2 Sekunden im Browser (gemessen mit `performance.now()`). | Hinweis aus Prüfung (⚠️ Schwierigkeitsgrad‑Steuerung) |
| **A15** | **Gewinn‑Animation (optional)** | Beim Erreichen von `body.geloest` ändert sich mindestens ein Stil (z. B. Hintergrundfarbe oder kurze Animation). | Hinweis aus Prüfung (⚠️ Gewinn‑Animation) |

Erfüllte Kriterien **A1–A13** sind zwingend; **A14** und **A15** gelten als Qualitäts‑Kriterien, deren Fehlen das Projekt jedoch nicht blockiert. 

--- 

*Ende der Spezifikation.*