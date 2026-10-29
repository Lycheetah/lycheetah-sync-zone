#!/usr/bin/env python3
"""Count the syllables named in the claim vs the ratios it maps them to. Writes nothing."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
l = [x for x in (root/"knowledge/language-and-symbols/sacred-tonecode-phonology.md").read_text().splitlines() if x.startswith("  - **DERIVED:** The 7 canonical")][0]
names = re.findall(r"`([^`]+)`", l.split("mapped")[0]); ratios = re.search(r"\[([^\]]+)\]", l).group(1).split(",")
print("syllables named:", len(names), names); print("ratios listed:", len(ratios), [r.strip().strip("$") for r in ratios])
