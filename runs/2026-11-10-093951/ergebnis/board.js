(function () {
  'use strict';

  var brett = document.getElementById('brett');
  var meldung = document.getElementById('meldung');
  var stufenButtons = document.querySelectorAll('[data-stufe]');
  var cells = [];
  var puzzle = [];      // Vorgaben (0 = leer)
  var solution = null;
  var grid = [];        // aktueller Stand
  var selected = -1;
  var anfrage = 0;
  var geladen = false;

  // Brett aufbauen
  for (var i = 0; i < 81; i++) {
    var c = document.createElement('div');
    c.className = 'feld';
    c.setAttribute('data-index', String(i));
    c.setAttribute('role', 'gridcell');
    var col = i % 9, row = Math.floor(i / 9);
    if (col % 3 === 2 && col !== 8) c.classList.add('blockrechts');
    if (row % 3 === 2 && row !== 8) c.classList.add('blockunten');
    brett.appendChild(c);
    cells.push(c);
  }

  brett.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-index]') : null;
    if (t && brett.contains(t)) select(parseInt(t.getAttribute('data-index'), 10));
  });

  function select(idx) {
    selected = idx;
    render();
  }

  function berechneKonflikte(g) {
    var set = {};
    var groups = [], k, j;
    for (k = 0; k < 9; k++) {
      var r = [], cc = [], b = [];
      for (j = 0; j < 9; j++) {
        r.push(k * 9 + j);
        cc.push(j * 9 + k);
        b.push((Math.floor(k / 3) * 3 + Math.floor(j / 3)) * 9 + (k % 3) * 3 + (j % 3));
      }
      groups.push(r, cc, b);
    }
    groups.forEach(function (grp) {
      var seen = {};
      grp.forEach(function (idx) {
        var v = g[idx];
        if (!v) return;
        (seen[v] = seen[v] || []).push(idx);
      });
      Object.keys(seen).forEach(function (v) {
        if (seen[v].length > 1) seen[v].forEach(function (idx) { set[idx] = true; });
      });
    });
    return set;
  }

  function istGeloest(konf) {
    if (!geladen) return false;
    for (var i = 0; i < 81; i++) {
      if (!grid[i] || konf[i]) return false;
      if (solution && grid[i] !== solution[i]) return false;
    }
    return true;
  }

  function render() {
    var konf = berechneKonflikte(grid);
    var sr = selected >= 0 ? Math.floor(selected / 9) : -1;
    var sc = selected >= 0 ? selected % 9 : -1;
    for (var i = 0; i < 81; i++) {
      var el = cells[i];
      var v = grid[i] || 0;
      var txt = v ? String(v) : '';
      if (el.textContent !== txt) el.textContent = txt;
      var given = geladen && puzzle[i] !== 0;
      var r = Math.floor(i / 9), c = i % 9;
      el.classList.toggle('vorgabe', given);
      el.classList.toggle('eigen', geladen && !given && v !== 0);
      el.classList.toggle('konflikt', !!konf[i]);
      el.classList.toggle('ausgewaehlt', i === selected);
      var verw = selected >= 0 && i !== selected && (r === sr || c === sc ||
        (Math.floor(r / 3) === Math.floor(sr / 3) && Math.floor(c / 3) === Math.floor(sc / 3)));
      el.classList.toggle('verwandt', verw);
      el.setAttribute('aria-selected', i === selected ? 'true' : 'false');
      el.setAttribute('aria-label', 'Reihe ' + (r + 1) + ', Spalte ' + (c + 1) + ', ' +
        (v ? v + (given ? ', vorgegeben' : '') : 'leer') + (konf[i] ? ', Konflikt' : ''));
    }
    document.body.classList.toggle('geloest', istGeloest(konf));
  }

  function setDigit(d) {
    if (!geladen || selected < 0) return;
    if (puzzle[selected] !== 0) return;
    if (document.body.classList.contains('geloest')) return;
    grid[selected] = d;
    render();
  }

  function move(dr, dc) {
    if (selected < 0) { select(0); return; }
    var r = Math.min(8, Math.max(0, Math.floor(selected / 9) + dr));
    var c = Math.min(8, Math.max(0, selected % 9 + dc));
    select(r * 9 + c);
  }

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (k >= '1' && k <= '9') { setDigit(parseInt(k, 10)); e.preventDefault(); }
    else if (k === 'Delete' || k === 'Backspace' || k === '0') { setDigit(0); e.preventDefault(); }
    else if (k === 'ArrowUp') { move(-1, 0); e.preventDefault(); }
    else if (k === 'ArrowDown') { move(1, 0); e.preventDefault(); }
    else if (k === 'ArrowLeft') { move(0, -1); e.preventDefault(); }
    else if (k === 'ArrowRight') { move(0, 1); e.preventDefault(); }
  });

  Array.prototype.forEach.call(document.querySelectorAll('[data-digit]'), function (b) {
    b.addEventListener('click', function () {
      setDigit(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  Array.prototype.forEach.call(stufenButtons, function (b) {
    b.addEventListener('click', function () { neu(b.getAttribute('data-stufe')); });
  });

  function neu(stufe) {
    var mine = ++anfrage;
    Array.prototype.forEach.call(stufenButtons, function (b) {
      var an = b.getAttribute('data-stufe') === stufe;
      b.classList.toggle('aktiv', an);
      b.setAttribute('aria-pressed', an ? 'true' : 'false');
    });
    meldung.textContent = 'Lade Rätsel …';
    fetch('api/neu?stufe=' + encodeURIComponent(stufe))
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        if (mine !== anfrage) return;
        puzzle = data.puzzle.slice();
        solution = data.solution ? data.solution.slice() : null;
        grid = data.puzzle.slice();
        geladen = true;
        selected = -1;
        meldung.textContent = '';
        render();
      })
      .catch(function () {
        if (mine !== anfrage) return;
        meldung.textContent = 'Rätsel konnte nicht geladen werden. Stufe erneut wählen.';
      });
  }

  grid = new Array(81).fill(0);
  render();
  neu('mittel');
})();
