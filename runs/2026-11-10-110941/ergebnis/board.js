(function () {
  'use strict';

  var brettEl = document.getElementById('brett');
  var statusEl = document.getElementById('status');
  var hinweisBtn = document.getElementById('hinweis');
  var notizBtn = document.getElementById('notizen');
  var stufenBtns = document.querySelectorAll('[data-stufe]');

  var zellen = [];
  var puzzle = new Array(81).fill(0);
  var loesung = new Array(81).fill(0);
  var werte = new Array(81).fill(0);
  var notizen = [];
  var hinweise = new Set();
  var hinweiseUebrig = 3;
  var notizModus = false;
  var gewaehlt = -1;
  var gerade = false;
  var aktuelleStufe = 'mittel';
  var anfrage = 0;

  function zeile(i) { return Math.floor(i / 9); }
  function spalte(i) { return i % 9; }
  function block(i) { return Math.floor(zeile(i) / 3) * 3 + Math.floor(spalte(i) / 3); }
  function verwandt(a, b) {
    return zeile(a) === zeile(b) || spalte(a) === spalte(b) || block(a) === block(b);
  }

  function bauen() {
    for (var i = 0; i < 81; i++) {
      var z = document.createElement('div');
      z.className = 'feld';
      z.setAttribute('data-index', String(i));
      z.setAttribute('role', 'gridcell');
      if ((Math.floor(zeile(i) / 3) + Math.floor(spalte(i) / 3)) % 2 === 1) z.classList.add('tief');
      if (spalte(i) % 3 === 2 && spalte(i) < 8) z.classList.add('rechts3');
      if (zeile(i) % 3 === 2 && zeile(i) < 8) z.classList.add('unten3');
      brettEl.appendChild(z);
      zellen.push(z);
      notizen.push(new Set());
    }
    brettEl.addEventListener('click', function (e) {
      var t = e.target.closest('[data-index]');
      if (t) { gewaehlt = parseInt(t.getAttribute('data-index'), 10); render(); }
    });
  }

  function konflikte() {
    var menge = new Set();
    for (var u = 0; u < 9; u++) {
      var einheiten = [{}, {}, {}];
      for (var k = 0; k < 9; k++) {
        var idx = [u * 9 + k, k * 9 + u,
          (Math.floor(u / 3) * 3 + Math.floor(k / 3)) * 9 + (u % 3) * 3 + (k % 3)];
        for (var m = 0; m < 3; m++) {
          var v = werte[idx[m]];
          if (!v) continue;
          (einheiten[m][v] = einheiten[m][v] || []).push(idx[m]);
        }
      }
      einheiten.forEach(function (e) {
        Object.keys(e).forEach(function (v) {
          if (e[v].length > 1) e[v].forEach(function (i) { menge.add(i); });
        });
      });
    }
    return menge;
  }

  function bearbeitbar(i) { return puzzle[i] === 0 && !hinweise.has(i); }

  function render() {
    var k = konflikte();
    var voll = werte.every(function (v) { return v !== 0; });
    gerade = voll && k.size === 0;
    document.body.classList.toggle('geloest', gerade);

    for (var i = 0; i < 81; i++) {
      var z = zellen[i];
      var v = werte[i];
      z.textContent = '';
      if (v) {
        z.textContent = String(v);
      } else if (notizen[i].size) {
        var n = document.createElement('span');
        n.className = 'notizen';
        for (var d = 1; d <= 9; d++) {
          var s = document.createElement('span');
          s.textContent = notizen[i].has(d) ? String(d) : '';
          n.appendChild(s);
        }
        z.appendChild(n);
      }
      z.classList.toggle('vorgabe', puzzle[i] !== 0);
      z.classList.toggle('eigene', puzzle[i] === 0 && v !== 0);
      z.classList.toggle('hinweis', hinweise.has(i));
      z.classList.toggle('konflikt', k.has(i) && puzzle[i] === 0);
      z.classList.toggle('gewaehlt', i === gewaehlt);
      z.classList.toggle('mit', gewaehlt >= 0 && i !== gewaehlt && verwandt(i, gewaehlt));
    }
    hinweisBtn.textContent = 'Hinweis (' + hinweiseUebrig + ')';
    hinweisBtn.disabled = hinweiseUebrig <= 0 || gerade;
    notizBtn.textContent = 'Notizen: ' + (notizModus ? 'an' : 'aus');
    notizBtn.setAttribute('aria-pressed', notizModus ? 'true' : 'false');
    notizBtn.classList.toggle('aktiv', notizModus);
  }

  function eingabe(d) {
    if (gewaehlt < 0 || gerade || !bearbeitbar(gewaehlt)) return;
    var i = gewaehlt;
    if (d === 0) {
      if (werte[i] !== 0) {
        werte[i] = 0;
      } else if (notizen[i].size) {
        var letzte = Array.from(notizen[i]).pop();
        notizen[i].delete(letzte);
      }
    } else if (notizModus) {
      if (werte[i] !== 0) return;
      if (notizen[i].has(d)) notizen[i].delete(d); else notizen[i].add(d);
    } else {
      werte[i] = d;
      notizen[i].clear();
      for (var j = 0; j < 81; j++) {
        if (j !== i && verwandt(i, j)) notizen[j].delete(d);
      }
    }
    render();
  }

  function hinweisGeben() {
    if (hinweiseUebrig <= 0 || gerade) return;
    var ziel = -1;
    if (gewaehlt >= 0 && bearbeitbar(gewaehlt) && werte[gewaehlt] !== loesung[gewaehlt]) {
      ziel = gewaehlt;
    } else {
      var kandidaten = [];
      for (var i = 0; i < 81; i++) {
        if (bearbeitbar(i) && werte[i] !== loesung[i]) kandidaten.push(i);
      }
      if (!kandidaten.length) return;
      ziel = kandidaten[Math.floor(Math.random() * kandidaten.length)];
    }
    werte[ziel] = loesung[ziel];
    notizen[ziel].clear();
    hinweise.add(ziel);
    hinweiseUebrig--;
    gewaehlt = ziel;
    render();
  }

  function neu(stufe) {
    aktuelleStufe = stufe;
    stufenBtns.forEach(function (b) {
      b.classList.toggle('aktiv', b.getAttribute('data-stufe') === stufe);
    });
    var mein = ++anfrage;
    statusEl.textContent = 'Lotung läuft …';
    fetch('api/neu?stufe=' + stufe)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (daten) {
        if (mein !== anfrage) return;
        if (!daten || !daten.puzzle || daten.puzzle.length !== 81) throw new Error('Ungültige Daten');
        puzzle = daten.puzzle.slice();
        loesung = (daten.solution || []).slice();
        werte = puzzle.slice();
        notizen.forEach(function (n) { n.clear(); });
        hinweise = new Set();
        hinweiseUebrig = 3;
        gewaehlt = -1;
        statusEl.textContent = '';
        render();
      })
      .catch(function () {
        if (mein !== anfrage) return;
        statusEl.textContent = 'Rätsel konnte nicht geladen werden. Bitte Stufe erneut wählen.';
      });
  }

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var k = e.key;
    if (k >= '1' && k <= '9' && k.length === 1) {
      eingabe(parseInt(k, 10));
      e.preventDefault();
    } else if (k === 'Delete' || k === 'Backspace') {
      eingabe(0);
      e.preventDefault();
    } else if (k.indexOf('Arrow') === 0) {
      e.preventDefault();
      if (gewaehlt < 0) { gewaehlt = 0; render(); return; }
      var z = zeile(gewaehlt), s = spalte(gewaehlt);
      if (k === 'ArrowUp') z = Math.max(0, z - 1);
      else if (k === 'ArrowDown') z = Math.min(8, z + 1);
      else if (k === 'ArrowLeft') s = Math.max(0, s - 1);
      else if (k === 'ArrowRight') s = Math.min(8, s + 1);
      gewaehlt = z * 9 + s;
      render();
    }
  });

  document.querySelectorAll('[data-digit]').forEach(function (b) {
    b.addEventListener('click', function () {
      eingabe(parseInt(b.getAttribute('data-digit'), 10));
    });
  });
  stufenBtns.forEach(function (b) {
    b.addEventListener('click', function () { neu(b.getAttribute('data-stufe')); });
  });
  hinweisBtn.addEventListener('click', hinweisGeben);
  notizBtn.addEventListener('click', function () { notizModus = !notizModus; render(); });

  bauen();
  render();
  neu(aktuelleStufe);
})();
