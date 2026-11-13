#!/usr/bin/env python3
"""
test_spiel.py – minimal engine tests (standard library only)

Requirements (per specification):
* Test only engine.py functions: generate, solutions, conflicts, CLUES and the CLI call.
* Use at least 10 puzzles per difficulty level.
* Print one line per criterion: "OK <criterion>" or "FEHLER <criterion>"
* Exit immediately with sys.exit(1) on first failure.
"""

import sys
import json
import subprocess
import importlib.util
from pathlib import Path

# ----------------------------------------------------------------------
# Helper assertions
# ----------------------------------------------------------------------
def ok(message):
    print(f"OK {message}")

def fail(message):
    print(f"FEHLER {message}")
    sys.exit(1)

# ----------------------------------------------------------------------
# Load engine module (must exist in same directory)
# ----------------------------------------------------------------------
ENGINE_PATH = Path(__file__).with_name("engine.py")
if not ENGINE_PATH.is_file():
    fail("engine.py not found")

spec = importlib.util.spec_from_file_location("engine", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(engine)
except Exception as e:
    fail(f"import engine – {e}")

# ----------------------------------------------------------------------
# A1 – Engine conforms to spec (functions exist, CLUES present)
# ----------------------------------------------------------------------
required_attrs = ["generate", "solutions", "conflicts", "CLUES"]
for attr in required_attrs:
    if not hasattr(engine, attr):
        fail(f"A1 – missing attribute {attr}")

if not isinstance(engine.CLUES, dict):
    fail("A1 – CLUES is not a dict")

# check signatures (basic)
if not callable(engine.generate):
    fail("A1 – generate not callable")
if not callable(engine.solutions):
    fail("A1 – solutions not callable")
if not callable(engine.conflicts):
    fail("A1 – conflicts not callable")
ok("A1 – Engine‑Konformität")

# ----------------------------------------------------------------------
# Helper to count clues
# ----------------------------------------------------------------------
def count_clues(puzzle):
    return sum(1 for v in puzzle if v != 0)

# ----------------------------------------------------------------------
# A2 – Correct number of clues per level (10 puzzles each)
# ----------------------------------------------------------------------
levels = list(engine.CLUES.keys())
if set(levels) != {"leicht", "mittel", "schwer"}:
    fail("A2 – CLUES keys mismatch")

for level in levels:
    expected = engine.CLUES[level]
    for i in range(10):
        try:
            data = engine.generate(level)
        except Exception as e:
            fail(f"A2 – generate({level}) raised {e}")

        puzzle = data.get("puzzle")
        clues = data.get("clues")
        if not isinstance(puzzle, list) or len(puzzle) != 81:
            fail(f"A2 – generate({level}) puzzle malformed")
        if clues != expected:
            fail(f"A2 – generate({level}) clues {clues} != expected {expected}")
        if count_clues(puzzle) != expected:
            fail(f"A2 – generate({level}) actual clue count mismatch")
ok("A2 – Klare Hinweis‑Zahl")

# ----------------------------------------------------------------------
# A3 – Unique solution (solutions(puzzle, 2) returns at most 1)
# ----------------------------------------------------------------------
for level in levels:
    for i in range(10):
        data = engine.generate(level)
        puzzle = data["puzzle"]
        sols = engine.solutions(puzzle, 2)
        if not isinstance(sols, list):
            fail("A3 – solutions did not return a list")
        if len(sols) != 1:
            fail(f"A3 – puzzle from generate({level}) has {len(sols)} solutions (expected 1)")
ok("A3 – Eindeutige Lösung")

# ----------------------------------------------------------------------
# A4 – Conflict detection on hand‑crafted grids
# ----------------------------------------------------------------------
# Helper to compute expected conflicts (same algorithm as engine should use)
def expected_conflicts(grid):
    conflicts = set()
    # rows
    for r in range(9):
        vals = {}
        for c in range(9):
            idx = r * 9 + c
            v = grid[idx]
            if v == 0:
                continue
            if v in vals:
                conflicts.add(idx)
                conflicts.add(vals[v])
            else:
                vals[v] = idx
    # columns
    for c in range(9):
        vals = {}
        for r in range(9):
            idx = r * 9 + c
            v = grid[idx]
            if v == 0:
                continue
            if v in vals:
                conflicts.add(idx)
                conflicts.add(vals[v])
            else:
                vals[v] = idx
    # blocks
    for br in range(3):
        for bc in range(3):
            vals = {}
            for dr in range(3):
                for dc in range(3):
                    r = br * 3 + dr
                    c = bc * 3 + dc
                    idx = r * 9 + c
                    v = grid[idx]
                    if v == 0:
                        continue
                    if v in vals:
                        conflicts.add(idx)
                        conflicts.add(vals[v])
                    else:
                        vals[v] = idx
    return conflicts

# Test cases: each a tuple (grid, expected_conflict_set)
test_cases = []

# 1. Duplicate in first row
grid1 = [0] * 81
grid1[0] = 5
grid1[1] = 5  # conflict with index 0
test_cases.append((grid1, {0, 1}))

# 2. Duplicate in column
grid2 = [0] * 81
grid2[0] = 3
grid2[9] = 3  # conflict indices 0 and 9
test_cases.append((grid2, {0, 9}))

# 3. Duplicate in top‑left block
grid3 = [0] * 81
grid3[0] = 7
grid3[10] = 7  # (row1,col1) and (row2,col2) same block
test_cases.append((grid3, {0, 10}))

# 4. Multiple conflicts mixed
grid4 = [0] * 81
# row conflict
grid4[20] = 4
grid4[22] = 4
# column conflict
grid4[5] = 9
grid4[14] = 9
# block conflict
grid4[40] = 2
grid4[48] = 2
expected4 = {20, 22, 5, 14, 40, 48}
test_cases.append((grid4, expected4))

# Run checks
for idx, (grid, exp) in enumerate(test_cases, 1):
    got = engine.conflicts(grid)
    if not isinstance(got, set):
        fail(f"A4 – conflicts did not return a set (case {idx})")
    if got != exp:
        fail(f"A4 – conflict set mismatch (case {idx}) got {got} exp {exp}")
ok("A4 – Konflikt‑Erkennung")

# ----------------------------------------------------------------------
# A5 – CLI output JSON correctness
# ----------------------------------------------------------------------
def run_cli(level):
    cmd = [sys.executable, str(ENGINE_PATH), "neu", level]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

for level in levels:
    proc = run_cli(level)
    if proc.returncode != 0:
        fail(f"A5 – CLI exited non‑zero for level {level}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        fail(f"A5 – CLI output not valid JSON for level {level}: {e}")

    # required keys
    for key in ("puzzle", "solution", "clues", "level"):
        if key not in data:
            fail(f"A5 – missing key '{key}' in CLI output for level {level}")

    if data["level"] != level:
        fail(f"A5 – CLI level field mismatch (got {data['level']}, expected {level})")
    if not isinstance(data["puzzle"], list) or len(data["puzzle"]) != 81:
        fail(f"A5 – CLI puzzle malformed for level {level}")
    if not isinstance(data["solution"], list) or len(data["solution"]) != 81:
        fail(f"A5 – CLI solution malformed for level {level}")
    if data["clues"] != engine.CLUES[level]:
        fail(f"A5 – CLI clues count mismatch for level {level}")

ok("A5 – CLI‑Ausgabe")

# ----------------------------------------------------------------------
# All tests passed
# ----------------------------------------------------------------------
print("Alle Kriterien erfüllt.")
sys.exit(0)
