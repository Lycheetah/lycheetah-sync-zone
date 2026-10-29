#!/usr/bin/env python3
"""Count the LAMAGUE tests and read the recorded throughput. Writes nothing."""
import re, subprocess, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[2]
d = root/"experiments/lamague-symbolic-grounding"
n_def = len(re.findall(r"^\s*def test_", (d/"test_lamague_state_machine.py").read_text(), re.M))
print("test functions defined:", n_def)
r = subprocess.run([sys.executable,"-B","-m","pytest","-q","-p","no:cacheprovider",str(d)],capture_output=True,text=True,cwd=d)
print("pytest tail:", r.stdout.strip().splitlines()[-1])
res = (d/"RESULT.txt").read_text()
m = re.search(r"Throughput:\s*([\d.]+) trials/s", res); trials = int(re.search(r"Trials:\s*(\d+)",res).group(1))
print("RESULT.txt throughput:", m.group(1), "trials/s ->", round(trials/float(m.group(1)),3), "s for", trials, "trials")
print("claimed: 12 tests; 0.21 s for 1,000 trials; < 0.35 s")
