"""engine.py - Sudoku-Engine: Generierung, Lösung und Konflikterkennung (nur Standardbibliothek)."""

import json
import random
import sys
import time

CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}

_ROW = [i // 9 for i in range(81)]
_COL = [i % 9 for i in range(81)]
_BOX = [(i // 27) * 3 + (i % 9) // 3 for i in range(81)]
_PEERS = []
for _i in range(81):
    _PEERS.append([
        j for j in range(81)
        if j != _i and (_ROW[j] == _ROW[_i] or _COL[j] == _COL[_i] or _BOX[j] == _BOX[_i])
    ])


def conflicts(grid):
    """Set der Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren."""
    result = set()
    for i in range(81):
        v = grid[i]
        if v:
            for j in _PEERS[i]:
                if grid[j] == v:
                    result.add(i)
                    break
    return result


def _solve(puzzle, limit, rnd=None):
    if limit <= 0 or len(puzzle) != 81:
        return []
    g = [int(v) for v in puzzle]
    if any(v < 0 or v > 9 for v in g):
        return []
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for i, v in enumerate(g):
        if v:
            bit = 1 << (v - 1)
            if rows[_ROW[i]] & bit or cols[_COL[i]] & bit or boxes[_BOX[i]] & bit:
                return []
            rows[_ROW[i]] |= bit
            cols[_COL[i]] |= bit
            boxes[_BOX[i]] |= bit

    results = []

    def rec():
        best = -1
        best_mask = 0
        best_count = 10
        for i in range(81):
            if g[i] == 0:
                mask = ~(rows[_ROW[i]] | cols[_COL[i]] | boxes[_BOX[i]]) & 511
                c = bin(mask).count("1")
                if c < best_count:
                    best, best_mask, best_count = i, mask, c
                    if c <= 1:
                        break
        if best == -1:
            results.append(g[:])
            return
        if best_count == 0:
            return
        digits = [d for d in range(9) if best_mask >> d & 1]
        if rnd is not None:
            rnd.shuffle(digits)
        r, c_, b = _ROW[best], _COL[best], _BOX[best]
        for d in digits:
            bit = 1 << d
            g[best] = d + 1
            rows[r] |= bit
            cols[c_] |= bit
            boxes[b] |= bit
            rec()
            rows[r] &= ~bit
            cols[c_] &= ~bit
            boxes[b] &= ~bit
            g[best] = 0
            if len(results) >= limit:
                return

    rec()
    return results


def solutions(puzzle, limit):
    """Liste mit höchstens `limit` Lösungen des Rätsels."""
    return _solve(puzzle, limit)


def generate(level):
    """Erzeugt ein Rätsel mit eindeutiger Lösung und genau CLUES[level] Hinweisen."""
    if level not in CLUES:
        raise ValueError("Unbekannte Stufe: %r" % (level,))
    target = CLUES[level]
    rnd = random.Random()
    while True:
        solution = _solve([0] * 81, 1, rnd)[0]
        puzzle = solution[:]
        count = 81
        order = list(range(81))
        rnd.shuffle(order)
        for idx in order:
            if count <= target:
                break
            saved = puzzle[idx]
            puzzle[idx] = 0
            if len(_solve(puzzle, 2)) == 1:
                count -= 1
            else:
                puzzle[idx] = saved
        if count == target:
            return {
                "puzzle": puzzle,
                "solution": solution,
                "clues": target,
                "level": level,
            }


def main(argv):
    if len(argv) >= 3 and argv[1] == "neu":
        try:
            print(json.dumps(generate(argv[2])))
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 1
        return 0
    print("Aufruf: python engine.py neu <leicht|mittel|schwer>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
