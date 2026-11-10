#!/usr/bin/env python3
"""
test_spiel.py – minimal test suite for engine.py

Requirements:
* Only the Python standard library is used.
* Tests generate(), solutions(), conflicts(), CLUES and the CLI call
  `python engine.py neu <stufe>`.
* For each level ("leicht","mittel","schwer") at least 10 puzzles are generated.
* On first failure the script prints "FEHLER" and exits with code 1.
* On success each criterion prints "OK".
"""

import json
import subprocess
import sys
from pathlib import Path

# ----------------------------------------------------------------------
# Import the engine module (assumed to be in the same directory)
# ----------------------------------------------------------------------
import importlib.util

ENGINE_PATH = Path(__file__).with_name("engine.py")
if not ENGINE_PATH.is_file():
    print("FEHLER: engine.py not found")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("engine", ENGINE_PATH)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)  # type: ignore

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def ok(msg: str) -> None:
    """Print a successful test line."""
    print(f"{msg}: OK")


def fail(msg: str) -> None:
    """Print a failure line and abort the test run."""
    print(f"{msg}: FEHLER")
    sys.exit(1)


def count_clues(puzzle):
    """Return number of non‑zero entries."""
    return sum(1 for v in puzzle if v != 0)


def run_cli(level: str) -> dict:
    """Execute `python engine.py neu <level>` and return parsed JSON."""
    try:
        result = subprocess.run(
            [sys.executable, str(ENGINE_PATH), "neu", level],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        fail(f"CLI-{level}")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        fail(f"CLI-{level}")
    return data


# ----------------------------------------------------------------------
# 1. Test CLUES constant
# ----------------------------------------------------------------------
expected_clues = {"leicht": 38, "mittel": 32, "schwer": 26}
if getattr(engine, "CLUES", None) != expected_clues:
    fail("A1_CLUES")
ok("A1_CLUES")


# ----------------------------------------------------------------------
# 2. Test generate() and uniqueness of solution (A1, A2, A10)
# ----------------------------------------------------------------------
def test_generate_level(level: str) -> None:
    for i in range(10):
        result = engine.generate(level)

        # basic structure
        for key in ("puzzle", "solution", "clues", "level"):
            if key not in result:
                fail(f"GEN_{level}_{i}_{key}")

        # level field matches request
        if result["level"] != level:
            fail(f"GEN_{level}_{i}_level_mismatch")

        # clue count matches CLUES
        if result["clues"] != engine.CLUES[level]:
            fail(f"GEN_{level}_{i}_clues")

        # puzzle length
        if len(result["puzzle"]) != 81 or len(result["solution"]) != 81:
            fail(f"GEN_{level}_{i}_length")

        # uniqueness: exactly one solution
        sols = engine.solutions(result["puzzle"], limit=2)
        if len(sols) != 1:
            fail(f"GEN_{level}_{i}_unique")

    ok(f"GEN_{level}")


for lvl in ("leicht", "mittel", "schwer"):
    test_generate_level(lvl)


# ----------------------------------------------------------------------
# 3. Test conflicts() on a known grid (A7)
# ----------------------------------------------------------------------
def test_conflicts():
    grid = [0] * 81

    # Row conflict: index 4 and 8 (row 0, cols 4 and 8, different blocks), value 5
    grid[4] = 5
    grid[8] = 5

    # Column conflict: index 0 and 27 (col 0, rows 0 and 3, different blocks), value 7
    grid[0] = 7
    grid[27] = 7

    # Block conflict: index 10 (row 1, col 1) and 20 (row 2, col 2),
    # both in block 0, different row and column, value 3
    grid[10] = 3
    grid[20] = 3

    conflicted = engine.conflicts(grid)

    expected = {4, 8, 0, 27, 10, 20}
    if set(conflicted) != expected:
        fail("CONF_expected_mismatch")

    # A grid without duplicates yields no conflicts
    clean = [0] * 81
    clean[0] = 1
    clean[1] = 2
    clean[9] = 3
    if set(engine.conflicts(clean)) != set():
        fail("CONF_clean_grid")

    ok("CONF")


test_conflicts()


# ----------------------------------------------------------------------
# 4. Test CLI output (A3)
# ----------------------------------------------------------------------
def test_cli():
    for level in ("leicht", "mittel", "schwer"):
        data = run_cli(level)

        # required keys
        for key in ("puzzle", "solution", "clues", "level"):
            if key not in data:
                fail(f"CLI_{level}_missing_{key}")

        # types
        if not isinstance(data["puzzle"], list) or len(data["puzzle"]) != 81:
            fail(f"CLI_{level}_puzzle")
        if not isinstance(data["solution"], list) or len(data["solution"]) != 81:
            fail(f"CLI_{level}_solution")
        if not isinstance(data["clues"], int):
            fail(f"CLI_{level}_clues_type")
        if data["level"] != level:
            fail(f"CLI_{level}_level_mismatch")

        # clue count matches constant
        if data["clues"] != engine.CLUES[level]:
            fail(f"CLI_{level}_clues_wrong")

    ok("CLI")


test_cli()

# ----------------------------------------------------------------------
# All tests passed
# ----------------------------------------------------------------------
print("Alle Tests erfolgreich.")
