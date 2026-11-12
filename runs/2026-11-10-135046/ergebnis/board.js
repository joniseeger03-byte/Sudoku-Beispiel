(function () {
  'use strict';

  var boardEl = document.getElementById('board');
  var zettelEl = document.getElementById('zettel');
  var meldungEl = document.getElementById('meldung');
  var timerEl = document.getElementById('timer');
  var timerBtn = document.getElementById('timer-schalter');
  var notizBtn = document.getElementById('notizen');
  var undoBtn = document.getElementById('undo');

  var cells = [];
  var given = new Array(81).fill(false);
  var values = new Array(81).fill(0);
  var notes = [];
  var selected = -1;
  var notesMode = false;
  var undoStack = [];
  var stufe = 'mittel';
  var loadToken = 0;
  var conflictMap = {};
  var seconds = 0;
  var timerOn = false;
  var solved = false;
  var ticker = null;

  function emptyNotes() {
    var a = [];
    for (var i = 0; i < 81; i++) a.push([]);
    return a;
  }
  notes = emptyNotes();

  // ---------- Brett aufbauen ----------
  for (var i = 0; i < 81; i++) {
    var c = document.createElement('div');
    c.setAttribute('data-index', String(i));
    c.setAttribute('role', 'gridcell');
    var r = Math.floor(i / 9), col = i % 9;
    c.className = 'zelle';
    if (col % 3 === 2 && col !== 8) c.className += ' blockrechts';
    if (r % 3 === 2 && r !== 8) c.className += ' blockunten';
    boardEl.appendChild(c);
    cells.push(c);
  }

  boardEl.addEventListener('click', function (e) {
    var el = e.target.closest('[data-index]');
    if (el) select(parseInt(el.getAttribute('data-index'), 10));
  });

  function select(i) {
    selected = i;
    render();
  }

  // ---------- Konflikte ----------
  function computeConflicts() {
    var map = {};
    function check(indices, label, nr) {
      var seen = {};
      indices.forEach(function (idx) {
        var v = values[idx];
        if (!v) return;
        (seen[v] = seen[v] || []).push(idx);
      });
      Object.keys(seen).forEach(function (v) {
        if (seen[v].length > 1) {
          seen[v].forEach(function (idx) {
            (map[idx] = map[idx] || []).push('Doppelte ' + v + ' in ' + label + ' ' + nr);
          });
        }
      });
    }
    for (var k = 0; k < 9; k++) {
      var row = [], colm = [], blk = [];
      for (var j = 0; j < 9; j++) {
        row.push(k * 9 + j);
        colm.push(j * 9 + k);
        blk.push((Math.floor(k / 3) * 3 + Math.floor(j / 3)) * 9 + (k % 3) * 3 + (j % 3));
      }
      check(row, 'Zeile', k + 1);
      check(colm, 'Spalte', k + 1);
      check(blk, 'Block', k + 1);
    }
    return map;
  }

  // ---------- Rendern ----------
  function render() {
    conflictMap = computeConflicts();
    var full = values.every(function (v) { return v > 0; });
    solved = full && Object.keys(conflictMap).length === 0;
    document.body.classList.toggle('geloest', solved);

    var sr = selected >= 0 ? Math.floor(selected / 9) : -1;
    var sc = selected >= 0 ? selected % 9 : -1;

    for (var i = 0; i < 81; i++) {
      var el = cells[i];
      var cls = el.className.split(' ').filter(function (n) {
        return n === 'zelle' || n === 'blockrechts' || n === 'blockunten';
      });
      if (given[i]) cls.push('vorgabe'); else if (values[i]) cls.push('eigen');
      if (i === selected) cls.push('selected');
      else if (selected >= 0) {
        var r = Math.floor(i / 9), c = i % 9;
        if (r === sr || c === sc ||
            (Math.floor(r / 3) === Math.floor(sr / 3) && Math.floor(c / 3) === Math.floor(sc / 3))) {
          cls.push('peer');
        }
      }
      if (conflictMap[i]) cls.push('konflikt');
      el.className = cls.join(' ');

      if (conflictMap[i]) el.title = conflictMap[i][0]; else el.removeAttribute('title');

      if (values[i]) {
        el.textContent = String(values[i]);
      } else if (notes[i].length) {
        el.textContent = '';
        var wrap = document.createElement('div');
        wrap.className = 'notizen';
        for (var d = 1; d <= 9; d++) {
          var s = document.createElement('span');
          s.textContent = notes[i].indexOf(d) >= 0 ? String(d) : '';
          wrap.appendChild(s);
        }
        el.appendChild(wrap);
      } else {
        el.textContent = '';
      }
    }

    // Zettel mit Fehlermeldung
    var msg = '';
    if (selected >= 0 && conflictMap[selected]) msg = conflictMap[selected].join(' · ');
    else {
      var keys = Object.keys(conflictMap);
      if (keys.length) msg = conflictMap[keys[0]][0];
    }
    zettelEl.textContent = msg;
    zettelEl.classList.toggle('sichtbar', !!msg);

    undoBtn.disabled = undoStack.length === 0;
    updateTimerDisplay();
  }

  // ---------- Eingabe ----------
  function snapshot() {
    undoStack.push({
      values: values.slice(),
      notes: notes.map(function (n) { return n.slice(); })
    });
    if (undoStack.length > 100) undoStack.shift();
  }

  function enter(d) {
    if (selected < 0 || given[selected]) return;
    if (d === 0) {
      if (!values[selected] && !notes[selected].length) return;
      snapshot();
      values[selected] = 0;
      notes[selected] = [];
    } else if (notesMode) {
      snapshot();
      if (values[selected]) values[selected] = 0;
      var p = notes[selected].indexOf(d);
      if (p >= 0) notes[selected].splice(p, 1); else notes[selected].push(d);
    } else {
      if (values[selected] === d && !notes[selected].length) return;
      snapshot();
      values[selected] = d;
      notes[selected] = [];
    }
    render();
  }

  function undo() {
    var s = undoStack.pop();
    if (!s) return;
    values = s.values;
    notes = s.notes;
    render();
  }

  document.addEventListener('keydown', function (e) {
    var k = e.key;
    if ((e.ctrlKey || e.metaKey) && (k === 'z' || k === 'Z')) {
      e.preventDefault();
      undo();
      return;
    }
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (/^[1-9]$/.test(k)) {
      e.preventDefault();
      enter(parseInt(k, 10));
    } else if (k === 'Delete' || k === 'Backspace') {
      e.preventDefault();
      enter(0);
    } else if (k.indexOf('Arrow') === 0) {
      e.preventDefault();
      if (selected < 0) { select(0); return; }
      var r = Math.floor(selected / 9), c = selected % 9;
      if (k === 'ArrowUp') r = Math.max(0, r - 1);
      else if (k === 'ArrowDown') r = Math.min(8, r + 1);
      else if (k === 'ArrowLeft') c = Math.max(0, c - 1);
      else if (k === 'ArrowRight') c = Math.min(8, c + 1);
      select(r * 9 + c);
    }
  });

  Array.prototype.forEach.call(document.querySelectorAll('[data-digit]'), function (b) {
    b.addEventListener('mousedown', function (e) { e.preventDefault(); });
    b.addEventListener('click', function () {
      enter(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  undoBtn.addEventListener('click', undo);

  notizBtn.addEventListener('click', function () {
    notesMode = !notesMode;
    notizBtn.setAttribute('aria-pressed', String(notesMode));
    notizBtn.textContent = 'Notizen: ' + (notesMode ? 'An' : 'Aus');
    notizBtn.classList.toggle('an', notesMode);
  });

  // ---------- Timer ----------
  function updateTimerDisplay() {
    var m = Math.floor(seconds / 60), s = seconds % 60;
    timerEl.textContent = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    timerEl.hidden = !timerOn;
  }
  timerBtn.addEventListener('click', function () {
    timerOn = !timerOn;
    timerBtn.setAttribute('aria-pressed', String(timerOn));
    timerBtn.classList.toggle('an', timerOn);
    updateTimerDisplay();
  });
  ticker = setInterval(function () {
    if (timerOn && !solved) {
      seconds++;
      updateTimerDisplay();
    }
  }, 1000);

  // ---------- Neues Rätsel ----------
  function neu(s) {
    stufe = s;
    var token = ++loadToken;
    Array.prototype.forEach.call(document.querySelectorAll('[data-stufe]'), function (b) {
      b.classList.toggle('aktiv', b.getAttribute('data-stufe') === s);
    });
    meldungEl.textContent = 'Lade Rätsel …';
    fetch('api/neu?stufe=' + stufe)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        if (token !== loadToken) return;
        var p = data.puzzle;
        given = p.map(function (v) { return v !== 0; });
        values = p.slice();
        notes = emptyNotes();
        undoStack = [];
        selected = -1;
        seconds = 0;
        meldungEl.textContent = '';
        render();
      })
      .catch(function () {
        if (token !== loadToken) return;
        meldungEl.textContent = 'Rätsel konnte nicht geladen werden.';
      });
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-stufe]'), function (b) {
    b.addEventListener('click', function () { neu(b.getAttribute('data-stufe')); });
  });

  render();
  neu('mittel');
})();
