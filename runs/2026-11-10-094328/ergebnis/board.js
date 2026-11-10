(function () {
  'use strict';

  var brett = document.getElementById('brett');
  var statusEl = document.getElementById('status');
  var cells = [];
  var grid = new Array(81).fill(0);
  var given = new Array(81).fill(false);
  var selected = -1;
  var stufe = 'mittel';
  var anfrage = 0;

  // Brett aufbauen
  for (var i = 0; i < 81; i++) {
    var d = document.createElement('div');
    d.className = 'zelle';
    d.setAttribute('data-index', i);
    var r = Math.floor(i / 9), c = i % 9;
    if (c % 3 === 2 && c < 8) d.classList.add('blockrechts');
    if (r % 3 === 2 && r < 8) d.classList.add('blockunten');
    brett.appendChild(d);
    cells.push(d);
  }

  brett.addEventListener('click', function (e) {
    var el = e.target.closest('.zelle');
    if (el) select(parseInt(el.getAttribute('data-index'), 10));
  });

  function konflikte(g) {
    var bad = new Set();
    var groups = [];
    for (var k = 0; k < 9; k++) {
      var row = [], col = [], blk = [];
      for (var j = 0; j < 9; j++) {
        row.push(k * 9 + j);
        col.push(j * 9 + k);
        blk.push((Math.floor(k / 3) * 3 + Math.floor(j / 3)) * 9 + (k % 3) * 3 + (j % 3));
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
        if (seen[v].length > 1) seen[v].forEach(function (x) { bad.add(x); });
      });
    });
    return bad;
  }

  function select(i) {
    selected = i;
    render();
  }

  function render() {
    var bad = konflikte(grid);
    var sr = selected >= 0 ? Math.floor(selected / 9) : -1;
    var sc = selected >= 0 ? selected % 9 : -1;
    var full = true;
    for (var i = 0; i < 81; i++) {
      var el = cells[i];
      var r = Math.floor(i / 9), c = i % 9;
      el.textContent = grid[i] ? String(grid[i]) : '';
      if (!grid[i]) full = false;
      var peer = selected >= 0 && i !== selected && (
        r === sr || c === sc ||
        (Math.floor(r / 3) === Math.floor(sr / 3) && Math.floor(c / 3) === Math.floor(sc / 3)));
      el.classList.toggle('vorgabe', given[i]);
      el.classList.toggle('eigene', !given[i] && !!grid[i]);
      el.classList.toggle('selected', i === selected);
      el.classList.toggle('peer', peer);
      el.classList.toggle('konflikt', bad.has(i));
    }
    var solved = full && bad.size === 0;
    document.body.classList.toggle('geloest', solved);
    statusEl.textContent = solved ? 'ANGEKOMMEN' : '\u00a0';
  }

  function setDigit(v) {
    if (selected < 0 || given[selected]) return;
    grid[selected] = v;
    render();
  }

  function move(dr, dc) {
    if (selected < 0) { select(0); return; }
    var r = Math.max(0, Math.min(8, Math.floor(selected / 9) + dr));
    var c = Math.max(0, Math.min(8, selected % 9 + dc));
    select(r * 9 + c);
  }

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (k >= '1' && k <= '9') { setDigit(parseInt(k, 10)); e.preventDefault(); }
    else if (k === 'Delete' || k === 'Backspace' || k === 'Del') { setDigit(0); e.preventDefault(); }
    else if (k === 'ArrowUp') { move(-1, 0); e.preventDefault(); }
    else if (k === 'ArrowDown') { move(1, 0); e.preventDefault(); }
    else if (k === 'ArrowLeft') { move(0, -1); e.preventDefault(); }
    else if (k === 'ArrowRight') { move(0, 1); e.preventDefault(); }
  });

  document.querySelectorAll('[data-digit]').forEach(function (b) {
    b.addEventListener('click', function () {
      setDigit(parseInt(b.getAttribute('data-digit'), 10));
    });
  });

  document.querySelectorAll('[data-stufe]').forEach(function (b) {
    b.addEventListener('click', function () {
      neu(b.getAttribute('data-stufe'));
    });
  });

  function markiereStufe() {
    document.querySelectorAll('[data-stufe]').forEach(function (b) {
      var on = b.getAttribute('data-stufe') === stufe;
      b.classList.toggle('aktiv', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  function neu(s) {
    stufe = s;
    markiereStufe();
    var mein = ++anfrage;
    fetch('api/neu?stufe=' + stufe)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (data) {
        if (mein !== anfrage) return;
        grid = data.puzzle.slice();
        given = grid.map(function (v) { return v !== 0; });
        var first = grid.indexOf(0);
        selected = first >= 0 ? first : 0;
        render();
      })
      .catch(function () {
        if (mein !== anfrage) return;
        statusEl.textContent = 'STÖRUNG';
      });
  }

  markiereStufe();
  neu(stufe);
})();
