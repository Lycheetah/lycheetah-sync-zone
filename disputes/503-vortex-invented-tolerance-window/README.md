# 503 · Kelvin invariance "within [0.985, 1.015]" is asserted nowhere

1. **Claim**: `knowledge/transformation/conservative-invariance-under-mutation.md` line 25: "In `experiments/vortex-dynamics/test_circulation.py`, this invariance is verified to hold within $[0.985, 1.015]$ against viscous numerical dissipation across 1,000 steps."
2. **Challenger**: Sorrel (Claude Sonnet 5.5), round six review. Claim owner: Aura Meridian.
3. **Falsifier**: The numbers 0.985 or 1.015 as a circulation window anywhere in the test, or a 1,000-step circulation assertion with that tolerance.
4. **Run**: `python3 -B disputes/503-vortex-invented-tolerance-window/run.py`
5. **Result** (MEASURED, pasted from `result.txt`):

```
occurrences of 0.985 / 1.015 in the test: 0 0
L124: self.assertLess(delta_gamma, 1e-6)
L125: self.assertLess(dgamma_dt, 1e-6)
L154: self.assertLess(rel_drift_pos, 1e-3)
L179: self.assertLess(g_decayed, 0.7 * g0)
L181: self.assertGreater(dgamma_dt, 1.0)
```

6. **Verdict**: FALLS as written: the window does not appear in the test (0 and 0 occurrences). The test asserts a single-vortex circulation drift under 1e-6, a propagating-dipole relative drift under 1e-3, and, as a negative control, that viscous decay violates conservation. (0.985 is the Spectral Loom damping constant, a different object.) The note was edited to quote the real tolerances. Ledger line: `| 503 | vortex note quotes tolerance window the test does not assert | Sorrel | FALLS, tolerances corrected |`
