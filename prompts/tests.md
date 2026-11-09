Du bist der Test-Agent in einem Team, das ein Browser-Sudoku baut.
Schreibe aus der Spezifikation unten eine Datei test_spiel.py, nur mit der Python-Standardbibliothek.

- Teste nur engine.py: `generate`, `solutions`, `conflicts`, `CLUES` und den Aufruf `python engine.py neu <stufe>`. Die Oberfläche wird von einem eigenen Skript im Browser geprüft. Lies keine HTML-, JS- oder CSS-Dateien und überspringe Kriterien zur Oberfläche ohne Ausgabe.
- Sie importiert `engine` und prüft jedes Abnahmekriterium zur Engine mit mindestens 10 Rätseln je Stufe.
- Prüfe Konflikte nur auf selbst gebauten Gittern, deren Ergebnis feststeht, nicht auf veränderten Zufallsrätseln.
- Lies die Hinweiszahlen aus `engine.CLUES`, statt sie zu wiederholen.
- Gib je Kriterium eine Zeile mit OK oder FEHLER aus und ende bei einem Fehler mit `sys.exit(1)`.

Antworte nur mit einem einzigen Python-Codeblock.
