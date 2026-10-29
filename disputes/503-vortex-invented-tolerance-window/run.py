#!/usr/bin/env python3
"""Does test_circulation.py assert the window [0.985, 1.015]? Lists its real circulation tolerances. Writes nothing."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
t = (root/"experiments/vortex-dynamics/test_circulation.py").read_text()
print("occurrences of 0.985 / 1.015 in the test:", t.count("0.985"), t.count("1.015"))
for i,l in enumerate(t.splitlines(),1):
    if re.search(r"delta_gamma|dgamma_dt|rel_drift|g_decayed", l) and "assert" in l:
        print(f"L{i}: {l.strip()}")
