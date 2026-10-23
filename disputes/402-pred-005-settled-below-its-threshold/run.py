#!/usr/bin/env python3
"""Dispute 402: PRED-005 says the zone will 'exceed 25 distinct interactive builds'. It was settled HIT
on '24 builds'. Check the claim text against the settlement, and the count at the settling commit."""
import re, subprocess
t = open("evidence/predictions-ledger.md").read()
b = re.split(r"\n(?=### PRED-)", t)
b = [x for x in b if x.startswith("### PRED-005")][0]
print(re.search(r"\*\*Prediction:\*\*.*", b).group())
print(re.search(r"\*\*Status:\*\*.*", b).group())
print("24 > 25 ?", 24 > 25)
for c in ["ad7cac6", "1b33925", "HEAD"]:
    n = subprocess.run(f"git ls-tree -r --name-only {c} | grep -c '^builds/[^/]*/index.html$'", shell=True, capture_output=True, text=True).stdout.strip()
    print(f"index.html builds at {c}: {n}")
