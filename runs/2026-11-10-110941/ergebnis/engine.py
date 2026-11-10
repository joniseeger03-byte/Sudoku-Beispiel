"""engine.py - Sudoku-Engine (nur Python-Standardbibliothek)."""

import json
import random
import sys

CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}

_ALL = 0x3FE  # Bits 1..9


def _box(i):
    return (i // 27) * 3 + (i % 9) // 3


def _solve(puzzle, limit, rng=None):
    """Backtracking mit MRV; liefert höchstens `limit` Lösungen."""
    if limit <= 0 or len(puzzle) != 81:
        return []
    grid = list(puzzle)
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for i, v in enumerate(grid):
        if v:
            if not isinstance(v, int) or v < 0 or v > 9:
                return []
            bit = 1 << v
            r, c, b = i // 9, i % 9, _box(i)
            if (rows[r] | cols[c] | boxes[b]) & bit:
                return []
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

    res = []

    def rec():
        best = -1
        best_m = 0
        best_c = 10
        for i in range(81):
            if grid[i] == 0:
                m = ~(rows[i // 9] | cols[i % 9] | boxes[_box(i)]) & _ALL
                cnt = bin(m).count("1")
                if cnt == 0:
                    return
                if cnt < best_c:
                    best, best_m, best_c = i, m, cnt
                    if cnt == 1:
                        break
        if best == -1:
            res.append(grid[:])
            return
        digits = [d for d in range(1, 10) if best_m & (1 << d)]
        if rng is not None:
            rng.shuffle(digits)
        r, c, b = best // 9, best % 9, _box(best)
        for d in digits:
            bit = 1 << d
            grid[best] = d
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            rec()
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
            grid[best] = 0
            if len(res) >= limit:
                return

    rec()
    return res


def solutions(puzzle, limit):
    """Liste mit höchstens `limit` Lösungen (je 81 Zahlen)."""
    return _solve(puzzle, limit)


def conflicts(grid):
    """Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren."""
    result = set()
    groups = {}
    for i, v in enumerate(grid):
        if v:
            for key in (("r", i // 9), ("c", i % 9), ("b", _box(i))):
                groups.setdefault(key + (v,), []).append(i)
    for idxs in groups.values():
        if len(idxs) > 1:
            result.update(idxs)
    return result


def generate(level):
    """Erzeugt ein Rätsel mit eindeutiger Lösung und genau CLUES[level] Hinweisen."""
    if level not in CLUES:
        raise ValueError("Unbekannte Stufe: %r" % (level,))
    target = CLUES[level]
    rng = random.Random()
    while True:
        solution = _solve([0] * 81, 1, rng)[0]
        for _ in range(8):
            puzzle = solution[:]
            count = 81
            order = list(range(81))
            rng.shuffle(order)
            for i in order:
                if count == target:
                    break
                old = puzzle[i]
                puzzle[i] = 0
                if len(_solve(puzzle, 2)) == 1:
                    count -= 1
                else:
                    puzzle[i] = old
            if count == target:
                return {
                    "puzzle": puzzle,
                    "solution": solution,
                    "clues": target,
                    "level": level,
                }


def main(argv):
    if len(argv) == 3 and argv[1] == "neu" and argv[2] in CLUES:
        print(json.dumps(generate(argv[2])))
        return 0
    sys.stderr.write("Aufruf: python engine.py neu <leicht|mittel|schwer>\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
