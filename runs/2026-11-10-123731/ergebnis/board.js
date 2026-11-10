(function () {
  'use strict';

  var brett = document.getElementById('brett');
  var meldung = document.getElementById('meldung');
  var stufenButtons = document.querySelectorAll('[data-stufe]');
  var zellen = [];
  var werte = new Array(81).fill(0);
  var vorgabe = new Array(81).fill(false);
  var auswahl = -1;
  var aktuelleStufe = 'mittel';
  var ladeZaehler = 0;

  // Brett aufbauen
  for (var i = 0; i < 81; i++) {
    var z = document.createElement('div');
    z.className = 'feld';
    z.setAttribute('data-index', String(i));
    z.setAttribute('role', 'gridcell');
    var r = Math.floor(i / 9), c = i % 9;
    if (c === 2 || c === 5) z.classList.add('br');
    if (r === 2 || r === 5) z.classList.add('bb');
    brett.appendChild(z);
    zellen.push(z);
  }

  brett.addEventListener('click', function (e) {
    var t = e.target.closest('[data-index]');
    if (!t) return;
    waehle(parseInt(t.getAttribute('data-index'), 10));
  });

  function waehle(i) {
    auswahl = i;
    zeichne();
  }

  function berechneKonflikte() {
    var bad = new Set();
    var einheiten = [];
    var k, j, m, idx;
    for (k = 0; k < 9; k++) {
      var zeile = [], spalte = [], block = [];
      for (j = 0; j < 9; j++) {
        zeile.push(k * 9 + j);
        spalte.push(j * 9 + k);
        var br = Math.floor(k / 3) * 3, bc = (k % 3) * 3;
        block.push((br + Math.floor(j / 3)) * 9 + bc + (j % 3));
      }
      einheiten.push(zeile, spalte, block);
    }
    einheiten.forEach(function (u) {
      var seen = {};
      for (m = 0; m < u.length; m++) {
        idx = u[m];
        var v = werte[idx];
        if (!v) continue;
        (seen[v] = seen[v] || []).push(idx);
      }
      Object.keys(seen).forEach(function (v) {
        if (seen[v].length > 1) seen[v].forEach(function (x) { bad.add(x); });
      });
    });
    return bad;
  }

  function zeichne() {
    var bad = berechneKonflikte();
    var voll = true;
    var ar = auswahl >= 0 ? Math.floor(auswahl / 9) : -1;
    var ac = auswahl >= 0 ? auswahl % 9 : -1;
    var aw = auswahl >= 0 ? werte[auswahl] : 0;
    for (var i = 0; i < 81; i++) {
      var z = zellen[i];
      var v = werte[i];
      if (!v) voll = false;
      var r = Math.floor(i / 9), c = i % 9;
      z.textContent = v ? String(v) : '';
      z.classList.toggle('vorgabe', vorgabe[i]);
      z.classList.toggle('eigene', !vorgabe[i] && v !== 0);
      z.classList.toggle('konflikt', bad.has(i));
      z.classList.toggle('selected', i === auswahl);
      var peer = auswahl >= 0 && i !== auswahl && (
        r === ar || c === ac ||
        (Math.floor(r / 3) === Math.floor(ar / 3) && Math.floor(c / 3) === Math.floor(ac / 3)));
      z.classList.toggle('bereich', !!peer);
      z.classList.toggle('gleich', aw !== 0 && v === aw);
      z.setAttribute('aria-selected', i === auswahl ? 'true' : 'false');
      z.setAttribute('aria-label',
        'Zeile ' + (r + 1) + ', Spalte ' + (c + 1) + ', ' +
        (v ? 'Wert ' + v : 'leer') + (vorgabe[i] ? ', vorgegeben' : '') +
        (bad.has(i) ? ', Konflikt' : ''));
    }
    var geloest = voll && bad.size === 0;
    document.body.classList.toggle('geloest', geloest);
    if (geloest) meldung.textContent = 'Geschafft! Das Rätsel ist gelöst.';
    else if (meldung.getAttribute('data-fehler') !== '1') meldung.textContent = '';
  }

  function setze(ziffer) {
    if (auswahl < 0 || vorgabe[auswahl]) return;
    werte[auswahl] = ziffer;
    zeichne();
  }

  // Ziffernfeld
  document.querySelectorAll('[data-digit]').forEach(function (b) {
    b.addEventListener('click', function () {
      setze(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  // Tastatur
  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (/^[1-9]$/.test(k)) {
      setze(parseInt(k, 10));
      e.preventDefault();
    } else if (k === '0' || k === 'Delete' || k === 'Backspace') {
      setze(0);
      e.preventDefault();
    } else if (k.indexOf('Arrow') === 0) {
      e.preventDefault();
      if (auswahl < 0) { waehle(0); return; }
      var r = Math.floor(auswahl / 9), c = auswahl % 9;
      if (k === 'ArrowUp') r = Math.max(0, r - 1);
      else if (k === 'ArrowDown') r = Math.min(8, r + 1);
      else if (k === 'ArrowLeft') c = Math.max(0, c - 1);
      else if (k === 'ArrowRight') c = Math.min(8, c + 1);
      waehle(r * 9 + c);
    }
  });

  // Rätsel laden
  function lade(stufe) {
    aktuelleStufe = stufe;
    var mein = ++ladeZaehler;
    stufenButtons.forEach(function (b) {
      var an = b.getAttribute('data-stufe') === stufe;
      b.classList.toggle('aktiv', an);
      b.setAttribute('aria-pressed', an ? 'true' : 'false');
    });
    fetch('api/neu?stufe=' + encodeURIComponent(stufe))
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (d) {
        if (mein !== ladeZaehler) return;
        for (var i = 0; i < 81; i++) {
          var v = d.puzzle[i] | 0;
          werte[i] = v;
          vorgabe[i] = v !== 0;
        }
        auswahl = -1;
        meldung.removeAttribute('data-fehler');
        meldung.textContent = '';
        zeichne();
      })
      .catch(function () {
        if (mein !== ladeZaehler) return;
        meldung.setAttribute('data-fehler', '1');
        meldung.textContent = 'Rätsel konnte nicht geladen werden.';
      });
  }

  stufenButtons.forEach(function (b) {
    b.addEventListener('click', function () {
      lade(b.getAttribute('data-stufe'));
    });
  });

  zeichne();
  lade(aktuelleStufe);
})();
