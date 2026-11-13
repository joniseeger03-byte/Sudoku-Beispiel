(function () {
  'use strict';

  var brett = document.getElementById('brett');
  var meldung = document.getElementById('meldung');
  var zellen = [];
  var puzzle = new Array(81).fill(0);
  var grid = new Array(81).fill(0);
  var vorgegeben = new Array(81).fill(false);
  var auswahl = -1;
  var stufe = 'mittel';
  var anfrage = 0;
  var geloest = false;

  // Brett aufbauen
  for (var i = 0; i < 81; i++) {
    var r = Math.floor(i / 9), c = i % 9;
    var z = document.createElement('div');
    z.className = 'zelle t' + ((Math.floor(r / 3) % 2) * 2 + (Math.floor(c / 3) % 2));
    if (c === 0) z.className += ' c0';
    else if (c % 3 === 0) z.className += ' bl';
    if (r === 0) z.className += ' r0';
    else if (r % 3 === 0) z.className += ' bo';
    z.setAttribute('data-index', i);
    z.setAttribute('role', 'gridcell');
    brett.appendChild(z);
    zellen.push(z);
  }

  function konflikte(g) {
    var res = new Set();
    function gruppe(idx) {
      var seen = {};
      idx.forEach(function (k) {
        var v = g[k];
        if (!v) return;
        (seen[v] = seen[v] || []).push(k);
      });
      Object.keys(seen).forEach(function (v) {
        if (seen[v].length > 1) seen[v].forEach(function (k) { res.add(k); });
      });
    }
    for (var a = 0; a < 9; a++) {
      var zeile = [], spalte = [], block = [];
      for (var b = 0; b < 9; b++) {
        zeile.push(a * 9 + b);
        spalte.push(b * 9 + a);
        block.push((Math.floor(a / 3) * 3 + Math.floor(b / 3)) * 9 + (a % 3) * 3 + (b % 3));
      }
      gruppe(zeile); gruppe(spalte); gruppe(block);
    }
    return res;
  }

  function zeige() {
    var k = konflikte(grid);
    var voll = grid.every(function (v) { return v > 0; });
    geloest = voll && k.size === 0;
    document.body.classList.toggle('geloest', geloest);
    var sr = auswahl >= 0 ? Math.floor(auswahl / 9) : -1;
    var sc = auswahl >= 0 ? auswahl % 9 : -1;
    var sb = auswahl >= 0 ? Math.floor(sr / 3) * 3 + Math.floor(sc / 3) : -1;
    for (var i = 0; i < 81; i++) {
      var z = zellen[i];
      var r = Math.floor(i / 9), c = i % 9;
      var b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
      z.textContent = grid[i] ? String(grid[i]) : '';
      z.classList.toggle('vorgabe', vorgegeben[i]);
      z.classList.toggle('eingabe', !vorgegeben[i] && grid[i] > 0);
      z.classList.toggle('konflikt', !geloest && k.has(i));
      z.classList.toggle('ausgewaehlt', i === auswahl);
      z.classList.toggle('mit', auswahl >= 0 && i !== auswahl && (r === sr || c === sc || b === sb));
    }
  }

  function waehle(i) {
    if (i < 0 || i > 80) return;
    auswahl = i;
    zeige();
  }

  function setze(d) {
    if (auswahl < 0 || vorgegeben[auswahl] || geloest) return;
    grid[auswahl] = d;
    zeige();
  }

  function neu(s) {
    stufe = s;
    document.querySelectorAll('[data-stufe]').forEach(function (b) {
      b.classList.toggle('aktiv', b.getAttribute('data-stufe') === s);
    });
    var mein = ++anfrage;
    meldung.textContent = 'Lade Rätsel …';
    fetch('api/neu?stufe=' + encodeURIComponent(s))
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (d) {
        if (mein !== anfrage) return;
        puzzle = d.puzzle.slice();
        grid = d.puzzle.slice();
        vorgegeben = d.puzzle.map(function (v) { return v !== 0; });
        auswahl = -1;
        meldung.textContent = '';
        zeige();
      })
      .catch(function () {
        if (mein !== anfrage) return;
        meldung.textContent = 'Rätsel konnte nicht geladen werden.';
      });
  }

  brett.addEventListener('click', function (e) {
    var z = e.target.closest('[data-index]');
    if (z) waehle(parseInt(z.getAttribute('data-index'), 10));
  });

  document.querySelectorAll('[data-digit]').forEach(function (b) {
    b.addEventListener('click', function () {
      setze(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  document.querySelectorAll('[data-stufe]').forEach(function (b) {
    b.addEventListener('click', function () {
      neu(b.getAttribute('data-stufe'));
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (k >= '1' && k <= '9' && k.length === 1) {
      setze(parseInt(k, 10));
      e.preventDefault();
    } else if (k === 'Backspace' || k === 'Delete') {
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

  neu(stufe);
})();
