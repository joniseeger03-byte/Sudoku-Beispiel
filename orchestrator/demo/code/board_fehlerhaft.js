const board = document.getElementById('board'), pad = document.getElementById('pad'), status = document.getElementById('status');
let game, grid, sel = 0;
for (let i = 0; i < 81; i++) {
  const b = document.createElement('button');
  b.dataset.index = i;
  b.onclick = () => { sel = i; draw(); };
  board.append(b);
}
for (let d = 0; d <= 9; d++) {
  const b = document.createElement('button');
  b.textContent = d || '⌫';
  b.dataset.digit = d;
  b.onclick = () => put(d);
  pad.append(b);
}
function put(d) {
  if (grid[sel] === undefined) grid[sel] = d;
  draw();
  status.textContent = grid.join() === game.solution.join() ? 'Gelöst!' : '';
}
function conflicts(g) {
  const bad = new Set();
  for (let i = 0; i < 81; i++) for (let j = 0; j < 81; j++) {
    const same = Math.floor(i / 9) === Math.floor(j / 9) || i % 9 === j % 9 || (Math.floor(i / 27) === Math.floor(j / 27) && Math.floor(i % 9 / 3) === Math.floor(j % 9 / 3));
    if (i !== j && g[i] && g[i] === g[j] && same) bad.add(i);
  }
  return bad;
}
function draw() {
  const bad = conflicts(grid);
  [...board.children].forEach((b, i) => {
    b.textContent = grid[i] || '';
    b.className = [game.puzzle[i] ? 'given' : '', i === sel ? 'sel' : '', bad.has(i) ? 'konflikt' : ''].join(' ');
  });
}
async function start() {
  status.textContent = 'Python erzeugt ein Rätsel …';
  const r = await fetch('api/neu?stufe=' + document.getElementById('level').value);
  game = await r.json();
  grid = game.puzzle.slice();
  sel = grid.indexOf(0);
  status.textContent = '';
  draw();
}
document.addEventListener('keydown', e => {
  if (/^[1-9]$/.test(e.key)) put(+e.key);
  if (e.key === 'Backspace' || e.key === 'Delete') put(0);
  const m = { ArrowUp: -9, ArrowDown: 9, ArrowLeft: -1, ArrowRight: 1 }[e.key];
  if (m) { e.preventDefault(); sel = (sel + m + 81) % 81; draw(); }
});
document.getElementById('new').onclick = start;
start();
