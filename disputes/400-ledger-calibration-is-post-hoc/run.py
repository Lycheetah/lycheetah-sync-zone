#!/usr/bin/env python3
"""Dispute 400: is the predictions ledger 'calibrated' by a real forecast-then-outcome process?
Reads the ledger, recomputes Brier from it, and checks the git record for any commit in which a
settled prediction existed BEFORE its result. No network. Run from the repo root."""
import re, subprocess
L = "evidence/predictions-ledger.md"
def preds(text):
    out = {}
    for b in re.split(r"\n(?=### PRED-)", text)[1:]:
        i = re.search(r"PRED-\d+", b).group()
        c = float(re.search(r"Confidence:\*\*\s*([\d.]+)", b).group(1))
        s = re.search(r"Status:\*\*\s*(\w+)", b).group(1)
        out[i] = (c, s)
    return out
now = preds(open(L).read())
settled = {k: v for k, v in now.items() if v[1] in ("HIT", "MISSED")}
brier = sum((c - (1.0 if s == "HIT" else 0.0)) ** 2 for c, s in settled.values()) / len(settled)
print(f"predictions: {len(now)}  settled: {len(settled)}  misses: {sum(1 for v in settled.values() if v[1]=='MISSED')}")
print(f"recomputed Brier over settled: {brier:.6f}  (arithmetic is correct)")
print(f"settled with confidence >= 0.95: {sum(1 for c,_ in settled.values() if c>=0.95)} of {len(settled)}")
revs = subprocess.run(["git", "log", "--format=%h", "--", L], capture_output=True, text=True).stdout.split()
print("commits touching the ledger:", len(revs))
pre = 0
for r in revs:
    t = subprocess.run(["git", "show", f"{r}:{L}"], capture_output=True, text=True).stdout
    p = preds(t)
    pend = {k for k, v in p.items() if v[1] == "PENDING"}
    # a prediction that appears PENDING in some commit and later HIT would be a real forecast
    for k in pend:
        if k in now and now[k][1] in ("HIT", "MISSED"):
            pre += 1
            print("  forecast-then-settle:", k)
print(f"predictions committed PENDING and later settled: {pre}")
print("settled predictions first committed already carrying their HIT: ", len(settled) - pre)
