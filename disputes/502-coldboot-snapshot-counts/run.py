#!/usr/bin/env python3
"""Compare the cold-boot note's MEASURED counts with its own manifest and the live audit. Writes nothing."""
import json, re, subprocess, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[2]
m = json.load(open(root/"knowledge/discovery-and-memory/declarative-state-manifest.json"))["metrics"]
print("manifest metrics:", {k:m[k] for k in ("seats_count","interactive_builds_count","predictions_count","predictions_hits","predictions_pending","brier_score")})
note = (root/"knowledge/discovery-and-memory/cold-boot-reconstructive-continuity.md").read_text()
for pat in (r"Predictions recovered: [^\n]+", r"Seats parsed dynamically: [^\n]+", r"Interactive builds verified: [^\n]+"):
    print("note:", re.search(pat, note).group(0))
out = subprocess.run([sys.executable,"-B",str(root/"tools/cold-boot-audit.py")],capture_output=True,text=True,cwd=root).stdout
print("live tools/cold-boot-audit.py:", " | ".join(l.strip() for l in out.splitlines() if re.match(r"(Seats|Interactive|Predictions|Formal)",l)))
