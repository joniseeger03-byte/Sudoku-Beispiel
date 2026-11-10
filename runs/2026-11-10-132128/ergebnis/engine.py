"""engine.py - Sudoku-Engine (nur Python-Standardbibliothek).

Vertrag:
  CLUES, generate(level), solutions(puzzle, limit), conflicts(grid)
  CLI: python engine.py neu <stufe>  -> JSON auf stdout
"""

import json
import random
import sys

CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}

_ALL = 0x3FE  # Bits 1..9


def _box(i):
    return (i // 27) * 3 + (i % 9) // 3


def _search(puzzle, limit, randomize=False):
    """Backtracking mit MRV-Heuristik und Bitmasken. Liefert bis zu `limit`
    vollstaendige Loesungen (jeweils Liste mit 81 Zahlen)."""
    if limit <= 0 or len(puzzle) != 81:
        return []
    grid = list(puzzle)
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
    for i, v in enumerate(grid):
        if v:
            if not 1 <= v <= 9:
                return []
            bit = 1 << v
            r, c, b = i // 9, i % 9, _box(i)
            if (rows[r] | cols[c] | boxes[b]) & bit:
                return []  # widerspruechliche Vorgaben
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit

    found = []

    def rec():
        if len(found) >= limit:
            return
        best, best_mask, best_cnt = -1, 0, 10
        for i in range(81):
            if grid[i] == 0:
                mask = ~(rows[i // 9] | cols[i % 9] | boxes[_box(i)]) & _ALL
                cnt = bin(mask).count("1")
                if cnt < best_cnt:
                    best, best_mask, best_cnt = i, mask, cnt
                    if cnt <= 1:
                        break
        if best == -1:
            found.append(grid[:])
            return
        if best_cnt == 0:
            return
        r, c, b = best // 9, best % 9, _box(best)
        digits = [d for d in range(1, 10) if best_mask & (1 << d)]
        if randomize:
            random.shuffle(digits)
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
            if len(found) >= limit:
                return

    rec()
    return found


def solutions(puzzle, limit):
    """Gibt bis zu `limit` vollstaendige Loesungen zurueck."""
    return _search(puzzle, limit)


def conflicts(grid):
    """Menge aller Indizes, die in Zeile, Spalte oder Block mit einem
    anderen Feld dieselbe Zahl (!= 0) teilen."""
    result = set()
    units = []
    for k in range(9):
        units.append([k * 9 + j for j in range(9)])
        units.append([j * 9 + k for j in range(9)])
        br, bc = (k // 3) * 3, (k % 3) * 3
        units.append([(br + dr) * 9 + bc + dc for dr in range(3) for dc in range(3)])
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


def generate(level):
    """Erzeugt ein Raetsel mit genau einer Loesung und CLUES[level] Hinweisen."""
    if level not in CLUES:
        raise ValueError("Unbekannte Stufe: %r" % (level,))
    target = CLUES[level]
    while True:
        solution = _search([0] * 81, 1, randomize=True)[0]
        puzzle = solution[:]
        order = list(range(81))
        random.shuffle(order)
        count = 81
        for i in order:
            if count <= target:
                break
            v = puzzle[i]
            puzzle[i] = 0
            # Zwei-mal-Backtrack-Prinzip: nach jedem Entfernen nach einer
            # zweiten Loesung suchen (limit=2); nur bei genau 1 bleibt es entfernt.
            if len(solutions(puzzle, 2)) == 1:
                count -= 1
            else:
                puzzle[i] = v
        if count == target:
            return {
                "puzzle": puzzle,
                "solution": solution,
                "clues": count,
                "level": level,
            }
        # Sackgasse (nicht weiter reduzierbar) -> neuer Versuch


def main(argv):
    if len(argv) == 3 and argv[1] == "neu" and argv[2] in CLUES:
        print(json.dumps(generate(argv[2])))
        return 0
    sys.stderr.write("Aufruf: python engine.py neu <leicht|mittel|schwer>\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
