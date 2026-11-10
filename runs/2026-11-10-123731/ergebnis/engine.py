"""engine.py - Sudoku-Engine (nur Standardbibliothek)."""
import json
import random
import sys
import time

CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}

_FULL = 0x1FF


def _units():
    units = []
    for r in range(9):
        units.append([r * 9 + c for c in range(9)])
    for c in range(9):
        units.append([r * 9 + c for r in range(9)])
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            units.append([(br + i) * 9 + bc + j for i in range(3) for j in range(3)])
    return units


_UNITS = _units()


def conflicts(grid):
    """Menge der Indizes (0-80), die in Zeile, Spalte oder Block kollidieren."""
    result = set()
    for unit in _UNITS:
        seen = {}
        for i in unit:
            v = grid[i]
            if v:
                seen.setdefault(v, []).append(i)
        for idxs in seen.values():
            if len(idxs) > 1:
                result.update(idxs)
    return result


def _search(puzzle, limit, rng=None):
    if limit <= 0:
        return []
    grid = list(puzzle)
    if len(grid) != 81 or conflicts(grid):
        return []
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []
    for i, v in enumerate(grid):
        r, c = divmod(i, 9)
        b = (r // 3) * 3 + c // 3
        if v:
            bit = 1 << (v - 1)
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
        else:
            empties.append((i, r, c, b))
    found = []

    def solve(remaining):
        if len(found) >= limit:
            return
        best = None
        best_mask = 0
        best_count = 10
        for cell in remaining:
            _, r, c, b = cell
            mask = ~(rows[r] | cols[c] | boxes[b]) & _FULL
            cnt = bin(mask).count("1")
            if cnt == 0:
                return
            if cnt < best_count:
                best, best_mask, best_count = cell, mask, cnt
                if cnt == 1:
                    break
        if best is None:
            found.append(grid[:])
            return
        i, r, c, b = best
        rest = [x for x in remaining if x is not best]
        digits = [d for d in range(9) if best_mask >> d & 1]
        if rng is not None:
            rng.shuffle(digits)
        for d in digits:
            bit = 1 << d
            grid[i] = d + 1
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            solve(rest)
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
            grid[i] = 0
            if len(found) >= limit:
                return

    solve(empties)
    return found


def solutions(puzzle, limit):
    """Liste von maximal `limit` Lösungen (jeweils Liste mit 81 Zahlen)."""
    return _search(puzzle, limit)


def generate(level):
    if level not in CLUES:
        raise ValueError("Unbekannte Stufe: %r" % (level,))
    target = CLUES[level]
    rng = random.Random()
    deadline = time.time() + 4.0
    best = None
    while True:
        solution = _search([0] * 81, 1, rng)[0]
        puzzle = solution[:]
        order = list(range(81))
        rng.shuffle(order)
        count = 81
        for i in order:
            if count <= target:
                break
            old = puzzle[i]
            puzzle[i] = 0
            if len(_search(puzzle, 2)) == 1:
                count -= 1
            else:
                puzzle[i] = old
        if count == target:
            return {"puzzle": puzzle, "solution": solution,
                    "clues": target, "level": level}
        if time.time() > deadline and best is None:
            best = None  # weiter versuchen; Ziel muss exakt erreicht werden


def main(argv):
    if len(argv) == 3 and argv[1] == "neu" and argv[2] in CLUES:
        print(json.dumps(generate(argv[2])))
        return 0
    sys.stderr.write("Aufruf: python engine.py neu <leicht|mittel|schwer>\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
