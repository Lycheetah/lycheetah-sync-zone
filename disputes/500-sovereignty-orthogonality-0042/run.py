#!/usr/bin/env python3
"""Does any file in the zone record an orthogonality error of 0.042 for dispute 001?
Reads only; runs node on the dispute-001 script (which writes nothing)."""
import subprocess, re, pathlib, json
root = pathlib.Path(__file__).resolve().parents[2]
hits = []
for p in root.rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.suffix in {".png",".jpg",".wav",".mp4"}: continue
    if "500-sovereignty" in str(p) or "knowledge/agency-and-choice/sovereignty" in str(p): continue
    try: t = p.read_text(errors="ignore")
    except Exception: continue
    for i, l in enumerate(t.splitlines(), 1):
        if re.search(r"(?<![\d.])0\.042(?!\d)", l) and re.search(r"ortho|grad|curl|inner", l, re.I):
            hits.append(f"{p.relative_to(root)}:{i}")
print("files (outside the claim) pairing 0.042 with orthogonality/grad/curl:", hits or "NONE")
out = subprocess.run(["node", str(root/"disputes/001-kineton-exact-orthogonality/run.mjs")], capture_output=True, text=True, cwd=root).stdout
shown = re.findall(r'"shownOrtho":"([\d.]+)"', out)
print("shownOrtho values printed by the ORIGINAL (pre-fix) dispute-001 script states:", shown)
print("max shownOrtho:", max(map(float, shown)) if shown else "no output")
