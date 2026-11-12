# Herbarium-Bogen: gepresstes Papier, Pflanzenetikett und Sepiatinte

## Entscheidung
Der Herbarium-Bogen hat gewonnen, weil er sich von allen bisherigen Designs deutlich unterscheidet. Es ist ein warmes, mattes Naturpapier mit grüner Tinte, ohne Nachtmodus, Neon oder harte Schatten. Die Ziffern stehen als dunkle Tinte auf hellem Grund und bleiben auf dem Smartphone sehr gut lesbar. Die Blöcke werden durch Rahmenlinien wie bei einem Archivbogen getrennt, und Auswahl und Konflikt bekommen je eine eigene Form- und Farbsprache. Alles lässt sich mit reinem CSS umsetzen: Verläufe für die Papierfaser, Rahmen, Systemschrift mit Serifen.

## Vorgaben für die Oberfläche
**Farben**
- Seitenhintergrund (Schreibtisch, Pappe): `#CFC4A8`
- Bogenpapier (Brett und Karte): `#F3EBD6`
- Feinraster und Papierfasern (leichte Verläufe): `#E6DCC0`
- Tinte, Ziffern und dicke Blocklinien: `#2B2A1E`
- Dünne Feldlinien: `#A99F80`
- Vorgegebene Zahlen (Druckfarbe, kräftig): `#1F3A2B` (Tannengrün)
- Eigene Eingaben (Sepiatinte): `#7A4A1E`
- Ausgewählt: Feldfüllung `#F2D77A` (Blütengelb) mit 3 px Innenrahmen `#1F3A2B`. Zeile, Spalte und Block der Auswahl liegen leicht darunter bei `#EADFB8`.
- Konflikt: Füllung `#E9B8A6` (Krapp hell), Ziffer `#8C1D18`, fett, plus ein Streifen aus `repeating-linear-gradient` in `#C4553E` am Feldrand. So ist der Konflikt auch ohne Farbwahrnehmung an Fett und Streifen erkennbar.
- Gelöst: Rahmen und Etikett wechseln zu `#4F7A3A` (Blattgrün), dazu ein Stempeltext „Bestimmt“ per `::after`.
- Buttons: Grundfläche `#E6DCC0`, Rand `#2B2A1E`, aktive Stufe `#1F3A2B` mit Text `#F3EBD6`.

**Schrift** (nur Systemschriften)
- Ziffern im Brett: `Georgia, "Times New Roman", serif`, fett für Vorgaben, normal für eigene Eingaben. Größe etwa 60 % der Feldhöhe.
- Beschriftung, Etikett und Buttons: `"Courier New", ui-monospace, monospace` in Kapitälchen (`font-variant: small-caps`) oder Großbuchstaben mit Laufweite. Das wirkt wie ein Sammlungsetikett.

**Anordnung**
- Der Bogen steht als zentrierte Karte (max. 460 px, auf dem Handy volle Breite minus 12 px Rand) mit einem doppelten Innenrahmen und leichten Papierfasern. Oben sitzt ein Etikett, ein kleines Rechteck wie ein Herbariumsschild: „Sudoku · Stufe: mittel“.
- Das Brett ist quadratisch (`aspect-ratio: 1`) und nutzt CSS Grid mit 9×9 Feldern. Feine Linien 1 px `#A99F80`. Die 3×3-Blöcke sind durch 3 px Linien in `#2B2A1E` getrennt, und der Außenrahmen ist 4 px stark. Alternativ kann man zusätzlich 3 px Abstand zwischen den Blöcken lassen.
- Die Stufenwahl liegt als drei gleich breite Reiter („leicht / mittel / schwer“) in einer Zeile oberhalb des Bretts, wie Registerkarten. Sie wirken wie Karteireiter und sind mindestens 44 px hoch.
- Das Ziffernfeld liegt unterhalb des Bretts als 5×2-Raster: 1–5 in der oberen Reihe, 6–9 und Löschen (⌫) in der unteren. Die Tasten sind mindestens 48 px groß, haben abgerundete Ecken (4 px) und einen 2 px Rand in Tinte, aber keinen Schlagschatten.
- Hinweis- und Lösungsbutton sind kleiner und stehen als Textlinks mit Unterstreichung unter dem Ziffernfeld.

