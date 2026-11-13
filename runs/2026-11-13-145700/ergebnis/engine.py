"""engine.py - Sudoku-Engine (nur Standardbibliothek)."""
import json
import random
import sys

CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}

_ALL = 0x1FF


def _box(i):
    return (i // 27) * 3 + (i % 9) // 3


def _search(grid, limit, randomize):
    """Sucht bis zu `limit` Lösungen mit Bitmasken und MRV-Heuristik."""
    if limit <= 0 or len(grid) != 81:
        return []
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []
    for i, v in enumerate(grid):
        if not isinstance(v, int) or v < 0 or v > 9:
            return []
        if v == 0:
            empties.append(i)
            continue
        bit = 1 << (v - 1)
        r, c, b = i // 9, i % 9, _box(i)
        if (rows[r] | cols[c] | boxes[b]) & bit:
            return []  # Vorgaben widersprechen sich
        rows[r] |= bit
        cols[c] |= bit
        boxes[b] |= bit

    work = list(grid)
    found = []
    remaining = set(empties)

    def rec():
        best = -1
        best_mask = 0
        best_n = 10
        for i in remaining:
            m = ~(rows[i // 9] | cols[i % 9] | boxes[_box(i)]) & _ALL
            n = bin(m).count("1")
            if n < best_n:
                best, best_mask, best_n = i, m, n
                if n <= 1:
                    break
        if best == -1:
            found.append(list(work))
            return len(found) >= limit
        if best_n == 0:
            return False
        r, c, b = best // 9, best % 9, _box(best)
        digits = [d for d in range(9) if best_mask >> d & 1]
        if randomize:
            random.shuffle(digits)
        remaining.discard(best)
        for d in digits:
            bit = 1 << d
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            work[best] = d + 1
            stop = rec()
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
            work[best] = 0
            if stop:
                remaining.add(best)
                return True
        remaining.add(best)
        return False

    rec()
    return found


def solutions(puzzle, limit):
    """Liefert bis zu `limit` verschiedene Lösungen (Listen mit 81 Zahlen)."""
    return _search(list(puzzle), limit, False)


def conflicts(grid):
    """Indizes (0-80), die in Zeile, Spalte oder Block mit einem anderen Feld kollidieren."""
    result = set()
    units = []
    for k in range(9):
        units.append([k * 9 + j for j in range(9)])
        units.append([j * 9 + k for j in range(9)])
        br, bc = (k // 3) * 3, (k % 3) * 3
        units.append([(br + a) * 9 + bc + b for a in range(3) for b in range(3)])
    for unit in units:
        seen = {}
        for i in unit:
            v = grid[i]
            if v:
                seen.setdefault(v, []).append(i)
        for idxs in seen.values():
            if len(idxs) > 1:
                result.update(idxs)
    return result


def _full_grid():
    return _search([0] * 81, 1, True)[0]


def generate(level):
    """Erzeugt ein Rätsel mit genau einer Lösung und CLUES[level] Hinweisen."""
    if level not in CLUES:
        raise ValueError("Unbekannte Stufe: %r" % (level,))
    target = CLUES[level]
    while True:
        solution = _full_grid()
        puzzle = list(solution)
        count = 81
        order = list(range(81))
        random.shuffle(order)
        for i in order:
            if count == target:
                break
            old = puzzle[i]
            puzzle[i] = 0
            if len(_search(puzzle, 2, False)) == 1:
                count -= 1
            else:
                puzzle[i] = old
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
    sys.stderr.write("Aufruf: python engine.py neu <%s>\n" % "|".join(CLUES))
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
