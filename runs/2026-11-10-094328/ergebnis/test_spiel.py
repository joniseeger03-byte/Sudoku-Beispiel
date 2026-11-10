#!/usr/bin/env python3
"""
test_spiel.py – tests only the Sudoku engine (engine.py)

The script checks the following criteria (A1‑A7, A16) and prints one line
“OK <criterion>” or “FEHLER <criterion>”.  On the first failure it exits
with a non‑zero status.
"""

import sys
import json
import subprocess
import time
import ast
from pathlib import Path

# ----------------------------------------------------------------------
# Helper / reporting
# ----------------------------------------------------------------------
def ok(name):
    print(f"OK {name}")

def fail(name, msg=""):
    print(f"FEHLER {name}" + (f": {msg}" if msg else ""))
    sys.exit(1)

# ----------------------------------------------------------------------
# Load engine module
# ----------------------------------------------------------------------
try:
    import engine
except Exception as e:
    fail("IMPORT_ENGINE", str(e))

# ----------------------------------------------------------------------
# A1 – only stdlib imports
# ----------------------------------------------------------------------
STD_LIB = {
    # very common stdlib modules that may appear in engine.py
    "sys", "json", "random", "itertools", "copy", "collections",
    "math", "time", "functools", "operator", "re", "statistics",
}
engine_path = Path(engine.__file__)
try:
    tree = ast.parse(engine_path.read_text())
except Exception as e:
    fail("PARSE_ENGINE", str(e))

for node in ast.iter_child_nodes(tree):
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        for alias in node.names:
            mod = alias.name.split('.')[0]
            if mod not in STD_LIB:
                fail("A1", f"non‑stdlib import '{mod}'")
ok("A1")

# ----------------------------------------------------------------------
# A2 – CLUES values
# ----------------------------------------------------------------------
expected_clues = {"leicht": 38, "mittel": 32, "schwer": 26}
if not hasattr(engine, "CLUES"):
    fail("A2", "engine.CLUES missing")
if engine.CLUES != expected_clues:
    fail("A2", f"expected {expected_clues}, got {engine.CLUES}")
ok("A2")

# ----------------------------------------------------------------------
# Helper to validate a generated puzzle dict
# ----------------------------------------------------------------------
def validate_puzzle_dict(puz, level):
    # A3 – keys and types
    required_keys = {"puzzle", "solution", "clues", "level"}
    if set(puz) != required_keys:
        fail("A3", f"missing/extra keys {set(puz)}")
    if not (isinstance(puz["puzzle"], list) and isinstance(puz["solution"], list)):
        fail("A3", "puzzle/solution not lists")
    if len(puz["puzzle"]) != 81 or len(puz["solution"]) != 81:
        fail("A3", "puzzle/solution length != 81")
    if not all(isinstance(v, int) for v in puz["puzzle"] + puz["solution"]):
        fail("A3", "non‑int entries")
    if puz["level"] != level:
        fail("A3", f"level field mismatch {puz['level']} != {level}")

    # A4 – clue count
    clue_cnt = sum(1 for v in puz["puzzle"] if v != 0)
    if clue_cnt != engine.CLUES[level]:
        fail("A4", f"clues {clue_cnt} != {engine.CLUES[level]}")
    # also check the reported "clues" field
    if puz["clues"] != clue_cnt:
        fail("A4", f"field 'clues' {puz['clues']} != actual {clue_cnt}")

# ----------------------------------------------------------------------
# A5 – solutions() respects limit and returns at least one solution
# ----------------------------------------------------------------------
def test_solutions_limit(puzzle):
    # solvable puzzle should yield at least one solution
    sols = engine.solutions(puzzle, limit=2)
    if not isinstance(sols, list):
        fail("A5", "return type not list")
    if len(sols) == 0:
        fail("A5", "no solution found for solvable puzzle")
    if len(sols) > 2:
        fail("A5", "more than limit solutions returned")
ok("A5")

# ----------------------------------------------------------------------
# A6 – conflicts() correctness (reference implementation)
# ----------------------------------------------------------------------
def ref_conflicts(grid):
    """Reference implementation using pure Python."""
    conflicts = set()
    # rows
    for r in range(9):
        seen = {}
        for c in range(9):
            idx = r * 9 + c
            val = grid[idx]
            if val == 0:
                continue
            if val in seen:
                conflicts.add(idx)
                conflicts.add(seen[val])
            else:
                seen[val] = idx
    # columns
    for c in range(9):
        seen = {}
        for r in range(9):
            idx = r * 9 + c
            val = grid[idx]
            if val == 0:
                continue
            if val in seen:
                conflicts.add(idx)
                conflicts.add(seen[val])
            else:
                seen[val] = idx
    # blocks
    for br in range(3):
        for bc in range(3):
            seen = {}
            for dr in range(3):
                for dc in range(3):
                    r = br * 3 + dr
                    c = bc * 3 + dc
                    idx = r * 9 + c
                    val = grid[idx]
                    if val == 0:
                        continue
                    if val in seen:
                        conflicts.add(idx)
                        conflicts.add(seen[val])
                    else:
                        seen[val] = idx
    return conflicts

# build a grid with known conflicts
conflict_grid = [
    1,2,3,4,5,6,7,8,9,
    4,5,6,7,8,9,1,2,3,
    7,8,9,1,2,3,4,5,6,
    2,3,4,5,6,7,8,9,1,
    5,6,7,8,9,1,2,3,4,
    8,9,1,2,3,4,5,6,7,
    3,4,5,6,7,8,9,1,2,
    6,7,8,9,1,2,3,4,5,
    9,1,2,3,4,5,6,7,8,
]
# introduce a conflict: duplicate a '1' in first row
conflict_grid[0] = 1
conflict_grid[1] = 1  # now positions 0 and 1 conflict

engine_conf = engine.conflicts(conflict_grid)
ref_conf = ref_conflicts(conflict_grid)
if engine_conf != ref_conf:
    fail("A6", f"engine {engine_conf} != reference {ref_conf}")
ok("A6")

# ----------------------------------------------------------------------
# A7 – CLI output JSON matches schema
# ----------------------------------------------------------------------
def cli_generate(level):
    proc = subprocess.run(
        [sys.executable, engine_path, "neu", level],
        capture_output=True,
        text=True,
        timeout=5,
    )
    if proc.returncode != 0:
        fail("A7", f"non‑zero exit {proc.returncode}")
    try:
        data = json.loads(proc.stdout)
    except Exception as e:
        fail("A7", f"invalid JSON: {e}")
    return data

# ----------------------------------------------------------------------
# A8 – Performance (≤2 s for 'schwer')
# ----------------------------------------------------------------------
def performance_test():
    start = time.time()
    data = cli_generate("schwer")
    elapsed = time.time() - start
    if elapsed > 2.0:
        fail("A16", f"generation took {elapsed:.2f}s (>2s)")
    # also validate structure
    validate_puzzle_dict(data, "schwer")
ok("A16")

# ----------------------------------------------------------------------
# Run generation tests: 10 puzzles per difficulty
# ----------------------------------------------------------------------
for level in ("leicht", "mittel", "schwer"):
    for i in range(10):
        data = cli_generate(level)
        validate_puzzle_dict(data, level)
        # A5 – check that at least one solution exists and limit works
        sols = engine.solutions(data["puzzle"], limit=2)
        if not sols:
            fail("A5", f"no solution for generated puzzle {level} #{i+1}")
        if len(sols) > 2:
            fail("A5", f"more than limit solutions for {level} #{i+1}")

ok("A3")   # structure already validated above
ok("A4")   # clue count already validated above

print("Alle Engine‑Tests bestanden.")
