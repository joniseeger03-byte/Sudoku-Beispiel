(function () {
  'use strict';

  var brett = document.getElementById('brett');
  var meldung = document.getElementById('meldung');
  var cells = [];
  var values = new Array(81).fill(0);
  var given = new Array(81).fill(false);
  var selected = -1;
  var solved = false;
  var ladeNr = 0;
  var stufe = 'mittel';

  // Brett aufbauen
  for (var i = 0; i < 81; i++) {
    var el = document.createElement('div');
    var r = Math.floor(i / 9), c = i % 9;
    el.className = 'feld';
    if (c % 3 === 2 && c < 8) el.className += ' blockrechts';
    if (r % 3 === 2 && r < 8) el.className += ' blockunten';
    el.setAttribute('data-index', String(i));
    el.setAttribute('role', 'gridcell');
    brett.appendChild(el);
    cells.push(el);
  }

  brett.addEventListener('click', function (e) {
    var t = e.target.closest('[data-index]');
    if (!t) return;
    select(parseInt(t.getAttribute('data-index'), 10));
  });

  function peers(a, b) {
    var ra = Math.floor(a / 9), ca = a % 9, rb = Math.floor(b / 9), cb = b % 9;
    return ra === rb || ca === cb ||
      (Math.floor(ra / 3) === Math.floor(rb / 3) && Math.floor(ca / 3) === Math.floor(cb / 3));
  }

  function findConflicts() {
    var set = {};
    for (var a = 0; a < 81; a++) {
      if (!values[a]) continue;
      for (var b = a + 1; b < 81; b++) {
        if (values[b] === values[a] && peers(a, b)) {
          set[a] = true;
          set[b] = true;
        }
      }
    }
    return set;
  }

  function render() {
    var conf = findConflicts();
    var full = true, anyConf = false;
    for (var i = 0; i < 81; i++) {
      var el = cells[i];
      el.textContent = values[i] ? String(values[i]) : '';
      if (!values[i]) full = false;
      var cls = ['feld'];
      if (el.classList.contains('blockrechts')) cls.push('blockrechts');
      if (el.classList.contains('blockunten')) cls.push('blockunten');
      cls.push(given[i] ? 'vorgabe' : 'eigen');
      if (selected >= 0 && i !== selected && peers(i, selected)) cls.push('bezug');
      if (conf[i]) { cls.push('konflikt'); anyConf = true; }
      if (i === selected) cls.push('selected');
      el.className = cls.join(' ');
    }
    solved = full && !anyConf;
    document.body.classList.toggle('geloest', solved);
    meldung.textContent = solved ? 'Geschafft – das Rätsel ist gelöst.' : '';
  }

  function select(i) {
    selected = i;
    render();
  }

  function setDigit(d) {
    if (selected < 0 || given[selected] || solved) return;
    values[selected] = d;
    render();
  }

  function move(dr, dc) {
    if (selected < 0) { select(0); return; }
    var r = Math.floor(selected / 9) + dr, c = (selected % 9) + dc;
    if (r < 0 || r > 8 || c < 0 || c > 8) return;
    select(r * 9 + c);
  }

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (k >= '1' && k <= '9') { setDigit(parseInt(k, 10)); e.preventDefault(); }
    else if (k === 'Delete' || k === 'Backspace' || k === 'Del' || k === '0') { setDigit(0); e.preventDefault(); }
    else if (k === 'ArrowUp') { move(-1, 0); e.preventDefault(); }
    else if (k === 'ArrowDown') { move(1, 0); e.preventDefault(); }
    else if (k === 'ArrowLeft') { move(0, -1); e.preventDefault(); }
    else if (k === 'ArrowRight') { move(0, 1); e.preventDefault(); }
  });

  // Ziffernfeld
  var pad = document.querySelectorAll('[data-digit]');
  Array.prototype.forEach.call(pad, function (b) {
    b.addEventListener('mousedown', function (e) { e.preventDefault(); });
    b.addEventListener('click', function () {
      setDigit(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  // Stufen
  var stufenBtns = document.querySelectorAll('[data-stufe]');
  Array.prototype.forEach.call(stufenBtns, function (b) {
    b.addEventListener('click', function () {
      neu(b.getAttribute('data-stufe'));
    });
  });

  function markStufe() {
    Array.prototype.forEach.call(stufenBtns, function (b) {
      b.classList.toggle('aktiv', b.getAttribute('data-stufe') === stufe);
    });
  }

  function neu(s) {
    stufe = s;
    markStufe();
    var nr = ++ladeNr;
    fetch('api/neu?stufe=' + encodeURIComponent(s))
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        if (nr !== ladeNr) return;
        for (var i = 0; i < 81; i++) {
          values[i] = data.puzzle[i] || 0;
          given[i] = values[i] !== 0;
        }
        selected = -1;
        render();
      })
      .catch(function () {
        if (nr !== ladeNr) return;
        meldung.textContent = 'Rätsel konnte nicht geladen werden.';
      });
  }

  neu(stufe);
})();
