import sys
import time

import engine as S

N = 10
ps, slowest = [], 0
for level in ("leicht", "mittel", "schwer"):
    for _ in range(N):
        t = time.time()
        p = S.generate(level)
        slowest = max(slowest, time.time() - t)
        ps.append(p)


def count(f):
    return sum(1 for p in ps if f(p))


def conflict_found(p):
    g = list(p["solution"])
    g[1] = g[0]
    return 0 in S.conflicts(g)


checks = [
    ("A1 Gueltige Loesung", count(lambda p: len(p["solution"]) == 81 and all(p["solution"]) and not S.conflicts(p["solution"]))),
    ("A2 Genau eine Loesung", count(lambda p: len(S.solutions(p["puzzle"], 2)) == 1)),
    ("A3 Hinweiszahl", count(lambda p: sum(1 for v in p["puzzle"] if v) == S.CLUES[p["level"]])),
    ("A4 Konflikte erkannt", count(conflict_found)),
    ("A5 Fuehrt zur Loesung", count(lambda p: S.solutions(p["puzzle"], 1)[0] == p["solution"])),
    ("A6 Unter 5 Sekunden", len(ps) if slowest < 5 else 0),
]
failed = False
for name, ok in checks:
    print(f"{'OK    ' if ok == len(ps) else 'FEHLER'} {name}: {ok} von {len(ps)}")
    failed = failed or ok != len(ps)
sys.exit(1 if failed else 0)
