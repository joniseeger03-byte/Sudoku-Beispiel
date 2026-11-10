#!/usr/bin/env python3
"""
test_spiel.py – minimal engine tests (A1, A2, A3)

Runs without any third‑party libraries, only the Python standard library.
"""

import sys
import json
import subprocess
from pathlib import Path

# ----------------------------------------------------------------------
# import the engine module (must be in the same directory)
# ----------------------------------------------------------------------
try:
    import engine
except Exception as e:
    print(f"FEHLER: konnte engine nicht importieren – {e}")
    sys.exit(1)

# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def run_cli(level: str) -> dict:
    """Execute `python engine.py neu <level>` and return the parsed JSON."""
    cmd = [sys.executable, Path(__file__).with_name("engine.py").as_posix(), "neu", level]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, timeout=5
        )
    except subprocess.CalledProcessError as exc:
        print(f"FEHLER: CLI‑Aufruf fehlgeschlagen für Stufe {level} – {exc}")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"FEHLER: CLI‑Aufruf timed out für Stufe {level}")
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"FEHLER: JSON‑Parsing fehlgeschlagen für Stufe {level} – {exc}")
        sys.exit(1)

    return data


def reference_conflicts(grid: list) -> set:
    """Independent reference: indices of non-zero cells sharing a digit
    with another cell in the same row, column or block."""
    result = set()
    for i in range(81):
        if grid[i] == 0:
            continue
        for j in range(81):
            if i == j or grid[j] != grid[i]:
                continue
            same_row = i // 9 == j // 9
            same_col = i % 9 == j % 9
            same_block = (i // 27 == j // 27) and ((i % 9) // 3 == (j % 9) // 3)
            if same_row or same_col or same_block:
                result.add(i)
                break
    return result


def check_a1(level: str, data: dict) -> None:
    """A1 – clues count must equal CLUES[level]."""
    expected = engine.CLUES.get(level)
    actual = data.get("clues")
    if expected != actual:
        print(
            f"FEHLER: A1 – {level}: clues {actual} ≠ erwartete {expected}"
        )
        sys.exit(1)
    print(f"OK: A1 – {level}")


def check_a2(puzzle: list) -> None:
    """A2 – the puzzle must have exactly one solution."""
    sols = engine.solutions(puzzle, limit=2)
    if len(sols) != 1:
        print(f"FEHLER: A2 – puzzle hat {len(sols)} Lösungen (erwartet 1)")
        sys.exit(1)
    print("OK: A2")


def check_a3() -> None:
    """A3 – conflicts must be reported correctly."""
    solved = engine.generate("leicht")["solution"]
    if len(solved) != 81:
        print("FEHLER: A3 – gelöste Lösung hat nicht 81 Felder")
        sys.exit(1)

    # a valid solution has no conflicts
    clean = engine.conflicts(list(solved))
    if set(clean) != set():
        print(f"FEHLER: A3 – gültige Lösung meldet Konflikte {set(clean)}")
        sys.exit(1)

    # copy the first digit of row 0 onto index 1 -> duplicate in row 0.
    # Column 1 now also contains that digit twice: at index 1 and at the
    # cell in column 1 that originally held it.
    grid = list(solved)
    digit = grid[0]
    grid[1] = digit
    partner = next(i for i in range(10, 81, 9) if solved[i] == digit)

    conflict_set = set(engine.conflicts(grid))

    expected = reference_conflicts(grid)
    must_contain = {0, 1, partner}
    if not must_contain.issubset(expected):
        print("FEHLER: A3 – interner Testfehler bei Referenzberechnung")
        sys.exit(1)

    missing = expected - conflict_set
    extra = conflict_set - expected
    if missing:
        print(f"FEHLER: A3 – fehlende Konflikt‑Indizes {missing}")
        sys.exit(1)
    if extra:
        print(f"FEHLER: A3 – unerwartete Konflikt‑Indizes {extra}")
        sys.exit(1)

    print("OK: A3")


# ----------------------------------------------------------------------
# main test execution
# ----------------------------------------------------------------------
def main() -> None:
    levels = ["leicht", "mittel", "schwer"]
    puzzles_per_level = 10

    # A3 is independent of the random generator – test it once
    check_a3()

    for level in levels:
        for i in range(puzzles_per_level):
            data = run_cli(level)

            # A1 – clue count
            check_a1(level, data)

            # A2 – uniqueness of solution
            puzzle = data.get("puzzle")
            if not isinstance(puzzle, list) or len(puzzle) != 81:
                print(f"FEHLER: A2 – puzzle hat falsches Format (Iteration {i+1} Stufe {level})")
                sys.exit(1)
            check_a2(puzzle)

    # all checks passed
    print("OK: Alle Tests bestanden")
    sys.exit(0)


if __name__ == "__main__":
    main()
