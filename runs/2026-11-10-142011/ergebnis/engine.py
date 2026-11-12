"""engine.py - Sudoku-Generator und -Löser (nur Standardbibliothek)."""
import json
import random
import sys

CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}

_ROW = [i // 9 for i in range(81)]
_COL = [i % 9 for i in range(81)]
_BOX = [(i // 27) * 3 + (i % 9) // 3 for i in range(81)]
_PEERS = [
    [j for j in range(81)
     if j != i and (_ROW[j] == _ROW[i] or _COL[j] == _COL[i] or _BOX[j] == _BOX[i])]
    for i in range(81)
]


def conflicts(grid):
    """Indizes, die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren."""
    result = set()
    for i in range(81):
        v = grid[i]
        if v == 0:
            continue
        for j in _PEERS[i]:
            if grid[j] == v:
                result.add(i)
                break
    return result


def _search(puzzle, limit, randomize=False):
    """Sucht bis zu `limit` Lösungen (Bitmasken + MRV-Heuristik)."""
    if limit <= 0:
        return []
    grid = [int(v) for v in puzzle]
    if len(grid) != 81 or any(v < 0 or v > 9 for v in grid):
        return []
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empty = []
    for i, v in enumerate(grid):
        if v == 0:
            empty.append(i)
            continue
        bit = 1 << v
        if rows[_ROW[i]] & bit or cols[_COL[i]] & bit or boxes[_BOX[i]] & bit:
            return []
        rows[_ROW[i]] |= bit
        cols[_COL[i]] |= bit
        boxes[_BOX[i]] |= bit

    results = []

    def rec(empty):
        if not empty:
            results.append(grid[:])
            return len(results) >= limit
        best_k = -1
        best_n = 10
        best_m = 0
        for k, i in enumerate(empty):
            m = ~(rows[_ROW[i]] | cols[_COL[i]] | boxes[_BOX[i]]) & 0x3FE
            n = bin(m).count("1")
            if n < best_n:
                best_k, best_n, best_m = k, n, m
                if n <= 1:
                    break
        if best_n == 0:
            return False
        i = empty[best_k]
        rest = empty[:best_k] + empty[best_k + 1:]
        digits = [d for d in range(1, 10) if best_m & (1 << d)]
        if randomize:
            random.shuffle(digits)
        r, c, b = _ROW[i], _COL[i], _BOX[i]
        for d in digits:
            bit = 1 << d
            grid[i] = d
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            done = rec(rest)
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
            grid[i] = 0
            if done:
                return True
        return False

    rec(empty)
    return results


def solutions(puzzle, limit):
    """Liste mit höchstens `limit` Lösungen des Rätsels."""
    return _search(puzzle, limit)


def generate(level):
    if level not in CLUES:
        raise ValueError("Unbekannte Stufe: %r" % (level,))
    target = CLUES[level]
    while True:
        solution = _search([0] * 81, 1, randomize=True)[0]
        puzzle = solution[:]
        count = 81
        order = list(range(81))
        random.shuffle(order)
        for i in order:
            if count <= target:
                break
            saved = puzzle[i]
            puzzle[i] = 0
            if len(_search(puzzle, 2)) == 1:
                count -= 1
            else:
                puzzle[i] = saved
        if count == target:
            return {
                "puzzle": puzzle,
                "solution": solution,
                "clues": count,
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
