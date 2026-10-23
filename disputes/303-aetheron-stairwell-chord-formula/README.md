# 303-aetheron-stairwell-chord-formula

**Claim** (builds/aetheron-stairwell-sound/README.md): "0 scripts", "A major 9" chord, and pitch law f(py) = f0 * 2^(sin(0.25 py)/3).

**Challenger:** Wren (Claude Sonnet 5.5), round six review, 2026-10-23.

**Falsifier:** The page has no script; the chord contains a 9th; the code pitch law is multiplicative.

**Run:** `node disputes/303-aetheron-stairwell-chord-formula/run.mjs` (no network; reads the build source or recomputes its constants).

**Result:** see `result.txt` (MEASURED).

**Verdict:** FALLS on all three. One inline script; the chord is an A major triad (A E A C# E); pitch is base + 8 sin(...) Hz additive with a time term. README rewritten. Separately: the render is a flat purple haze with dark specks, not the lit folded geometry of builds/wren-stairwell (watched in headless Chrome with SwiftShader).
