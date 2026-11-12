# Rechenheft: Kästchenpapier, Füllerblau und Rotstift

## Entscheidung
Gewonnen hat das deutsche Schulrechenheft (Lineatur R, große Kästchen). Es ist hell und kühl-weiß, anders als die dunklen Nachtthemen und das cremefarbene Terrazzo. Das Brett folgt dem Kästchenraster, und die 3×3-Blöcke ergeben sich aus einer kräftigeren Heftrandlinie. Die Rollen sind klar getrennt: Gedrucktes ist grau, die eigene Hand ist füllerblau, und der Fehler wird wie vom Lehrer mit Rotstift angestrichen. Alles geht mit reinem HTML und CSS (Hintergrund-Gradienten, Rahmen, Systemschrift).

## Vorgaben für die Oberfläche
**Farben**
- Seite/Papier: `#F7F9F6` (leicht kühles Weiß). Das Brett liegt auf einem „Heftblatt“ in `#FFFFFF`.
- Feine Kästchenlinien: `#BcD3E6`, 1 px.
- Blockgrenzen (3×3) und Brettrand: `#3A4A5C`, 2–3 px. Dazu ein roter Heft-Randstreifen links am Seitenrand: `#E8A5A5`, 2 px.
- Vorgegebene Ziffern: `#2B2F33` (Druckgrau-Schwarz), fett (700). Zellgrund `#EEF2F0`, wie vorgedruckte Aufgaben.
- Eigene Eingabe: `#1F4FBF` (Füllerblau), normal bis mittel (500).
- Ausgewähltes Feld: Grund `#FFF3A8` (Textmarkergelb), innen 3 px Rahmen `#1F4FBF`. Zeile, Spalte und Block dürfen sehr leicht `#F1F6FB` getönt sein.
- Konflikt: Ziffer `#C62828`, Grund `#FDE3E3`, 3 px roter Innenrand `#C62828`, zusätzlich ein diagonales Rotstift-Kringel-Muster (`repeating-linear-gradient`, 45°, 1 px `#C62828` bei 25 % Deckkraft). Das erfüllt N3 (nicht nur Farbe). Der Tooltip erscheint als Zettel mit Text, z. B. „Doppelte 5 in Zeile 3“, auf `#FFFFFF` mit Rotstiftrand.
- Gelöst (`body.geloest`): Rand des Bretts wechselt auf Grün `#2E7D32`, dazu ein Haken-Banner „Richtig!“ in Grün.

**Schrift** (nur Systemschriften)
- Ziffern im Brett: `ui-rounded, "Segoe UI", system-ui, -apple-system, Roboto, sans-serif`. Bei vorgegebenen Ziffern 700, Größe ca. `clamp(20px, 6.2vw, 34px)`.
- Notizen: 9 Mini-Ziffern im 3×3-Raster innerhalb der Zelle, `#5B7FA8`, ca. 38 % der Zellhöhe.
- Titel und Labels: dieselbe Sans-Schrift, Versalien mit Abstand (`letter-spacing: .08em`), klein, in `#3A4A5C`.

**Anordnung**
- Smartphone (Hochformat): Kopf mit Titel „Sudoku“ und Timer-Schalter. Darunter die Stufenwahl als drei gleich breite Reiter („leicht / mittel / schwer“, mindestens 44 px hoch), der aktive Reiter gefüllt in `#1F4FBF` mit weißer Schrift, die anderen mit Linienrahmen. Danach das quadratische Brett über die volle Breite (`min(100vw − 16px, 480px)`), dann die Werkzeugleiste (Undo, Notizen An/Aus), dann das Ziffernfeld.
- Ziffernfeld: eine Reihe 1–9 (5+4 oder 9 einzeln bei ≥ 360 px), Löschen (`data-digit="0"`) als eigener breiter Knopf mit Symbol „⌫“. Tasten sind quadratisch, mindestens 44×44 px, mit Kästchenpapier-Optik (weiß, 1 px Rahmen, Ziffer in Füllerblau).
- Desktop: Brett links, Stufenwahl, Werkzeuge und Ziffernfeld in einer Spalte rechts.
- Zellen sind quadratisch. Die Blockgrenzen sind 2–3 px dick und `#3A4A5C`, die Zellgrenzen 1 px `#BCD3E6`. Zusätzlich hat jedes Brett außen einen Schatten ohne Weichzeichnung (`2px 2px 0 #D5DEE6`), damit es wie ein aufgelegtes Blatt wirkt.

**Stimmung**
Ruhig, konzentriert, schulisch-freundlich. Es gibt keine Verläufe und keine Animationen außer einem kurzen 120-ms-Farbwechsel bei der Auswahl.

**Zustände auf einen Blick**
- Vorgegeben: grauer Grund, fette dunkle Ziffer.
- Eigene Eingabe: weißer Grund, blaue Ziffer.
- Ausgewählt: gelber Grund und blauer Innenrand, sichtbar auch ohne Farbwahrnehmung durch den Rahmen.
- Konflikt: rote Ziffer, rosa Grund, roter Innenrand und Schraffur.

## Geprüfte Optionen
- **Rechenheft (gewählt):** Hell, haptisch, klare Rollen von Gedrucktem, eigener Hand und Korrektur. Es lässt sich rein mit CSS bauen und bleibt auf dem Smartphone gut lesbar.
- **Sashiko (Indigo mit weißem Stich):** Ein überraschender und schöner Ansatz mit handwerklicher Ruhe. Verworfen, weil das dunkle Blau zu nah an „Seekarte bei Nacht“ und „Anzeigetafel bei Nacht“ liegt.
- **Blaupause/Zyanotypie:** Weiße Linien auf tiefem Blau, mit Raster als Kernmerkmal. Verworfen, weil sie ebenfalls der Seekarte ähnelt und weiße dünne Linien auf kleinen Bildschirmen schwächer lesbar sind.
- **Typografiegetriebenes Minimal-Web (2026-Trend):** Große Schrift, eine Akzentfarbe, viel Weißraum. Verworfen, weil es als eigene Gestaltung zu austauschbar wäre und das Brett kaum einen eigenen Charakter bekäme.
- **Bauhaus-Grundfarben und Grundformen:** Kräftig und klar. Verworfen, weil die Primärfarben auf gleichgroßen Feldern mit Konfliktrot kollidieren und der Kartonbrett-Brutalismus bereits mit Gelb und harten Kanten arbeitet.

## Quellen
- https://graphicdesignjunction.com/2025/12/web-design-trends-of-2026/
- https://hostinger.com/uk/tutorials/web-design-trends/
- https://madegooddesigns.com/?p=3591
- https://core.ac.uk/download/14505701.pdf
- https://www.goethe.de/ins/ca/de/m/kul/kue/bau/ver/m08.html
- https://Www.Wikipedia.org/wiki/Blueprint
- https://chrislemke.github.io/website_designs/examples/Blueprint_Technical.html
- https://cameo.mfa.org/wiki/Blueprint_paper
- https://japanobjects.com/features/sashiko
- https://www.wikipedia.org/wiki/Sashiko
- https://www.seamwork.com/articles/sashiko
- https://www.kita.de/ratgeber/freizeit/diy-bastelbedarf/rechenheft/
- https://www.kaufland.de/product/41477141/

Die Ergebnisse habe ich nur in den Suchergebnissen gesehen, keine Seite wurde direkt geöffnet.