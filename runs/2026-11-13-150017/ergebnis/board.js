(function () {
  'use strict';
  var brett = document.getElementById('brett');
  var meldung = document.getElementById('meldung');
  var status = document.getElementById('status');
  var notizBtn = document.getElementById('notizen');
  var cells = [];
  var puzzle = [], solution = [], values = [], notes = [];
  var selected = -1;
  var notesMode = false;
  var showWrong = false;
  var loadId = 0;

  for (var i = 0; i < 81; i++) {
    var c = document.createElement('div');
    c.className = 'feld';
    c.setAttribute('role', 'gridcell');
    c.dataset.index = i;
    var r = Math.floor(i / 9), col = i % 9;
    var blk = Math.floor(r / 3) * 3 + Math.floor(col / 3);
    if (blk % 2 === 1) c.classList.add('flach');
    if (col % 3 === 0 && col > 0) c.classList.add('links');
    if (r % 3 === 0 && r > 0) c.classList.add('oben');
    brett.appendChild(c);
    cells.push(c);
  }

  function peers(a, b) {
    var ra = Math.floor(a / 9), ca = a % 9, rb = Math.floor(b / 9), cb = b % 9;
    return ra === rb || ca === cb ||
      (Math.floor(ra / 3) === Math.floor(rb / 3) && Math.floor(ca / 3) === Math.floor(cb / 3));
  }

  function conflicts(g) {
    var s = {};
    for (var a = 0; a < 81; a++) {
      if (!g[a]) continue;
      for (var b = a + 1; b < 81; b++) {
        if (g[b] === g[a] && peers(a, b)) { s[a] = 1; s[b] = 1; }
      }
    }
    return s;
  }

  function candidates(idx) {
    var out = [];
    for (var d = 1; d <= 9; d++) {
      var ok = true;
      for (var j = 0; j < 81; j++) {
        if (j !== idx && values[j] === d && peers(idx, j)) { ok = false; break; }
      }
      if (ok) out.push(d);
    }
    return out;
  }

  function render() {
    var cf = conflicts(values);
    var full = values.length === 81 && values.every(function (v) { return v > 0; });
    var solved = full && Object.keys(cf).length === 0 &&
      values.every(function (v, k) { return v === solution[k]; });
    var selVal = selected >= 0 ? values[selected] : 0;
    for (var i = 0; i < 81; i++) {
      var el = cells[i], v = values[i] || 0;
      el.classList.toggle('vorgabe', puzzle[i] !== 0 && !!puzzle[i]);
      el.classList.toggle('eigen', !puzzle[i] && v > 0);
      el.classList.toggle('konflikt', !!cf[i]);
      el.classList.toggle('falsch', showWrong && !puzzle[i] && v > 0 && v !== solution[i]);
      el.classList.toggle('gewaehlt', i === selected);
      el.classList.toggle('nachbar', selected >= 0 && i !== selected && peers(selected, i));
      el.classList.toggle('gleich', selVal > 0 && v === selVal);
      if (v > 0) {
        if (el.textContent !== String(v) || el.firstElementChild) el.textContent = v;
      } else if (notes[i] && notes[i].length) {
        var h = '<span class="notiz">';
        for (var d = 1; d <= 9; d++) h += '<i>' + (notes[i].indexOf(d) >= 0 ? d : '') + '</i>';
        el.innerHTML = h + '</span>';
      } else {
        el.textContent = '';
      }
    }
    document.body.classList.toggle('geloest', solved);
    meldung.hidden = !solved;
    if (solved) status.textContent = 'Gelöst!';
  }

  function select(i) {
    selected = Math.max(0, Math.min(80, i));
    render();
  }

  function enter(d) {
    if (selected < 0 || document.body.classList.contains('geloest') || !values.length) return;
    if (puzzle[selected]) return;
    if (d === 0) {
      values[selected] = 0; notes[selected] = [];
    } else if (notesMode) {
      if (values[selected]) return;
      var n = notes[selected] || [];
      var p = n.indexOf(d);
      if (p >= 0) n.splice(p, 1); else n.push(d);
      notes[selected] = n;
    } else {
      values[selected] = d; notes[selected] = [];
    }
    render();
  }

  function setNotes(on) {
    notesMode = on;
    notizBtn.setAttribute('aria-pressed', on);
    notizBtn.classList.toggle('an', on);
    document.body.classList.toggle('notizmodus', on);
  }

  brett.addEventListener('click', function (e) {
    var t = e.target.closest('.feld');
    if (t) select(+t.dataset.index);
  });

  document.getElementById('ziffern').addEventListener('click', function (e) {
    var b = e.target.closest('button[data-digit]');
    if (b) enter(+b.dataset.digit);
  });

  document.querySelectorAll('button[data-stufe]').forEach(function (b) {
    b.addEventListener('click', function () { neu(b.dataset.stufe); });
  });

  notizBtn.addEventListener('click', function () { setNotes(!notesMode); });
  document.getElementById('fehler').addEventListener('click', function () {
    showWrong = !showWrong;
    var n = Object.keys(conflicts(values)).length;
    status.textContent = n ? n + ' Felder im Konflikt.' : 'Keine Konflikte.';
    render();
  });
  document.getElementById('moegliche').addEventListener('click', function () {
    if (selected < 0) { status.textContent = 'Erst ein Feld wählen.'; return; }
    if (values[selected]) { status.textContent = 'Feld ist bereits belegt.'; return; }
    var c = candidates(selected);
    status.textContent = 'Möglich: ' + (c.length ? c.join(' ') : 'keine');
  });

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (k >= '1' && k <= '9') { enter(+k); e.preventDefault(); }
    else if (k === 'Delete' || k === 'Backspace') { enter(0); e.preventDefault(); }
    else if (k === 'n' || k === 'N') { setNotes(!notesMode); }
    else if (k.indexOf('Arrow') === 0) {
      e.preventDefault();
      if (selected < 0) { select(0); return; }
      var r = Math.floor(selected / 9), c = selected % 9;
      if (k === 'ArrowUp') r = Math.max(0, r - 1);
      if (k === 'ArrowDown') r = Math.min(8, r + 1);
      if (k === 'ArrowLeft') c = Math.max(0, c - 1);
      if (k === 'ArrowRight') c = Math.min(8, c + 1);
      select(r * 9 + c);
    }
  });

  function neu(stufe) {
    var id = ++loadId;
    document.querySelectorAll('button[data-stufe]').forEach(function (b) {
      b.classList.toggle('aktiv', b.dataset.stufe === stufe);
    });
    status.textContent = 'Lade Rätsel …';
    fetch('api/neu?stufe=' + stufe)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        if (id !== loadId) return;
        puzzle = d.puzzle.slice();
        solution = d.solution.slice();
        values = d.puzzle.slice();
        notes = [];
        selected = -1;
        showWrong = false;
        document.body.classList.remove('geloest');
        status.textContent = 'Feld wählen und Ziffer setzen.';
        render();
      })
      .catch(function () {
        if (id === loadId) status.textContent = 'Rätsel konnte nicht geladen werden.';
      });
  }

  neu('mittel');
})();
