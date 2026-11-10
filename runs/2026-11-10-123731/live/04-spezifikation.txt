## Spezifikation – Sudoku‑Web‑App  

### 1. Ziel  
Eine vollständig spielbare Sudoku‑Applikation im Browser ohne Backend.  
* Drei Schwierigkeitsgrade (leicht, mittel, schwer) mit fest vorgegebenen Hinweiszahlen.  
* Eingabe per Tastatur und Touch, sofortige Fehlermarkierung, eindeutige Lösung pro Rätsel.  

---

### 2. Vertrag  

> **engine.py nutzt nur die Python‑Standardbibliothek.**  
> **`CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}`** gibt die Hinweiszahl je Stufe an.  
> **`generate(level)`** liefert ein `dict` mit den Schlüsseln `puzzle`, `solution`, `clues` und `level`.  
> * `puzzle` & `solution` sind Listen mit 81 Zahlen (0 = leer).  
> * `clues` ist die Anzahl der Nicht‑Null‑Zellen in `puzzle` und muss **gleich** `CLUES[level]` sein.  
> **`solutions(puzzle, limit)`** liefert eine Liste von maximal `limit` Lösungen.  
> **`conflicts(grid)`** liefert ein `set` von Indizes (0‑80), die in Zeile, Spalte oder Block kollidieren.  
> **`python engine.py neu <stufe>`** gibt das Ergebnis von `generate` als JSON aus.  
> **Frontend‑Dateien** `index.html`, `board.js` und `style.css` bilden die Oberfläche.  
> * `board.js` ruft per `fetch('api/neu?stufe=mittel')` das JSON‑Rätsel relativ zur Seite ab.  
> * **UI‑Vertrag:**  
>   * Jedes der 81 Felder hat das Attribut `data-index="0"` … `"80"` und zeigt seine Ziffer als Text (kein `<input>`).  
>   * Ziffern‑Buttons besitzen `data-digit="1"` … `"9"`, der Löschen‑Button `data-digit="0"`.  
>   * Drei Schwierigkeits‑Buttons besitzen `data-stufe="leicht"`, `data-stufe="mittel"` und `data-stufe="schwer"` und starten sofort ein neues Rätsel.  
>   * Tastatureingaben (1‑9, Pfeiltasten, Entf, Rücktaste) werden über ein `keydown`‑Listener auf `document` verarbeitet.  
>   * Das aktuell ausgewählte Feld erhält eine extra Klasse zur Hervorhebung.  
>   * 3×3‑Blöcke sind durch dickere Linien bzw. größere Abstände erkennbar.  
>   * Felder im Konflikt erhalten die Klasse `konflikt`.  
>   * Ist das Rätsel korrekt gelöst, trägt das `<body>` die Klasse `geloest`.  
> **Tests:** `test_spiel.py` wird mit `python test_spiel.py` ausgeführt und beendet bei einem Fehler mit einem Exit‑Code ≠ 0.  

---

### 3. Abnahmekriterien  

| Kriterium | Beschreibung | Prüfung |
|-----------|--------------|--------|
| **A1** | **Generator** liefert für jede Stufe (`leicht`, `mittel`, `schwer`) ein Rätsel, dessen `clues`‑Wert exakt dem in `CLUES` definierten Wert entspricht. | `python engine.py neu leicht` → JSON‑Objekt → `clues == 38` (analog für die anderen Stufen). |
| **A2** | Das generierte Rätsel hat **genau eine** Lösung. | `solutions(puzzle, 2)` liefert exakt **eine** Lösung; `len(result) == 1`. |
| **A3** | `conflicts(grid)` gibt **alle** kollidierenden Indizes zurück und **nur** diese. | Für ein beliebiges, manuell manipuliertes Grid prüfen, dass jede falsche Zeile/Spalte/Block‑Duplikation im Rückgabeset enthalten ist und kein korrektes Feld. |
| **A4** | UI zeigt ein 9×9‑Gitter, 81 Felder mit `data-index`‑Attribut und die aktuelle Ziffer als Text. | Visuelle Inspektion + DOM‑Abfrage (`document.querySelectorAll('[data-index]')`). |
| **A5** | Auswahl eines Feldes fügt die Klasse `selected` (oder analog) hinzu und entfernt sie von allen anderen Feldern. | Klick/Touch → prüfen, dass genau ein Element die Klasse besitzt. |
| **A6** | Tastatureingaben 1‑9 schreiben die Ziffer in das aktuell selektierte Feld, 0/Entf/Backspace leert das Feld. Ungültige Tasten werden ignoriert. | Simulierter `keydown`‑Event → Prüfung des `textContent` des Feldes. |
| **A7** | Zahlen‑Buttons (`data-digit`) und Löschen‑Button (`data-digit="0"`) wirken identisch wie Tastatureingaben auf das selektierte Feld. | Klick auf Button → Feldwert prüfen. |
| **A8** | Schwierigkeits‑Buttons (`data-stufe`) starten sofort ein neues Rätsel mit den korrekten Hinweiszahlen. | Klick → `fetch`‑Aufruf → JSON‑Antwort → `clues`‑Wert prüfen. |
| **A9** | Nach jeder Eingabe werden **alle** Konflikte im betroffenen Feld, seiner Zeile, Spalte und Block markiert (`class="konflikt"`). | Eingabe einer falschen Ziffer → prüfen, dass die betroffenen Indizes die Klasse besitzen und keine anderen. |
| **A10** | Sobald das Gitter komplett und konfliktfrei ist, wird `body` mit der Klasse `geloest` versehen. | Vollständige, korrekte Lösung eingeben → `document.body.classList.contains('geloest')` muss `true` sein. |
| **A11** | `test_spiel.py` läuft ohne Fehlermeldungen (Exit‑Code 0). | `python test_spiel.py` → Rückgabecode 0. |
| **A12** | Performance‑Kriterium: Das Laden eines neuen Rätsels (Fetch + Render) dauert ≤ 500 ms auf einem durchschnittlichen Desktop‑Browser. | Messung mit Browser‑Dev‑Tools (Network → Timing). |
| **A13** | **Responsives Design:** Das Gitter ist auf mobilen Geräten (≤ 480 px Breite) vollständig nutzbar (Touch‑Buttons sichtbar, Felder gut anklickbar). | Manueller Test auf Smartphone bzw. Emulator. |
| **A14** | **Barrierefreiheit (optional, aber positiv bewertet):** Jedes Feld hat ein `aria-label` mit Position und aktuellem Wert. | DOM‑Inspection (`getAttribute('aria-label')`). |

Erfüllung **aller** Kriterien A1‑A14 gilt die Spezifikation als abgenommen.  

---  

*Hinweis:* Die genannten Akzeptanzkriterien berücksichtigen die in **02‑pruefung.md** aufgeführten Einwände (Eingabemaskierung, sofortige Fehlermarkierung, Performance).