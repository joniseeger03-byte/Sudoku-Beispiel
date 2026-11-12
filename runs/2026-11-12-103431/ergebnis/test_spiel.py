#!/usr/bin/env python3
"""
test_spiel.py - minimal test suite for engine.py

Only the engine API is verified (A1-A4).  UI-related criteria are ignored
as they are exercised by separate browser-side tests.
"""

import sys
import json
import subprocess
import time
from pathlib import Path

# ----------------------------------------------------------------------
# Import the engine module (must be in the same directory)
# ----------------------------------------------------------------------
try:
    import engine
except Exception as e:
    print(f"FEHLER - import engine: {e}")
    sys.exit(1)

# ----------------------------------------------------------------------
# Helper assertions
# ----------------------------------------------------------------------
def ok(msg):
    print(f"{msg}: OK")

def fail(msg, details=""):
    print(f"{msg}: FEHLER{(' - ' + details) if details else ''}")
    sys.exit(1)

# ----------------------------------------------------------------------
# A1 - Generator-Korrektheit & A2 - Eindeutige Loesung
# ----------------------------------------------------------------------
def test_generate():
    levels = list(engine.CLUES.keys())
    for level in levels:
        for i in range(10):          # 10 puzzles per level
            try:
                data = engine.generate(level)
            except Exception as e:
                fail("A1 - generate raised", f"{e}")

            # required keys
            for key in ("puzzle", "solution", "clues", "level"):
                if key not in data:
                    fail("A1 - missing key", f"{key}")

            puzzle = data["puzzle"]
            solution = data["solution"]
            clues = data["clues"]

            # 81 cells
            if not (isinstance(puzzle, list) and len(puzzle) == 81):
                fail("A1 - puzzle size", "must be list of 81")
            if not (isinstance(solution, list) and len(solution) == 81):
                fail("A1 - solution size", "must be list of 81")

            # clue count
            expected_clues = engine.CLUES[level]
            actual_clues = sum(1 for v in puzzle if v != 0)
            if actual_clues != expected_clues:
                fail("A1 - clue count", f"{actual_clues} vs {expected_clues}")

            # solution must be a valid Sudoku (no zeros)
            if any(v == 0 for v in solution):
                fail("A1 - solution contains zeros")

            # solution must match puzzle where puzzle is non-zero
            for p, s in zip(puzzle, solution):
                if p != 0 and p != s:
                    fail("A1 - puzzle-solution mismatch")

            # uniqueness
            sols = engine.solutions(puzzle, limit=2)
            if not isinstance(sols, list):
                fail("A2 - solutions return type", "expected list")
            if len(sols) != 1:
                fail("A2 - not unique", f"found {len(sols)} solutions")
    ok("A1-A2 - Generator-Korrektheit & eindeutige Loesung")

# ----------------------------------------------------------------------
# A3 - Konflikt-Erkennung
# ----------------------------------------------------------------------
def test_conflicts():
    # grid is a list of 81 ints, 0 = empty; index = row*9+col
    block_grid = [1, 2, 0] + [0] * 6 + [3, 1, 0] + [0] * 69   # 1 at idx 0 and 10
    test_cases = [
        # duplicate in first row (indices 0 and 1)
        ([5, 5] + [0] * 79, {0, 1}),
        # duplicate in first column (indices 0 and 9)
        ([7] + [0] * 8 + [7] + [0] * 71, {0, 9}),
        # duplicate only in top-left block (row 0 col 0 and row 1 col 1)
        (block_grid, {0, 10}),
        # no conflict
        (engine.generate("leicht")["solution"], set()),
    ]

    for grid, expected in test_cases:
        if len(grid) != 81:
            fail("A3 - test grid size", f"{len(grid)}")
        try:
            result = engine.conflicts(grid)
        except Exception as e:
            fail("A3 - conflicts raised", str(e))

        if not isinstance(result, set):
            fail("A3 - conflicts return type", "expected set")
        if result != expected:
            fail("A3 - conflict set mismatch", f"got {result}, expected {expected}")

    ok("A3 - Konflikt-Erkennung")

# ----------------------------------------------------------------------
# A4 - CLI-Ausgabe
# ----------------------------------------------------------------------
def test_cli():
    levels = list(engine.CLUES.keys())
    for level in levels:
        for _ in range(3):   # a few calls per level
            cmd = [sys.executable, Path(__file__).parent / "engine.py", "neu", level]
            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
            except Exception as e:
                fail("A4 - subprocess error", str(e))

            if proc.returncode != 0:
                fail("A4 - non-zero exit", f"rc={proc.returncode}")

            try:
                data = json.loads(proc.stdout)
            except json.JSONDecodeError as e:
                fail("A4 - invalid JSON", str(e))

            for key in ("puzzle", "solution", "clues", "level"):
                if key not in data:
                    fail("A4 - missing key in CLI output", key)

            if data["level"] != level:
                fail("A4 - level mismatch", f"{data['level']} vs {level}")

            if sum(1 for v in data["puzzle"] if v != 0) != engine.CLUES[level]:
                fail("A4 - clue count mismatch", f"{level}")

    ok("A4 - CLI-Ausgabe")

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
if __name__ == "__main__":
    start = time.time()
    test_generate()
    test_conflicts()
    test_cli()
    elapsed = time.time() - start
    print(f"Alle Tests bestanden in {elapsed:.2f}s")
    sys.exit(0)
