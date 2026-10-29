#!/usr/bin/env python3
"""Dispute 100: are the Hodge-transmutation 'results' computed or typed in?
AST-walks HodgeTransmutationOperator.execute() and lists every numeric literal assigned
to a result key, then checks whether Kineton's complex (curl 3.8667) is ever an input."""
import ast, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "experiments/causal-dag-transmutation"))
from pathlib import Path
src_path = Path(__file__).resolve().parents[2] / "experiments/causal-dag-transmutation/transmutation_engine.py"
tree = ast.parse(src_path.read_text())
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "HodgeTransmutationOperator")
fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "execute")
lits, calls = {}, []
for n in ast.walk(fn):
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        v = n.value
        try:
            val = ast.literal_eval(v)
            if isinstance(val, (int, float)):
                lits[n.targets[0].id] = val
        except Exception:
            if isinstance(v, ast.Call) and getattr(v.func, "id", "") == "min":
                try: lits[n.targets[0].id + " (min of literals)"] = [ast.literal_eval(a) for a in v.args]
                except Exception: pass
    if isinstance(n, ast.Dict):
        for k, v in zip(n.keys, n.values):
            try:
                kk, vv = ast.literal_eval(k), ast.literal_eval(v)
                calls.append((kk, vv))
            except Exception:
                pass
print("Numeric literals assigned in execute():")
for k, v in lits.items(): print(f"  {k} = {v}")
print("Result-dict entries that are pure literals:")
for k, v in calls: print(f"  {k!r}: {v!r}")
mod = {}
exec(compile(src_path.read_text(), str(src_path), "exec"), mod)
r = mod["HodgeTransmutationOperator"].execute()
print("Returned:", {k: r[k] for k in r if not isinstance(r[k], (list, dict))})
# Falsifier: change the only real computation (the 3x3 system) and see if anything reported changes.
text = src_path.read_text().replace("rhs = [1.0, 0.5, 0.0]", "rhs = [9.0, -4.0, 7.0]")
mod2 = {}
exec(compile(text, "mutated", "exec"), mod2)
r2 = mod2["HodgeTransmutationOperator"].execute()
same = all(r[k] == r2[k] for k in r if k in r2 and isinstance(r[k], (int, float, bool, str)))
print("Reported scalar fields identical after replacing the solve's right-hand side:", same)
import re
print("import/open/read of any Kineton data file in the module:", bool(re.search(r"(open\(|json\.load|read_text|import\s+kineton)", src_path.read_text())))
