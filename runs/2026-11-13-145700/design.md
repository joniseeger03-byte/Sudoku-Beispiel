# Bleiglasfenster bei Tageslicht

## Entscheidung
Die Bleiglas-Richtung hat gewonnen. Sie liefert die klarste Blockgliederung: Jeder 3×3-Block ist ein eigenes Farbfeld, getrennt durch dicke dunkle Bleilinien. Die Felder bleiben dabei hell und die Ziffern dunkel, sodass die Lesbarkeit auf dem Smartphone nicht leidet. Sie ist rein mit CSS umsetzbar und unterscheidet sich deutlich von allen bisherigen Designs, die alle mit Papier, Karton, Stein oder Fliesen arbeiten. Dieses Design nutzt dagegen Licht und Farbglas.

## Vorgaben für die Oberfläche

**Farben**
- Seitenhintergrund (Mauerwerk, dunkel): `#2B2A33`
- Bleilinien, Brettrahmen, Blockgrenzen: `#14131A`
- Feldflächen, vier Glastöne im Schachbrett, ein Ton pro 3×3-Block, alle hell:
  - `#F3E3B8` (Honiggelb)
  - `#CFE6E4` (Seeglas)
  - `#F2CFC4` (Rosenglas)
  - `#D9D2EE` (Violettglas)
  - Die Blöcke wechseln so, dass sich Nachbarblöcke immer unterscheiden.
- Ziffern, vorgegeben: `#14131A`
- Ziffern, eigene Eingabe: `#1F4FA8` (Kobaltblau)
- Auswahl: Füllung `#FFFFFF`, Rand 3 px `#E07A00` (Bernstein)
- Mitbetonte Zeile, Spalte und Block der Auswahl: weißer Schleier, etwa `rgba(255,255,255,0.45)` über dem Glaston
- Konflikt: Füllung `#B3261E`, Ziffer `#FFFFFF`, fett
- Tasten: Fläche `#F3E3B8`, Text `#14131A`, Rand `#14131A`
- Gelöst: Hintergrund hellt auf zu `#3A3850`, Brettfelder bekommen einen leichten goldenen Schimmer `#FFE08A`.

**Schrift**
- Nur Systemschriften.
- Ziffern: `Georgia, "Times New Roman", serif`, fett, damit sie wie Glasmalerei-Antiqua wirken. Größe etwa 6–7 vmin, mindestens 22 px.
- Beschriftung und Tasten: `system-ui, -apple-system, "Segoe UI", sans-serif`.

**Anordnung**
- Das Brett ist ein quadratisches Fenster, so breit wie der Bildschirm abzüglich 12 px Rand, höchstens 520 px.
- Der Rahmen ist 6 px `#14131A` stark, die Blockgrenzen 4 px, die Feldgrenzen 1 px in einem dunklen Grau-Blau (`#4A4860`). Die Blöcke sind also erkennbar durch Farbe und dicke Linie.
- Die Stufenwahl steht als Reihe mit drei gleich breiten Buttons über dem Brett. Die aktive Stufe ist mit Bernsteinrand und weißer Füllung markiert.
- Das Ziffernfeld steht unter dem Brett: ein Raster mit 5 Spalten × 2 Zeilen (1–5, 6–9 und Löschen). Jede Taste ist mindestens 48 px hoch und hat 3 px Bleirand.
- Auf breiten Bildschirmen steht das Ziffernfeld rechts neben dem Brett.

**Stimmung**
Ruhig und feierlich, aber hell und klar. Warm wie Kirchenlicht und ohne Schnörkel: keine Muster in den Feldern, nur Flächen und Linien. Eine Animation ist nicht nötig, höchstens ein kurzes Aufleuchten (0,2 s) beim Wählen.

**Zustände**
- **Vorgegeben:** Glaston des Blocks, Ziffer in Schwarzblau, fett, nicht anklickbar zum Ändern.
- **Eigene Eingabe:** gleicher Glaston, Ziffer in Kobaltblau und normaler Stärke. Der Farbunterschied wird durch die Strichstärke gestützt, damit er auch bei Farbschwäche trägt.
- **Ausgewählt (Klasse `ausgewaehlt`):** weiße Füllung und Bernsteinrand, innen liegend, damit er die Bleilinien nicht verschiebt. Zeile, Spalte und Block sind leicht aufgehellt.
- **Konflikt (Klasse `konflikt`):** kräftiges Rot mit weißer Ziffer. Das ist ein Wechsel von hell zu dunkel und daher auch ohne Farbwahrnehmung sichtbar. Ist ein Konfliktfeld zugleich ausgewählt, behält es das Rot und bekommt zusätzlich den Bernsteinrand.
- **Gelöst (`body.geloest`):** das ganze Fenster leuchtet golden, die Konfliktfarbe entfällt.

## Geprüfte Optionen
- **Bleiglasfenster bei Tageslicht:** farbige Blockflächen mit dunklen Bleilinien. Gewählt wegen starker Blockgliederung, gutem Kontrast und rein CSS-tauglicher Umsetzung, und weil es sich von allen Vorgängern abhebt.
- **Glasmorphismus / Liquid Glass (Trend 2026):** durchscheinende, unscharfe Flächen. Verworfen, weil Unschärfe und Transparenz den Kontrast der Ziffern auf kleinen Bildschirmen schwächen und die Wirkung stark vom Hintergrund abhängt.
- **Konstruktivistisches Fahrkarten-/Eintrittskartendesign:** harte Typografie, Geometrie, Stempel. Verworfen, weil es dem Kartonbrett-Brutalismus und dem Risodruck zu nah käme und Ziffern auf Karten zu eng gesetzt wirken.
- **Dunkler Modus mit Bento-Kacheln:** modulare Kacheln auf dunklem Grund. Verworfen, weil es ein verbreiteter Standard ist und den 3×3-Blöcken keine eigene Identität gibt.

## Quellen
- https://webflow.com/blog/web-design-trends-2026
- https://www.kimp.io/web-design-trends-2026/
- https://studiomeyer.io/en/blog/webdesign-trends-2026.md
- https://www.cooperhewitt.org/2014/08/22/tickets/
- https://fontsinuse.com/uses/55722/metra-tickets-1990-1991
- https://www.derix.com/us/leaded-stained-glass
- https://www.derix.com/us/portfolio-items/kath-kirche-st-andreas-en
- https://www.planet-wissen.de/kultur/kunst/gerhard_richter/gerhard-richter-fenster-koelner-dom-100.html
- https://www.friedrich-verlag.de/friedrich-plus/sekundarstufe/kunst/historische-kunst/in-der-kirche-mit-mondrian-10727