(function () {
  'use strict';

  var brett = document.getElementById('brett');
  var meldung = document.getElementById('meldung');
  var zellen = [];
  var puzzle = new Array(81).fill(0);
  var solution = null;
  var grid = new Array(81).fill(0);
  var gewaehlt = -1;
  var stufe = 'mittel';
  var anfrage = 0;

  // Brett aufbauen
  for (var i = 0; i < 81; i++) {
    var z = document.createElement('div');
    z.className = 'zelle';
    z.setAttribute('role', 'gridcell');
    z.setAttribute('data-index', String(i));
    var r = Math.floor(i / 9), c = i % 9;
    if (c % 3 === 2 && c < 8) z.classList.add('blockrechts');
    if (r % 3 === 2 && r < 8) z.classList.add('blockunten');
    brett.appendChild(z);
    zellen.push(z);
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
        block.push((Math.floor(a / 3) * 3 + Math.floor(b / 3)) * 9 + (a % 3) * 3 + (b % 3));
      }
      gruppen.push(zeile, spalte, block);
    }
    gruppen.forEach(function (gr) {
      var seen = {};
      gr.forEach(function (idx) {
        var v = g[idx];
        if (!v) return;
        (seen[v] = seen[v] || []).push(idx);
      });
      for (k in seen) {
        if (seen[k].length > 1) seen[k].forEach(function (idx) { bad.add(idx); });
      }
    });
    return bad;
  }

  function render() {
    var bad = konflikte(grid);
    var sel = gewaehlt;
    var selVal = sel >= 0 ? grid[sel] : 0;
    var voll = true;
    for (var i = 0; i < 81; i++) {
      var z = zellen[i];
      var v = grid[i];
      if (!v) voll = false;
      var text = v ? String(v) : '';
      if (z.textContent !== text) z.textContent = text;
      var vorgabe = puzzle[i] !== 0;
      z.classList.toggle('vorgegeben', vorgabe);
      z.classList.toggle('eigen', !vorgabe && v !== 0);
      z.classList.toggle('konflikt', bad.has(i));
      z.classList.toggle('selected', i === sel);
      var peer = false;
      if (sel >= 0 && i !== sel) {
        var r = Math.floor(i / 9), c = i % 9, sr = Math.floor(sel / 9), sc = sel % 9;
        peer = r === sr || c === sc ||
          (Math.floor(r / 3) === Math.floor(sr / 3) && Math.floor(c / 3) === Math.floor(sc / 3));
      }
      z.classList.toggle('peer', peer);
      z.classList.toggle('gleich', selVal !== 0 && v === selVal);
    }
    var geloest = voll && bad.size === 0;
    if (geloest && solution) {
      for (var j = 0; j < 81; j++) if (grid[j] !== solution[j]) { geloest = false; break; }
    }
    document.body.classList.toggle('geloest', geloest);
  }

  function waehle(i) {
    gewaehlt = i;
    render();
  }

  function setze(v) {
    if (gewaehlt < 0) return;
    if (puzzle[gewaehlt] !== 0) return; // Vorgaben sind fix
    grid[gewaehlt] = v;
    render();
  }

  brett.addEventListener('click', function (e) {
    var z = e.target.closest('.zelle');
    if (z) waehle(parseInt(z.getAttribute('data-index'), 10));
  });

  document.querySelectorAll('[data-digit]').forEach(function (b) {
    b.addEventListener('click', function () {
      setze(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (/^[1-9]$/.test(k)) {
      setze(parseInt(k, 10));
      e.preventDefault();
    } else if (k === 'Delete' || k === 'Backspace') {
      setze(0);
      e.preventDefault();
    } else if (k.indexOf('Arrow') === 0) {
      e.preventDefault();
      if (gewaehlt < 0) { waehle(0); return; }
      var r = Math.floor(gewaehlt / 9), c = gewaehlt % 9;
      if (k === 'ArrowUp') r = Math.max(0, r - 1);
      else if (k === 'ArrowDown') r = Math.min(8, r + 1);
      else if (k === 'ArrowLeft') c = Math.max(0, c - 1);
      else if (k === 'ArrowRight') c = Math.min(8, c + 1);
      waehle(r * 9 + c);
    }
  });

  function neu(s) {
    stufe = s;
    document.querySelectorAll('[data-stufe]').forEach(function (b) {
      b.classList.toggle('aktiv', b.getAttribute('data-stufe') === s);
    });
    var meine = ++anfrage;
    meldung.textContent = 'Lade Rätsel …';
    fetch('api/neu?stufe=' + s)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (d) {
        if (meine !== anfrage) return;
        puzzle = d.puzzle.slice();
        solution = d.solution ? d.solution.slice() : null;
        grid = d.puzzle.slice();
        gewaehlt = -1;
        meldung.textContent = '';
        render();
      })
      .catch(function () {
        if (meine !== anfrage) return;
        meldung.textContent = 'Rätsel konnte nicht geladen werden.';
      });
  }

  document.querySelectorAll('[data-stufe]').forEach(function (b) {
    b.addEventListener('click', function () {
      neu(b.getAttribute('data-stufe'));
    });
  });

  neu(stufe);
})();
