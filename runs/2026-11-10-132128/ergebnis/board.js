(function () {
  'use strict';

  var brettEl = document.getElementById('brett');
  var meldungEl = document.getElementById('meldung');
  var stufenBtns = document.querySelectorAll('[data-stufe]');

  var zellen = [];
  var grid = new Array(81).fill(0);
  var vorgabe = new Array(81).fill(false);
  var auswahl = -1;
  var stufe = 'mittel';
  var anfrage = 0;

  // Brett aufbauen: 81 Felder, Ziffer als Text
  for (var i = 0; i < 81; i++) {
    var z = document.createElement('div');
    z.className = 'zelle';
    z.setAttribute('data-index', String(i));
    z.setAttribute('role', 'gridcell');
    if (i % 9 === 2 || i % 9 === 5) z.classList.add('blockrechts');
    if (Math.floor(i / 9) === 2 || Math.floor(i / 9) === 5) z.classList.add('blockunten');
    brettEl.appendChild(z);
    zellen.push(z);
  }

  brettEl.addEventListener('click', function (e) {
    var z = e.target.closest('[data-index]');
    if (!z) return;
    waehle(parseInt(z.getAttribute('data-index'), 10));
  });

  function waehle(i) {
    auswahl = i;
    zeichne();
  }

  function setze(ziffer) {
    if (auswahl < 0 || vorgabe[auswahl]) return;
    grid[auswahl] = ziffer;
    zeichne();
  }

  function konflikte(g) {
    var bad = new Set();
    var gruppen = [];
    var a, b, k;
    for (a = 0; a < 9; a++) {
      var zeile = [], spalte = [], block = [];
      for (b = 0; b < 9; b++) {
        zeile.push(a * 9 + b);
        spalte.push(b * 9 + a);
        var br = Math.floor(a / 3) * 3 + Math.floor(b / 3);
        var bc = (a % 3) * 3 + (b % 3);
        block.push(br * 9 + bc);
      }
      gruppen.push(zeile, spalte, block);
    }
    gruppen.forEach(function (gr) {
      var gesehen = {};
      gr.forEach(function (idx) {
        var v = g[idx];
        if (!v) return;
        (gesehen[v] = gesehen[v] || []).push(idx);
      });
      for (k in gesehen) {
        if (gesehen[k].length > 1) gesehen[k].forEach(function (idx) { bad.add(idx); });
      }
    });
    return bad;
  }

  function zeichne() {
    var bad = konflikte(grid);
    var gefuellt = 0;
    var ar = auswahl >= 0 ? Math.floor(auswahl / 9) : -1;
    var ac = auswahl >= 0 ? auswahl % 9 : -1;
    var ab = auswahl >= 0 ? Math.floor(ar / 3) * 3 + Math.floor(ac / 3) : -1;

    for (var i = 0; i < 81; i++) {
      var z = zellen[i];
      var v = grid[i];
      if (v) gefuellt++;
      z.textContent = v ? String(v) : '';
      var r = Math.floor(i / 9), c = i % 9;
      var b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
      z.classList.toggle('vorgabe', vorgabe[i]);
      z.classList.toggle('eigen', !vorgabe[i] && v !== 0);
      z.classList.toggle('focus', i === auswahl);
      z.classList.toggle('peer', auswahl >= 0 && i !== auswahl && (r === ar || c === ac || b === ab));
      z.classList.toggle('konflikt', bad.has(i));
    }

    var geloest = gefuellt === 81 && bad.size === 0;
    document.body.classList.toggle('geloest', geloest);
    meldungEl.textContent = geloest ? 'Geschafft! Das Rätsel ist richtig gelöst.' : '';
  }

  function neu(s) {
    stufe = s;
    stufenBtns.forEach(function (b) {
      b.classList.toggle('aktiv', b.getAttribute('data-stufe') === s);
    });
    var mein = ++anfrage;
    meldungEl.textContent = 'Lade Rätsel …';
    fetch('api/neu?stufe=' + encodeURIComponent(s))
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (d) {
        if (mein !== anfrage) return;
        grid = d.puzzle.slice();
        vorgabe = grid.map(function (v) { return v !== 0; });
        auswahl = -1;
        zeichne();
      })
      .catch(function () {
        if (mein !== anfrage) return;
        meldungEl.textContent = 'Rätsel konnte nicht geladen werden.';
      });
  }

  stufenBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      neu(b.getAttribute('data-stufe'));
    });
  });

  document.querySelectorAll('[data-digit]').forEach(function (b) {
    // Auswahl nicht durch Fokuswechsel stören
    b.addEventListener('mousedown', function (e) { e.preventDefault(); });
    b.addEventListener('click', function () {
      setze(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (/^[1-9]$/.test(k)) {
      e.preventDefault();
      setze(parseInt(k, 10));
    } else if (k === 'Delete' || k === 'Backspace') {
      e.preventDefault();
      setze(0);
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

  neu(stufe);
})();
