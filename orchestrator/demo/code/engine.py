"""Sudoku-Logik. Aufruf: python engine.py neu mittel"""
import json
import random
import sys

CLUES = {"leicht": 38, "mittel": 32, "schwer": 26}
ALL = 0x3FE


def _peers(i):
    r, c = divmod(i, 9)
    out = set()
    for j in range(81):
        rr, cc = divmod(j, 9)
        if j != i and (rr == r or cc == c or (rr // 3 == r // 3 and cc // 3 == c // 3)):
            out.add(j)
    return tuple(out)


PEERS = tuple(_peers(i) for i in range(81))


def _candidates(g, i):
    used = 0
    for p in PEERS[i]:
        used |= 1 << g[p]
    return ALL & ~used


def _pick(g):
    best, best_n, best_m = -1, 10, 0
    for i in range(81):
        if g[i]:
            continue
        m = _candidates(g, i)
        n = bin(m).count("1")
        if n < best_n:
            best, best_n, best_m = i, n, m
            if n <= 1:
                break
    return best, best_m


def _fill(g):
    i, m = _pick(g)
    if i < 0:
        return True
    digits = [d for d in range(1, 10) if m & (1 << d)]
    random.shuffle(digits)
    for d in digits:
        g[i] = d
        if _fill(g):
            return True
    g[i] = 0
    return False


def solved():
    g = [0] * 81
    _fill(g)
    return g


def solutions(puzzle, limit=2):
    g, found = list(puzzle), []

    def go():
        i, m = _pick(g)
        if i < 0:
            found.append(list(g))
            return
        for d in range(1, 10):
            if m & (1 << d):
                g[i] = d
                go()
                if len(found) >= limit:
                    break
        g[i] = 0

    go()
    return found


def generate(level="mittel"):
    target, best = CLUES[level], None
    for _ in range(8):
        solution, clues = solved(), 81
        puzzle = list(solution)
        for i in random.sample(range(81), 81):
            if clues <= target:
                break
            keep, puzzle[i] = puzzle[i], 0
            if len(solutions(puzzle, 2)) == 1:
                clues -= 1
            else:
                puzzle[i] = keep
        if best is None or clues < best["clues"]:
            best = {"puzzle": puzzle, "solution": solution, "clues": clues, "level": level}
        if clues <= target:
            break
    return best


def conflicts(g):
    return {i for i in range(81) if g[i] and any(g[p] == g[i] for p in PEERS[i])}


if __name__ == "__main__":
    print(json.dumps(generate(sys.argv[2] if len(sys.argv) > 2 else "mittel")))
