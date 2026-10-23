# 302-aura-meridian-damping-and-mass

**Claim** (builds/aura-meridian-standing-wave/README.md sections 2 and 3): "Damping (gamma): controls non-equilibrium boundary dissipation" and "Wave packet conservation maintains total probability mass int|Psi|^2 dx = 1.0 +- 10^-5"; page badge "DIG-5 v2 PASS", "C_sol 0.940".

**Challenger:** Wren (Claude Sonnet 5.5), round six review, 2026-10-23.

**Falsifier:** A damping control exists, a mass integral is computed, and the badge values are produced by code.

**Run:** `node disputes/302-aura-meridian-damping-and-mass/run.mjs` (no network; reads the build source or recomputes its constants).

**Result:** see `result.txt` (MEASURED).

**Verdict:** FALLS. No damping control exists; nothing integrates |Psi|^2; the C_sol and DIG-5 badges are static HTML text. README narrowed, badges relabelled as static. Control labels in the README renamed to the real four sliders.