**Stimmung**
Ruhig, sammelnd und handschriftlich. Es soll sich anfühlen, als würde man einen Pflanzenbogen im Archiv bestimmen. Es gibt keine Animationen außer einem kurzen Einblenden (150 ms) der Auswahl.

**Zustände**
- **Vorgegeben (`vorgegeben`):** Tannengrün `#1F3A2B`, fett, Serifenziffer, Feldhintergrund leicht dunkler als das Papier (`#EDE3C8`).
- **Eigene Eingabe:** Sepia `#7A4A1E`, normale Strichstärke, Hintergrund Papierfarbe. So lassen sich Vorgabe und Eingabe nicht nur an der Farbe, sondern auch am Gewicht unterscheiden.
- **Ausgewählt (`selected`):** Blütengelb mit dunkelgrünem Innenrahmen, verwandte Felder schwach getönt.
- **Konflikt (`konflikt`):** Krapp-Füllung, dunkelrote fette Ziffer, diagonale Streifen am Rand. Die Auswahl hat Vorrang beim Rahmen, der Konflikt bei der Füllung, sodass ein gewähltes Feld im Konflikt gelb gerahmt und rot gefüllt ist.
- **Gelöst (`geloest`):** Blattgrüner Rahmen, Stempel „Bestimmt“ über dem Etikett.
- Fokus per Tastatur: 3 px Umriss in `#1F3A2B` mit 2 px Abstand.

## Geprüfte Optionen
- **Herbarium-Bogen (gewählt):** Gepresstes Papier, Pflanzenetikett, Tannengrün und Sepia. Er ist neu gegenüber den bisherigen Designs, gut lesbar und ohne Bilder oder Schriftdateien machbar.
- **Bauhaus-Schablone (verworfen):** Geometrische Schablonenziffern nach Albers' Schablonenschrift von 1926 mit Primärfarben. Das Konzept ist stark, aber ohne eigene Schrift sind die Ziffern mit Systemschriften nicht umsetzbar. Zudem liegen die kräftigen Flächen und Kanten zu nah am Kartonbrett-Brutalismus und am Risodruck.
- **Hanafuda-Spielkarte (verworfen):** Lack, Schwarz und Rot, jahreszeitliche Motive wie bei den Hanafuda-Karten. Die Stimmung ist schön, aber ohne Illustrationen bleibt nur eine dunkle Fläche mit Rot, die den Nachtdesigns (Anzeigetafel, Seekarte, Lichtspielhaus) und dem Karesansui zu ähnlich wäre.
- **Aktuelle Mobile-Puzzle-UI (verworfen):** Minimalistisch, mit Bewegung und Anpassbarkeit, wie es Trendübersichten beschreiben. Das ist austauschbar und gäbe keine eigene Handschrift.

## Quellen
Diese Adressen habe ich in den Suchergebnissen gesehen (nicht einzeln geöffnet):
- https://blazetype.eu/blog/stencil-an-avoided-history-2-2
- https://www.albersfoundation.org/news/schablonenschrift-in-the-times-literary-supplement
- https://www.typeoff.de/2011/08/some-thoughts-on-geometric-type/
- https://www.wikiwand.com/en/articles/Hanafuda
- https://peoplesgdarchive.org/item/14086/plum-blossoms-a-series-of-hanafuda-cards
- https://www.vanishingincmagic.com/playing-cards/hanami-hanafuda-playing-cards/
- https://pixune.com/?p=56786
- https://techcabal.com/?p=180239
- https://contra.com/p/mRqN33Wq-sudoku-lover-mobile-game-uiux-design

Zum Herbarium-Konzept selbst habe ich keine eigene Quelle gefunden. Die Suche nach Herbarium-Tafeln ergab nichts Passendes. Die Richtung beruht auf allgemeinem Wissen über Herbariumsbögen und ist von mir frei gestaltet.