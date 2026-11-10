# Trockengarten (Karesansui): Sand, Stein und ein Tropfen Zinnober

## Entscheidung
Die Richtung „Trockengarten“ gewinnt, weil sie das Gegenteil aller bisherigen Designs ist. Die vier früheren Entwürfe leben von Nacht oder Zweifarbdruck, dieser ist ein stiller Tageslicht-Entwurf aus Sand, Granit und Moos. Ziffern in tiefem Steingrau auf hellem Sand bringen hohen Kontrast. Die 3×3-Blöcke lassen sich als Kiesfelder mit breiten Rinnen zeigen. Ein einziger Signalton, Zinnoberrot, ist allein für Konflikte reserviert und fällt in der ruhigen Fläche sofort auf. Alles geht mit reinem CSS (Flächen, Rahmen, Verläufe), ohne Dateien und Schriften.

## Vorgaben für die Oberfläche
**Farben**
- Seitenhintergrund (Kies): `#E9E3D6`
- Brettrahmen und Blockgrenzen (Granit): `#4A4A47`
- Feldfläche (Sand): `#F5F1E7`
- Feldlinien (dünn, Rechen-Linie): `#CFC8B6`
- Vorgegebene Ziffern (Stein): `#2B2B29`
- Eigene Eingaben (Indigo-Tusche): `#2F4F7A`
- Ausgewähltes Feld: Moosgrün `#B9CDA0` als Fläche mit 3 px Rahmen `#4F6B3A`
- Gleiche Zeile, Spalte und Block wie das gewählte Feld: `#EBEBD9`
- Konflikt: Zinnober `#C8381F`, Ziffer auf `#F6D5CC`
- Gelöst (`body.geloest`): Brettrahmen wechselt zu Moos `#4F6B3A`, Hintergrund zu `#DDE6CF`
- Schaltflächen: Fläche `#DAD3C2`, Text `#2B2B29`

**Schrift:** nur Systemschriften. Ziffern in `"Hiragino Sans", "Segoe UI", system-ui, sans-serif`, Gewicht 600 für vorgegebene und 400 für eigene Ziffern. Beschriftungen in Kapitälchen mit weitem Buchstabenabstand.

**Anordnung**
- Das Brett steht mittig und ist so breit wie der Bildschirm, mit quadratischen Feldern. Es ist ein Quadrat mit 3 px Granitrahmen.
- Feldlinien sind 1 px, Blockgrenzen 3 px. Dazu bekommen die Blöcke eine leichte Rinne, etwa 2 px Abstand in der Hintergrundfarbe.
- Die Stufenwahl sitzt über dem Brett als drei gleich breite, flache Steine (Buttons) mit leicht abgerundeten Ecken. Die aktive Stufe ist dunkel gefüllt (`#4A4A47`, Text `#F5F1E7`).
- Das Ziffernfeld liegt unter dem Brett als eine Reihe aus 5 plus 4 Steinen und dem Löschen-Stein. Alle Buttons sind mindestens 48 px hoch.
- Auf dem Handy steht alles in einer Spalte, auf breiten Bildschirmen bleibt das Brett begrenzt (etwa 540 px).

**Stimmung:** ruhig, leer, meditativ. Es gibt viel Weißraum, keine Schatten und keine Verläufe außer einem sehr feinen Rechenmuster im Hintergrund (`repeating-linear-gradient`, `#E3DCCB`). Die Wirkung kommt aus dem Wechsel von Sand und Stein.

**Zustände**
- **Vorgegeben:** dunkle Steinziffer, kräftig, auf Sand.
- **Eigene Eingabe:** Indigo-Ziffer, leichter, auf Sand.
- **Ausgewählt:** Moosfläche mit dickem grünem Rahmen. Die Rahmenform macht es auch ohne Farbwahrnehmung erkennbar.
- **Konflikt (`konflikt`):** zinnoberrote fette Ziffer auf rosa Fläche und ein 2 px roter Innenrahmen. Rot kommt nirgends sonst vor.

## Geprüfte Optionen
- **Trockengarten (Karesansui):** gedämpfte Sand-, Stein- und Moostöne mit einem einzigen roten Akzent. Gewählt wegen Lesbarkeit, Ruhe und klarer Abgrenzung zu den dunklen und zweifarbigen Vorgängern.
- **Taktiler Neo-Brutalismus:** dicke Rahmen, harte Schatten und grelle Flächen, ein Trend für 2026. Verworfen, weil er zu laut ist und Konflikte in der Buntheit untergehen könnten. Außerdem liegt er dem Riso-Heft farblich nah.
- **Bauhaus/De Stijl:** Primärfarben, Rechtecke und ein strenges Raster. Verworfen, weil Rot, Gelb und Blau auf 81 Feldern mit der Konfliktfarbe konkurrieren. Die Grundidee wäre aber gut umsetzbar gewesen.
- **Zusätzlich verglichen, aber nicht ausgebaut:** Papier-/Körnungs-Looks als Textur (zu nah am Risodruck).

## Quellen
- https://fireart.studio/blog/the-best-web-design-trends/
- https://www.setproduct.com/blog/retro-brutalist-ui-design-2026
- https://pixso.net/articles/neo-brutalism-design/
- https://theplusaddons.com/blog/web-design-trends-2026/
- https://www.designrush.com/agency/website-design-development/trends/web-design-trends
- https://www.moo.com/blog/de/inspiration-de/5-bauhaus-inspirierte-logos-100-jahre
- https://www.studysmarter.de/studium/architektur/architekturgeschichte/bauhaustil/
- https://projects.mcah.columbia.edu/jaanus/node/3307
- https://najga.org/7-common-raking-patterns-in-japanese-dry-landscape-gardens/
- https://www.koreajoongangdaily.com/opinion/empty-yet-full-the-stone-garden-of-ryoanji/12476213

Ich habe nur die Suchergebnisse gesehen, keine Seite geöffnet. Alles Weitere stammt aus den Kurzfassungen.