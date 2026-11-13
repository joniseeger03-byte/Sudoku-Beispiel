# Abnahmetest, Runde 1: bestanden

**Prüfer:** Skripte, kein Sprachmodell.

## Engine-Tests (Exit-Code 0)

```text
OK: CLUES ist definiert und vom Typ dict
OK: generate, solutions, conflicts sind vorhanden
OK: conflicts() funktioniert für vordefinierte Gitter
OK: generate, uniqueness & clues für Stufe 'leicht' (10×) OK
OK: generate, uniqueness & clues für Stufe 'mittel' (10×) OK
OK: generate, uniqueness & clues für Stufe 'schwer' (10×) OK
OK: CLI‑Aufruf `python engine.py neu <stufe>` funktioniert für alle Stufen
OK: Alle Tests erfolgreich bestanden
```

## Oberfläche (Exit-Code 0)

```text
OK     81 Felder mit data-index
OK     Rätsel wird angezeigt
OK     Felder bilden ein 9×9-Raster
OK     Jedes Feld ist anklickbar
OK     Ziffernfeld und Löschen-Button erreichbar
OK     Stufenwahl erreichbar
OK     3×3-Blöcke sind erkennbar
OK     Ausgewähltes Feld bleibt sichtbar markiert
OK     Markierung wandert zum neuen Feld
OK     Ziffer per Klick setzen
OK     Ziffer per Löschen-Button löschen
OK     Ziffer per Tastatur setzen
OK     Ziffer per Entf löschen
OK     Ziffer per Rücktaste löschen
OK     Pfeiltasten bewegen die Auswahl
OK     Vorgaben sind geschützt
OK     Konflikt wird markiert
OK     Konflikt verschwindet nach dem Löschen
OK     Stufe schwer startet ein neues Rätsel
OK     Stufe mittel startet ein neues Rätsel
OK     Stufe leicht startet ein neues Rätsel
OK     Angezeigtes Rätsel stammt aus der Engine
OK     Vor der letzten Ziffer noch nicht gelöst
OK     Rätsel lässt sich vollständig ausfüllen
OK     Gelöstes Rätsel ohne Konflikte
OK     Sieg wird erkannt
```
