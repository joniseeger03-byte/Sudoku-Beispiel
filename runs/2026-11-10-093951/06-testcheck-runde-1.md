Der Test ist falsch. Der A1-Check hat zwei eigene Fehler und prüft die Engine nicht korrekt:

- `importlib.util` wird nie importiert. `importlib.util.find_spec` kann deshalb einen `AttributeError` auslösen. Der steckt hinter dem allgemeinen `except` und wird als "Failed to resolve import: json" gemeldet.
- Der Test vergleicht `spec.origin` mit dem Stdlib-Pfad. Eingebaute Module wie `sys` oder `time` haben als Origin `"built-in"` und fielen deshalb fälschlich durch.
- Das Parsen mit `line.split()[1]` liefert bei `import a, b` oder `import a.b` falsche Modulnamen.

Die Spezifikation verlangt nur, dass die Engine ausschließlich Standardbibliothek-Module nutzt. Das prüft die korrigierte Fassung mit `ast` und `sys.stdlib_module_names`.

URTEIL: test

```python
#!/usr/bin/env python3
"""
test_spiel.py – validates the Sudoku engine according to the specification.
Only the Python standard library is used.
"""

import sys
import ast
import json
import subprocess
import importlib
import inspect
from pathlib import Path

# ----------------------------------------------------------------------
# Helper assertions
# ----------------------------------------------------------------------
def ok(msg):
    print(f"{msg}: OK")

def fail(msg):
    print(f"{msg}: FEHLER")
    sys.exit(1)

# ----------------------------------------------------------------------
# 1. Import engine and basic module checks (A1, A2)
# ----------------------------------------------------------------------
try:
    engine = importlib.import_module("engine")
except Exception as e:
    fail(f"A1 Import engine module – {e}")

# A1: only stdlib imports
def top_level_imports(source):
    names = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                names.append("." * node.level + (node.module or ""))
            elif node.module:
                names.append(node.module.split(".")[0])
    return names

stdlib_names = set(getattr(sys, "stdlib_module_names", ())) | set(sys.builtin_module_names)
if not stdlib_names:
    fail("A1 Cannot determine standard library module names")
for mod in top_level_imports(inspect.getsource(engine)):
    if mod == "__future__":
        continue
    if mod not in stdlib_names:
        fail(f"A1 Non-standard import detected: {mod}")
ok("A1 Engine uses only standard-library modules")

# A2: CLUES mapping unchanged
expected_clues = {"leicht": 38, "mittel": 32, "schwer": 26}
if not hasattr(engine, "CLUES"):
    fail("A2 engine.CLUES missing")
if engine.CLUES != expected_clues:
    fail(f"A2 engine.CLUES altered: {engine.CLUES}")
ok("A2 CLUES mapping correct")

# ----------------------------------------------------------------------
# 2. Test generate() output structure (A3) – 10 puzzles per level
# ----------------------------------------------------------------------
def test_generate(level):
    result = engine.generate(level)
    if not isinstance(result, dict):
        fail(f"A3 generate({level}) did not return dict")
    for key in ("puzzle", "solution", "clues", "level"):
        if key not in result:
            fail(f"A3 generate({level}) missing key '{key}'")
    puzzle = result["puzzle"]
    solution = result["solution"]
    if not (isinstance(puzzle, list) and isinstance(solution, list)):
        fail(f"A3 generate({level}) puzzle/solution not list")
    if len(puzzle) != 81 or len(solution) != 81:
        fail(f"A3 generate({level}) puzzle/solution length != 81")
    if any(not isinstance(v, int) for v in puzzle + solution):
        fail(f"A3 generate({level}) non-int entries")
    clues = result["clues"]
    if clues != sum(1 for v in puzzle if v != 0):
        fail(f"A3 generate({level}) clues count mismatch")
    if clues != engine.CLUES[level]:
        fail(f"A3 generate({level}) clues not equal CLUES[level]")
    if result["level"] != level:
        fail(f"A3 generate({level}) level field mismatch")
    # ensure solution is a valid completed Sudoku (no zeros)
    if any(v == 0 for v in solution):
        fail(f"A3 generate({level}) solution contains zeros")
    # quick consistency check: solution respects puzzle values
    for i, v in enumerate(puzzle):
        if v != 0 and v != solution[i]:
            fail(f"A3 generate({level}) puzzle/value conflict at index {i}")

for lvl in ("leicht", "mittel", "schwer"):
    for i in range(10):
        test_generate(lvl)
ok("A3 generate() returns correct structure for 10 puzzles per level")

# ----------------------------------------------------------------------
# 3. Test solutions() limits (A4)
# ----------------------------------------------------------------------
def test_solutions_limit():
    # empty grid -> many solutions, but we limit
    empty = [0] * 81
    sols = engine.solutions(empty, limit=3)
    if not isinstance(sols, list):
        fail("A4 solutions() did not return list")
    if len(sols) > 3:
        fail(f"A4 solutions() returned {len(sols)} > limit 3")
    # each solution must be length 81 list of ints 1-9
    for sol in sols:
        if not (isinstance(sol, list) and len(sol) == 81):
            fail("A4 solution entry malformed")
        if any(not (1 <= v <= 9) for v in sol):
            fail("A4 solution contains invalid digits")
test_solutions_limit()
ok("A4 solutions() respects limit")

# ----------------------------------------------------------------------
# 4. Test conflicts() (A5)
# ----------------------------------------------------------------------
def test_conflicts():
    # a grid with a deliberate conflict: duplicate '5' in first row
    grid = [5, 5] + [0] * 79
    conflicted = engine.conflicts(grid)
    if not isinstance(conflicted, set):
        fail("A5 conflicts() did not return set")
    if 0 not in conflicted or 1 not in conflicted:
        fail("A5 conflicts() missed conflicting indices")
    # a correct grid (solution from generate) should yield empty set
    for lvl in ("leicht", "mittel", "schwer"):
        g = engine.generate(lvl)
        empty_conf = engine.conflicts(g["solution"])
        if empty_conf:
            fail(f"A5 conflicts() reported conflicts on a valid solution for {lvl}")
test_conflicts()
ok("A5 conflicts() correctly identifies conflicts")

# ----------------------------------------------------------------------
# 5. Test CLI output (A6) – generate JSON via subprocess
# ----------------------------------------------------------------------
def test_cli():
    script = Path(__file__).with_name("engine.py")
    if not script.is_file():
        fail("A6 engine.py not found")
    for lvl in ("leicht", "mittel", "schwer"):
        proc = subprocess.run(
            [sys.executable, str(script), "neu", lvl],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            fail(f"A6 CLI non-zero exit for level {lvl}")
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            fail(f"A6 CLI output not valid JSON for level {lvl}: {e}")
        # verify same structure as generate()
        if not isinstance(data, dict):
            fail(f"A6 CLI output not dict for level {lvl}")
        for key in ("puzzle", "solution", "clues", "level"):
            if key not in data:
                fail(f"A6 CLI missing key '{key}' for level {lvl}")
        if data["level"] != lvl:
            fail(f"A6 CLI level field mismatch for {lvl}")
        if data["clues"] != engine.CLUES[lvl]:
            fail(f"A6 CLI clues count mismatch for {lvl}")
    ok("A6 CLI generate command outputs correct JSON")
test_cli()

# ----------------------------------------------------------------------
# All tests passed
# ----------------------------------------------------------------------
print("Alle Kriterien erfüllt.")
sys.exit(0)
```