▶ Read: board.js

▶ PowerShell: python ../../../../orchestrator/ui_check.py .

Das Setzen von Ziffern schlägt fehl. board.js prüft `grid[sel] === undefined`, die Engine liefert für leere Felder aber `0`.

▶ Edit: board.js

▶ PowerShell: python ../../../../orchestrator/ui_check.py .

▶ PowerShell: python test_spiel.py

# Integrationsbericht

**Kaputt:** Oberfläche und Engine waren sich uneinig, wie ein leeres Feld aussieht. Die Oberfläche erwartete `undefined`, laut Vertrag ist es `0`. Dadurch ließ sich keine Ziffer setzen.

**Geändert:** `board.js`, Funktion `put`: Sie prüft jetzt, ob das Feld eine Vorgabe ist.

**Prüfung:** Oberflächen-Test und Engine-Tests bestehen.
