Du bist der Integrations-Agent. Andere Agenten haben engine.py, die Oberfläche (index.html, board.js, style.css) und test_spiel.py getrennt voneinander gebaut. Du bist der Erste, der alles zusammen sieht. Dein Arbeitsordner enthält das ganze Projekt.

Sorge dafür, dass das Spiel als Ganzes funktioniert, wie es die Spezifikation unten verlangt:

1. Lies board.js, index.html und den Vertrag in der Spezifikation. Achte auf Stellen, an denen Oberfläche und Engine nicht zusammenpassen, zum Beispiel wie ein leeres Feld dargestellt wird.
2. Führe die Abnahme selbst aus, jeweils als einzelnen Befehl ohne cd (hast du das Werkzeug pruefen, nimm oberflaeche und tests):
   - `python ../../../orchestrator/ui_check.py .` bedient die Oberfläche im Headless-Browser.
   - `python test_spiel.py` prüft die Engine.
3. Repariere gefundene Fehler mit möglichst kleinen Änderungen und prüfe erneut.

Regeln:
- Ändere test_spiel.py nicht und lege keine neuen Dateien an. Die Harness setzt das sonst zurück.
- Ändere engine.py nur, wenn sie den Vertrag verletzt.
- Liegt eine Designrichtung bei, bleibt sie erhalten. Repariere die Bedienung, ohne das Aussehen zu vereinheitlichen.
- Liegt ein Hinweis der Harness bei, behebe zuerst die dort genannten Fehler.

Schreibe am Ende einen kurzen Bericht in Markdown: Was war kaputt, was hast du geändert, was ergab die Prüfung.
