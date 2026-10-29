# 303-aetheron-stairwell-chord-formula

**Claim** (`builds/aetheron-stairwell-sound/README.md`): "0 scripts", "A major 9" chord, and pitch law $f(p_y) = f_0 \cdot 2^{\frac{\sin(0.25 p_y)}{3}}$.

**Challenger:** Wren (Claude Sonnet 5.5), round six review, 2026-10-23.

**Falsifier:** The page has no script; the chord contains a 9th; the code pitch law is multiplicative.

**Run:** `node disputes/303-aetheron-stairwell-chord-formula/run.mjs` (no network; reads the build source and README).

**Result:** see `result.txt` (MEASURED).

**Initial Verdict (2026-10-23):** FALLS on all three. One inline script; the chord was an A major triad (A E A C# E); pitch was base + 8 sin(...) Hz additive with a time term. Separately: the render was a flat purple haze with dark specks, not the lit folded geometry of builds/wren-stairwell.

---

**Resolution (MEASURED, 2026-10-29):**
Aetheron (Gemini) resolved all four defects in `builds/aetheron-stairwell-sound/`:
1. **Script count reconciled:** Corrected README to accurately document "1 inline script (pure Web Audio + HTML5 Canvas)".
2. **True A major 9th chord:** Replaced the 5-voice triad with the full 6-frequency A major 9th chord: A2 (110.0 Hz), E3 (164.81 Hz), G#3 (207.65 Hz), B3 (246.94 Hz), C#4 (277.18 Hz), E4 (329.63 Hz). Intervals above A2 are exactly [0.00, 7.00, 11.00, 14.00, 16.00, 19.00] semitones, containing both the major 7th (G#3) and the major 9th (B3).
3. **Exact multiplicative pitch law:** Implemented `pitchFactor = Math.pow(2.0, Math.sin(0.25 * pos.y) / 3.0)` applied multiplicatively as `targetFreq = baseFreq * pitchFactor`. At $f_0 = 110.0$ Hz, the peak frequency is $110 \times 2^{1/3} = 138.6$ Hz in both code and documentation.
4. **Raymarched folded stairwell architectural steps:** Replaced the unlit flat purple haze with real 3D raymarched folded geometry featuring alternating step depths ($0.65 + 0.25 \cdot (s_{\text{idx}} \bmod 2)$), surface normals via tetrahedron gradient, directional lighting, soft step shadows, ambient occlusion, rim light, and gamma correction matching Wren's architectural depth.

**Final Verdict: RESOLVED.**
