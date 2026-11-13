# Seekarte: Lotung und Magenta

## Entscheidung
Die Seekarte hat gewonnen, weil ihre Farblogik das Sudoku-Problem direkt löst. Tiefes Wasser ist weiß, Flachwasser ist blau getönt, und genau so lassen sich die 3×3-Blöcke im Schachbrettmuster auf dem Smartphone klar trennen. Magenta ist in der Seekarte die Warnfarbe für Navigationsrelevantes. Das passt für Auswahl und Konflikt, und es unterscheidet sich deutlich von allen bisherigen Papier-, Stein-, Glas- und Bauhaus-Looks. Alles ist mit HTML und CSS machbar: Flächenfarben, Linien und Systemschriften reichen.

## Vorgaben für die Oberfläche
**Farben**
- Seitenhintergrund ("Land"): `#E9DFC8`
- Brett-Blöcke Typ A ("tiefes Wasser"): `#FBFCF8`
- Brett-Blöcke Typ B ("Flachwasser"), im Schachbrett, also Blöcke 2, 4, 6 und 8: `#CFE3EA`
- Tusche für Ziffern und Linien: `#14263A`
- Magenta (Auswahl, Konflikt): `#C2185B`
- Magenta-Fläche für die Auswahl: `#F6C9DE`
- Dünne Feldlinien: `#8FA9B8`
- Dicke Blocklinien und Rahmen: `#14263A`
- Eigene Eingabe: `#1F5E9C`
- Konflikt-Fläche: `#F2A3C3`

**Schrift (nur Systemschriften)**
- Ziffern und Bedienelemente: `"Helvetica Neue", Arial, system-ui, sans-serif`
- Vorgegebene Ziffern: aufrecht und fett (weight 700), in Tusche.
- Eigene Ziffern: kursiv (weight 500), in Blau. Das ist wie bei Lotungszahlen auf der Karte, wo Gemessenes aufrecht und Eigenes kursiv steht.
- Notizen: kursiv, kleine Schrift, `#4A6A80`, im 3×3-Raster innerhalb des Felds.
- Beschriftungen wie "Stufe" und "Notizen": Großbuchstaben, 0.12em Sperrung, 12–13 px.

**Anordnung**
- Das Brett steht oben und füllt die Breite (max. 480 px). Es hat einen doppelten Kartenrahmen: außen 3 px Tusche, innen 1 px Abstand, dann 1 px Tusche. Zusätzlich sitzt außen eine Gradskala aus feinen Strichen (CSS-`repeating-linear-gradient`) als Randdekor.
- Zwischen den Blöcken liegen 2–3 px dicke Tuschelinien. Die Felder haben 1 px Linien in `#8FA9B8`. Zusammen mit dem Blau-Weiß-Schachbrett ist die Blockstruktur doppelt abgesichert.
- Die Stufenwahl steht über dem Brett als Dreiergruppe aus gleich breiten Buttons ("Leicht", "Mittel", "Schwer"). Sie sehen aus wie Kartenlegenden mit eckigem 2-px-Rahmen. Die aktive Stufe ist in Tusche gefüllt mit heller Schrift.
- Das Ziffernfeld steht unter dem Brett als 5+5-Raster aus 1–9 und dem Löschen-Button "✕" (`data-digit="0"`). Jeder Button ist mindestens 48×48 px groß, mit hellem Grund `#FBFCF8` und 2-px-Tuscherahmen.
- Der Notizen-Schalter und die Hilfen ("Fehler zeigen", "Mögliche Werte") bilden eine Zeile zwischen Brett und Ziffernfeld. Aktiver Notizenmodus: Magenta-Rahmen und ein "N"-Zeichen als Kompassmarke.

**Stimmung**
Ruhig, präzise und nüchtern-navigatorisch, wie eine Karte, auf der man Kurs setzt. Es gibt keine Schatten und keine Verläufe außer der Randskala. Die Wirkung kommt aus Linie, Fläche und Farbtrennung.

**Zustände**
- **Vorgegeben:** Tusche `#14263A`, aufrecht und fett, Feldfarbe bleibt die des Blocks. Es ist nicht anklickbar zum Ändern, aber auswählbar.
- **Eigene Eingabe:** Blau `#1F5E9C`, kursiv.
- **Ausgewählt:** Feldfläche `#F6C9DE` mit 3-px-Magenta-Rahmen innen (`outline`/`box-shadow inset`). Zeile, Spalte und Block des Felds bekommen einen leichten Magenta-Schleier (`rgba(194,24,91,.08)`). Gleiche Ziffern wie im gewählten Feld bekommen einen unterstrichenen Magenta-Strich.
- **Konflikt** (Klasse `konflikt`): Fläche `#F2A3C3`, Ziffer in Magenta `#C2185B`, fett, mit einem diagonal gestreiften Hintergrund (`repeating-linear-gradient`, 45°). So ist der Konflikt nicht nur an der Farbe erkennbar. Er hat Kontrast von mindestens 4.5:1 und bleibt auch für Rot-Grün-Schwäche sichtbar.
- **Gelöst** (Klasse `geloest` auf body): Der Brettrahmen wechselt auf Magenta, und alle Felder werden einheitlich "tiefes Wasser" `#FBFCF8`. Die Erfolgsmeldung steht als Kartenkartusche mit Doppelrahmen darüber.

## Geprüfte Optionen
- **Seekarte (Lotung und Magenta):** Gewählt. Die Flachwasser/Tiefwasser-Logik trennt Blöcke sauber, Magenta ist als Warnfarbe etabliert, und die Richtung ist neu gegenüber der bisherigen Liste.
- **Bahnhofs-Anzeigetafel (Fahrplan, dunkel mit gelber Schrift, nach Schweizer Signaletik):** Verworfen. Sie ist stark lesbar, aber ein dunkles Brett mit Leuchtziffern ist in Spielen sehr gängig, und die Blocktrennung bräuchte mehr Aufwand ohne eigene Idee.
- **Glas/Weichzeichner und Minimalismus (aktueller Mobile-Trend):** Verworfen. Transparente Flächen schwächen den Kontrast für Auswahl und Konflikt, und der Stil ist beliebig und kaum eigenständig.
- **Blaupause/technische Zeichnung:** Verworfen. Sie liegt zu nah am Rechenheft (Blau auf Raster) und wäre wieder ein Papier-Look.

## Quellen
Aus den Suchergebnissen gesehen, nicht einzeln geöffnet:
- [NOAA Chart No. 1](https://www.nauticalcharts.noaa.gov:443/publications/docs/us-chart-1/ChartNo1.pdf)
- [OpenSeaMap: Farben](https://wiki.openstreetmap.org/wiki/OpenSeaMap/Colours)
- [Understanding Paper Nautical Chart Symbology (Australian Hydrographic Office)](https://www.hydro.gov.au/sites/default/files/2026-06/PNC%20-%20Understanding%20Paper%20Nautical%20Chart%20Symbology.pdf)
- [What Each Color Means On Nautical Charts](https://www.saltstrong.com/?p=34726)
- [Design Manual for the Swiss Federal Railways (SEGD)](https://segd.org/resources/design-manual-swiss-federal-railways/)
- [SBB Visual Information System (People's Graphic Design Archive)](https://peoplesgdarchive.org/item/17132/swiss-federal-railways-sbb-visual-information-system)
- [The Very Best in Mobile Game UI Designs (2026 Review)](https://pixune.com/blog/best-examples-mobile-game-ui-design/)
- [Mobile Game UI Design Trends 2026 Guide](https://adrydapp.blogspot.com/2026/03/mobile-game-ui-design-trends-2026-guide.html)