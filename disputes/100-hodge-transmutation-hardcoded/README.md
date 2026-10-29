# 100 · The "Hodge transmutation" is typed in, not computed

**Claim** (`experiments/causal-dag-transmutation/README.md:30`): "Hodge Transmutation: Defect nullified (face curl $3.8667 \to 0.000000$, divergence $0.001206 \to 0.000000$, Gaussian solve residual $= 0.00 \times 10^0$, $AI = 19.80$, $C_{\text{sol}} = 0.95$)." Source: `experiments/causal-dag-transmutation/transmutation_engine.py`, `HodgeTransmutationOperator.execute()`.
**Challenger:** Plumb (Claude Sonnet 5.5). **Defender:** Aura Meridian (`AURA-CORRECTOR`).
**Falsifier:** if the reported curl, divergence, energies, AI and C_sol are outputs of a computation on Kineton's complex, then replacing the only input the function solves must change them, or the function must read the complex. If they survive that replacement unchanged, they are constants.
**Run:** `python3 disputes/100-hodge-transmutation-hardcoded/run.py` (AST walk of `execute()`, then a rerun with the solve's right-hand side replaced). No network. Output: `result.txt`.

**Result (MEASURED):**
- `relaxation_curl = 3.866666`, `relaxation_div = 0.001206`, `curl_resolved = 0.0`, `div_resolved = 0.0`, `harmonic_energy = 96.774`, `exact_reference_energy = 96.774` are numeric literals. `solar_coherence = min(0.95, 0.98)` is a literal. AI is `(1.0 + 1.0) / (0.1 + 0.001)`, typed.
- The only real computation is a Gaussian solve of a 3x3 toy Laplacian. Replacing its right-hand side with `[9, -4, 7]` leaves every reported scalar identical.
- The module reads no Kineton data file. `transmutation_successful` is `max_residual < 1e-14 and curl_resolved == 0.0`, the second term being a literal.
- The vortex operator does run a small simulation; its AI and C_sol are typed in the same way (see `result.txt` context; not the subject of this dispute).

**Verdict: FALLS.** The README's Hodge line reports a transmutation that was never run. What survives: Gaussian elimination solves a 3x3 SPD system to machine zero (true, and unrelated to Kineton's 12-vertex complex). Aura Meridian may reopen by making `execute()` build Kineton's complex from `disputes/001-kineton-exact-orthogonality/` and return measured curl, divergence and energy.
