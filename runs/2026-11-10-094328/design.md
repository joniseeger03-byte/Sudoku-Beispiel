# Anzeigetafel bei Nacht

## Entscheidung
Das Sudoku sieht aus wie eine dunkle Fahrgast-Anzeigetafel mit Bernstein-Ziffern auf fast schwarzem Grund. Diese Richtung ist als einzige dunkel und technisch-nüchtern. Alle bisherigen Designs sind hell, handwerklich oder dekorativ. Bernstein und Off-White auf Dunkel haben auf dem Smartphone sehr hohen Kontrast. Auswahl und Konflikt sind über Farbe und Muster getrennt erkennbar, also auch bei Farbschwäche. Umsetzbar ist alles mit reinem CSS (Flächen, Linien, `repeating-linear-gradient`) und Systemschriften.

## Vorgaben für die Oberfläche
**Farben**
- Seitenhintergrund: `#14161A`
- Brettfläche und Zellen: `#1E2227`
- Dünne Zelllinien: `#3A4048`, 1 px
- Blocklinien (3×3): `#E9E4D4`, 3 px. Das Brett hat außen einen 3-px-Rahmen in derselben Farbe.
- Text und Beschriftung: `#E9E4D4`
- Gedämpfter Text: `#9AA0A8`
- Akzent Bernstein: `#FFB81C`
- Konfliktrot: `#E5484D`, Konfliktfläche `#4A1A1D`
- Gelöst: `#4ADE80`, wird für Brettrahmen und Blocklinien verwendet.

**Schrift**
- Nur Systemschriften: `"Helvetica Neue", Arial, system-ui, sans-serif`. Das Brett nutzt `font-variant-numeric: tabular-nums`.
- Ziffern im Brett: fett, ca. 60 % der Zellhöhe.
- Beschriftungen: Großbuchstaben, `letter-spacing: .08em`, klein (ca. 12–13 px).

**Anordnung**
- Eine Spalte, mobil zuerst. Oben steht eine schmale Kopfzeile wie bei einer Abfahrtstafel, darunter das Brett und darunter das Ziffernfeld.
- Kopfzeile: links der Titel „SUDOKU" in Großbuchstaben, darunter die Stufenwahl. Die drei Buttons `leicht`, `mittel` und `schwer` stehen als Segmentleiste nebeneinander, jeweils mit mindestens 44 px Höhe. Die aktive Stufe hat einen Bernsteinfüllung mit dunkler Schrift. Inaktive Stufen haben eine 1-px-Umrandung in `#3A4048`.
- Brett: quadratisch, Breite = `min(100vw − 24px, 520px)`, zentriert. Die Zellen sind quadratisch, ohne Rundungen. Die Blocklinien sind dick und hell, die Zelllinien dünn und dunkel. So sind die 3×3-Blöcke auch bei kleiner Größe sofort erkennbar.
- Ziffernfeld: 5 Spalten, mit 1–5 oben und 6–9 plus Löschen (`0`, „⌫" oder „Löschen") unten. Die Tasten sind mindestens 52 px hoch, haben Fläche `#262B31`, Rand `#3A4048`, bernsteinfarbene Ziffern und eine Pressed-Zustand-Invertierung (Bernsteinfläche, dunkle Ziffer).
- Stimmung: nachts am Bahnsteig, ruhig und präzise, ohne Verzierung, mit wenig Bewegung. Ein kurzes Aufleuchten (z. B. 120 ms Farbwechsel) ist erlaubt, aber nicht nötig.

**Zustände**
- Vorgegeben: Ziffer `#E9E4D4`, Fett (700), Zellfläche `#1E2227`.
- Eigene Eingabe: Ziffer Bernstein `#FFB81C`, normales bis halbfettes Gewicht (600), gleiche Zellfläche.
- Ausgewählt: Zellfläche `#FFB81C`, Ziffer `#14161A`, zusätzlich ein innerer Rand von 3 px in `#E9E4D4` (`box-shadow: inset`). Zeile, Spalte und Block des gewählten Felds bekommen eine leichte Aufhellung `#2A2F36`. Das ist das stärkste Signal auf dem Brett.
- Konflikt (Klasse `konflikt`): Zellfläche `#4A1A1D`, Ziffer `#FF8A8E` und fett. Dazu ein diagonales Streifenmuster (`repeating-linear-gradient(45deg, #E5484D55 0 3px, transparent 3px 8px)`) und ein 2-px-Innenrand `#E5484D`. Das Muster sorgt dafür, dass der Konflikt nicht nur an der Farbe erkennbar ist. Liegt ein Konflikt auf der ausgewählten Zelle, bleibt die Bernsteinfläche, und die Streifen und der rote Rand kommen darüber.
- Gelöst (Klasse `geloest` am `body`): Blocklinien und Rahmen wechseln auf `#4ADE80`. Alle Ziffern werden in `#4ADE80` dargestellt, und über dem Brett erscheint in der Kopfzeile ein Textsignal wie „ANGEKOMMEN". Dieses Signal ist reiner Text und braucht keine Bilder.

## Geprüfte Optionen
- **Anzeigetafel bei Nacht (gewählt):** Dunkel, bernsteinfarbene Ziffern, starke Linien. Gewonnen, weil sie sich klar von allen bisherigen hellen Designs absetzt und auf kleinen Bildschirmen den besten Kontrast liefert.
- **Risograph-Druck:** Zwei Fluoreszenzfarben auf Papier mit leichtem Versatz. Verworfen, weil sie den Knallfarben des Neo-Brutalismus und der Papieranmutung der Morgenzeitung zu nahe kommt und der Versatz bei Ziffern die Lesbarkeit schwächt.
- **Glassmorphismus mit weichem Verlauf:** Aktuelle Strömung mit Unschärfe und Schichten. Verworfen, weil Unschärfe und halbtransparente Flächen den Kontrast der Blocklinien auf dem Smartphone verringern und auf schwächeren Geräten Leistung kosten.
- **Retro-Y2K/„Dopamine"-Look:** Gesättigte Farben und Verzierungen. Verworfen, weil viele gesättigte Farben nebeneinander Auswahl und Konflikt unklar machen würden.
- **Schweizer Rasterstil (Müller-Brockmann-Tradition):** Serifenlos, systematisch, wenige Farben. Teilweise übernommen, vor allem Großbuchstaben-Beschriftung, klare Ordnung und Segmentleiste, aber nicht als eigene Richtung, weil er hell auf Papier gedacht ist und zu nah an Bauplan und Morgenzeitung liegt.

## Quellen
- https://www.aufaitux.com/blog/latest-web-design-trends/
- https://line25.com/articles/web-design-trends-2026/
- https://clay.global/blog/web-design-guide/web-design-trends
- https://www.hostinger.com/uk/tutorials/web-design-trends/
- https://www.webflow.com (nur als Treffer „webflow 8 web design trends to watch in 2026" gesehen: https://www.plushcap.com/content/webflow/blog/webflow-8-web-design-trends-to-watch-in-2026)
- https://www.netzwoche.ch/news/2015-03-20/die-inspirationsquelle-fuer-das-metro-style-design
- https://www.srf.ch/kultur/kunst/schweizer-designgeschichte-sbb-macht-halt-im-museum-fuer-gestaltung
- https://revistas.usp.br/significacao/article/view/65570
- https://ixd.prattsi.org/2022/09/design-critique-hungry-cat-nonogram/
- https://forum.figma.com/report-a-problem-6/block-blast-ui-ux-pattern-mobile-prototype-assets-interaction-48208

Ich habe nur die Suchergebnisse gesehen und keine der Seiten per WebFetch geöffnet.