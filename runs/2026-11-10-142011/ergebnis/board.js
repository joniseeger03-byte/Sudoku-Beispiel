(function () {
  'use strict';

  var KEY = 'sudoku-herbarium-v1';
  var brett = document.getElementById('brett');
  var cells = [];
  var state = {
    stufe: 'mittel',
    puzzle: [],
    solution: [],
    grid: [],
    selected: -1,
    hints: 3,
    shown: false
  };

  function el(id) { return document.getElementById(id); }

  // ---------- Aufbau ----------
  for (var i = 0; i < 81; i++) {
    var c = document.createElement('div');
    var r = Math.floor(i / 9), col = i % 9;
    c.className = 'feld';
    if (col % 3 === 2 && col !== 8) c.className += ' br';
    if (r % 3 === 2 && r !== 8) c.className += ' bb';
    c.setAttribute('data-index', String(i));
    c.setAttribute('role', 'gridcell');
    c.setAttribute('tabindex', '0');
    c.setAttribute('aria-label', 'Zeile ' + (r + 1) + ', Spalte ' + (col + 1));
    brett.appendChild(c);
    cells.push(c);
  }

  // ---------- Konflikte ----------
  function conflicts(grid) {
    var out = new Set();
    var groups = [], k, j;
    for (k = 0; k < 9; k++) {
      var row = [], colm = [], blk = [];
      for (j = 0; j < 9; j++) {
        row.push(k * 9 + j);
        colm.push(j * 9 + k);
        blk.push((Math.floor(k / 3) * 3 + Math.floor(j / 3)) * 9 + (k % 3) * 3 + (j % 3));
      }
      groups.push(row, colm, blk);
    }
    groups.forEach(function (g) {
      var seen = {};
      g.forEach(function (idx) {
        var v = grid[idx];
        if (!v) return;
        (seen[v] = seen[v] || []).push(idx);
      });
      Object.keys(seen).forEach(function (v) {
        if (seen[v].length > 1) seen[v].forEach(function (x) { out.add(x); });
      });
    });
    return out;
  }

  // ---------- Darstellung ----------
  function render() {
    var conf = conflicts(state.grid);
    var sel = state.selected;
    var sr = sel >= 0 ? Math.floor(sel / 9) : -1;
    var sc = sel >= 0 ? sel % 9 : -1;
    for (var i = 0; i < 81; i++) {
      var c = cells[i];
      var v = state.grid[i];
      var r = Math.floor(i / 9), col = i % 9;
      c.textContent = v ? String(v) : '';
      var cls = 'feld';
      if (col % 3 === 2 && col !== 8) cls += ' br';
      if (r % 3 === 2 && r !== 8) cls += ' bb';
      if (state.puzzle[i]) cls += ' vorgegeben';
      if (conf.has(i)) cls += ' konflikt';
      if (i === sel) cls += ' selected';
      else if (sel >= 0 && (r === sr || col === sc ||
        (Math.floor(r / 3) === Math.floor(sr / 3) && Math.floor(col / 3) === Math.floor(sc / 3)))) {
        cls += ' bezug';
      }
      c.className = cls;
      c.setAttribute('aria-selected', i === sel ? 'true' : 'false');
    }
    var full = state.grid.length === 81 && state.grid.every(function (x) { return x > 0; });
    var solved = state.shown || (full && conf.size === 0);
    document.body.classList.toggle('geloest', solved);
    el('meldung').textContent = solved ? 'Bestimmt – richtig gelöst!' : '';
    el('hinweisrest').textContent = String(state.hints);
    el('stufenname').textContent = state.stufe;
    Array.prototype.forEach.call(document.querySelectorAll('[data-stufe]'), function (b) {
      var on = b.getAttribute('data-stufe') === state.stufe;
      b.classList.toggle('aktiv', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* ignorieren */ }
  }

  function toast(msg) {
    var t = el('toast');
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(toast.h);
    toast.h = setTimeout(function () { t.hidden = true; }, 2500);
  }

  // ---------- Aktionen ----------
  function select(i) {
    if (i < 0 || i > 80) return;
    state.selected = i;
    render();
    save();
  }

  function setDigit(d) {
    var i = state.selected;
    if (i < 0 || state.puzzle[i] || state.shown) return;
    state.grid[i] = d;
    render();
    save();
  }

  function applyPuzzle(data, stufe) {
    state.stufe = stufe;
    state.puzzle = data.puzzle.slice();
    state.solution = (data.solution || []).slice();
    state.grid = data.puzzle.slice();
    state.hints = 3;
    state.shown = false;
    var first = state.puzzle.indexOf(0);
    state.selected = first >= 0 ? first : 0;
    render();
    save();
  }

  function neu(stufe) {
    fetch('api/neu?stufe=' + stufe)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        if (!data || !data.puzzle || data.puzzle.length !== 81) throw new Error('Ungültige Daten');
        applyPuzzle(data, stufe);
      })
      .catch(function () { toast('Rätsel konnte nicht geladen werden.'); });
  }

  function hint() {
    if (state.shown) return;
    if (state.hints <= 0) { toast('Keine Hinweise mehr übrig.'); return; }
    var empty = [];
    for (var i = 0; i < 81; i++) if (!state.grid[i]) empty.push(i);
    if (!empty.length || !state.solution.length) return;
    var pick = empty[Math.floor(Math.random() * empty.length)];
    state.grid[pick] = state.solution[pick];
    state.hints--;
    state.selected = pick;
    render();
    save();
  }

  function showSolution() {
    if (!state.solution.length) return;
    state.grid = state.solution.slice();
    state.shown = true;
    el('modal').hidden = true;
    render();
    save();
  }

  // ---------- Ereignisse ----------
  brett.addEventListener('click', function (e) {
    var t = e.target.closest('[data-index]');
    if (t) select(parseInt(t.getAttribute('data-index'), 10));
  });
  brett.addEventListener('focusin', function (e) {
    var t = e.target.closest && e.target.closest('[data-index]');
    if (t && state.selected !== parseInt(t.getAttribute('data-index'), 10)) {
      select(parseInt(t.getAttribute('data-index'), 10));
    }
  });

  Array.prototype.forEach.call(document.querySelectorAll('[data-digit]'), function (b) {
    b.addEventListener('click', function () {
      setDigit(parseInt(b.getAttribute('data-digit'), 10));
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll('[data-stufe]'), function (b) {
    b.addEventListener('click', function () { neu(b.getAttribute('data-stufe')); });
  });
  document.querySelector('[data-hint]').addEventListener('click', hint);
  document.querySelector('[data-show-solution]').addEventListener('click', function () {
    el('modal').hidden = false;
    el('modal-nein').focus();
  });
  el('modal-nein').addEventListener('click', function () { el('modal').hidden = true; });
  el('modal-ja').addEventListener('click', showSolution);

  document.addEventListener('keydown', function (e) {
    if (!el('modal').hidden) {
      if (e.key === 'Escape') el('modal').hidden = true;
      return;
    }
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key, i = state.selected;
    if (k >= '1' && k <= '9' && k.length === 1) {
      e.preventDefault();
      setDigit(parseInt(k, 10));
    } else if (k === 'Backspace' || k === 'Delete') {
      e.preventDefault();
      setDigit(0);
    } else if (k.indexOf('Arrow') === 0) {
      e.preventDefault();
      if (i < 0) i = 0;
      var r = Math.floor(i / 9), c = i % 9;
      if (k === 'ArrowUp') r = Math.max(0, r - 1);
      if (k === 'ArrowDown') r = Math.min(8, r + 1);
      if (k === 'ArrowLeft') c = Math.max(0, c - 1);
      if (k === 'ArrowRight') c = Math.min(8, c + 1);
      select(r * 9 + c);
    } else if (k.length === 1 && /\S/.test(k) && !/^[a-z]$/i.test(k) === false) {
      toast('Nur die Ziffern 1–9 sind erlaubt.');
    }
  });

  // ---------- Start ----------
  var restored = false;
  try {
    var raw = localStorage.getItem(KEY);
    if (raw) {
      var s = JSON.parse(raw);
      if (s && s.puzzle && s.puzzle.length === 81 && s.grid && s.grid.length === 81) {
        state = {
          stufe: s.stufe || 'mittel',
          puzzle: s.puzzle,
          solution: s.solution || [],
          grid: s.grid,
          selected: typeof s.selected === 'number' ? s.selected : 0,
          hints: typeof s.hints === 'number' ? s.hints : 3,
          shown: !!s.shown
        };
        restored = true;
        render();
      }
    }
  } catch (e) { restored = false; }
  if (!restored) neu('mittel');
})();
