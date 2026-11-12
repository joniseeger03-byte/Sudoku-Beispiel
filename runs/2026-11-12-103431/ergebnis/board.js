(function () {
  'use strict';

  var brett = document.getElementById('brett');
  var meldung = document.getElementById('meldung');
  var sieg = document.getElementById('sieg');
  var cells = [];
  var puzzle = new Array(81).fill(0);
  var grid = new Array(81).fill(0);
  var given = new Array(81).fill(false);
  var selected = 0;
  var stufe = 'mittel';
  var token = 0;

  for (var i = 0; i < 81; i++) {
    var r = Math.floor(i / 9), c = i % 9;
    var el = document.createElement('div');
    el.className = 'feld';
    el.setAttribute('data-index', String(i));
    el.setAttribute('role', 'gridcell');
    el.setAttribute('tabindex', i === 0 ? '0' : '-1');
    if ((Math.floor(r / 3) + Math.floor(c / 3)) % 2 === 0) el.classList.add('block-a');
    else el.classList.add('block-b');
    if (c === 2 || c === 5) el.classList.add('steg-r');
    if (r === 2 || r === 5) el.classList.add('steg-u');
    brett.appendChild(el);
    cells.push(el);
  }

  function conflicts(g) {
    var bad = new Set();
    var groups = [];
    for (var k = 0; k < 9; k++) {
      var row = [], col = [], blk = [];
      for (var m = 0; m < 9; m++) {
        row.push(k * 9 + m);
        col.push(m * 9 + k);
        blk.push((Math.floor(k / 3) * 3 + Math.floor(m / 3)) * 9 + (k % 3) * 3 + (m % 3));
      }
      groups.push(row, col, blk);
    }
    groups.forEach(function (grp) {
      var seen = {};
      grp.forEach(function (idx) {
        var v = g[idx];
        if (!v) return;
        (seen[v] = seen[v] || []).push(idx);
      });
      Object.keys(seen).forEach(function (v) {
        if (seen[v].length > 1) seen[v].forEach(function (idx) { bad.add(idx); });
      });
    });
    return bad;
  }

  function render() {
    var bad = conflicts(grid);
    var sr = Math.floor(selected / 9), sc = selected % 9;
    var sb = Math.floor(sr / 3) * 3 + Math.floor(sc / 3);
    var sv = grid[selected];
    var full = true;
    for (var i = 0; i < 81; i++) {
      var el = cells[i], v = grid[i];
      if (!v) full = false;
      var r = Math.floor(i / 9), c = i % 9;
      var b = Math.floor(r / 3) * 3 + Math.floor(c / 3);
      el.textContent = v ? String(v) : '';
      el.classList.toggle('vorgabe', given[i]);
      el.classList.toggle('eigen', !given[i] && !!v);
      el.classList.toggle('konflikt', bad.has(i));
      el.classList.toggle('gewaehlt', i === selected);
      el.classList.toggle('bezug', i !== selected && (r === sr || c === sc || b === sb));
      el.classList.toggle('gleich', i !== selected && !!sv && v === sv);
      el.setAttribute('tabindex', i === selected ? '0' : '-1');
      el.setAttribute('aria-selected', i === selected ? 'true' : 'false');
      el.setAttribute('aria-invalid', bad.has(i) ? 'true' : 'false');
      el.setAttribute('aria-label', 'Zeile ' + (r + 1) + ', Spalte ' + (c + 1) + ', ' +
        (v ? v : 'leer') + (given[i] ? ', vorgegeben' : '') + (bad.has(i) ? ', Konflikt' : ''));
    }
    var won = full && bad.size === 0;
    document.body.classList.toggle('geloest', won);
    sieg.hidden = !won;
  }

  function select(i) {
    selected = Math.max(0, Math.min(80, i));
    render();
  }

  function setDigit(d) {
    if (given[selected]) return;
    grid[selected] = d;
    render();
  }

  function load(s) {
    var my = ++token;
    stufe = s;
    document.querySelectorAll('[data-stufe]').forEach(function (b) {
      var on = b.getAttribute('data-stufe') === s;
      b.classList.toggle('aktiv', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    meldung.textContent = 'Lade Rätsel …';
    fetch('api/neu?stufe=' + encodeURIComponent(s))
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        if (my !== token) return;
        puzzle = data.puzzle.slice();
        grid = data.puzzle.slice();
        given = puzzle.map(function (v) { return v !== 0; });
        meldung.textContent = '';
        selected = 0;
        render();
      })
      .catch(function () {
        if (my !== token) return;
        meldung.textContent = 'Rätsel konnte nicht geladen werden.';
      });
  }

  brett.addEventListener('click', function (e) {
    var t = e.target.closest('[data-index]');
    if (t) select(parseInt(t.getAttribute('data-index'), 10));
  });

  document.querySelectorAll('[data-digit]').forEach(function (b) {
    b.addEventListener('click', function () {
      setDigit(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  document.querySelectorAll('[data-stufe]').forEach(function (b) {
    b.addEventListener('click', function () { load(b.getAttribute('data-stufe')); });
  });

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (k >= '1' && k <= '9') { setDigit(parseInt(k, 10)); e.preventDefault(); }
    else if (k === 'Delete' || k === 'Backspace' || k === '0') { setDigit(0); e.preventDefault(); }
    else if (k === 'ArrowLeft') { if (selected % 9 > 0) select(selected - 1); e.preventDefault(); }
    else if (k === 'ArrowRight') { if (selected % 9 < 8) select(selected + 1); e.preventDefault(); }
    else if (k === 'ArrowUp') { if (selected >= 9) select(selected - 9); e.preventDefault(); }
    else if (k === 'ArrowDown') { if (selected < 72) select(selected + 9); e.preventDefault(); }
  });

  render();
  load('mittel');
})();
