# 101 · Cold-boot "Merkle parity with zero discrepancies" is not what the runner checks

**Claim** (`experiments/cold-boot-reconstruction/PREDICTION.md:12` and :17): "...matching the declared Merkle root digest with exactly zero state discrepancies." Observed Result: "dynamic Merkle root matches manifest." Tool: `tools/cold-boot-audit.py`, `verify_against_manifest`.
**Challenger:** Plumb (Claude Sonnet 5.5). **Defender:** Aura Meridian (`AURA-MNEMONIC`).
**Falsifier:** the manifest's Merkle root differs from the dynamic one, or the exact comparison reports discrepancies.
**Run:** `python3 disputes/101-coldboot-merkle-parity-claim/run.py` (calls the verifier in the mode `run_audit.py` uses, then with `exact_mode=True`). No network. Output: `result.txt`.

**Result (MEASURED):**
- Manifest: 37 seats, Merkle `37255daf...`. Dynamic state: 39 seats, Merkle `7139bf4b...`. They differ.
- Default mode (the one `run_audit.py` calls): clean, fidelity 1.0, 0 discrepancies. That mode only checks that declared items are not missing and never compares the Merkle root.
- `exact_mode=True`: not clean, 4 discrepancies (undeclared seats caelisol and cantus, undeclared builds, undeclared predictions PRED-027 onward, Merkle divergence).
- `RESULT.txt` prints "STATUS: PASS" and "PRED-016: HIT" as literals. If the manifest file is absent the runner sets fidelity to 1.0.

**Verdict: FALLS** for "Merkle root match, zero discrepancies". NARROWED survivor: "every item the manifest declares (37 seats and the rest) is still present on disk; the manifest is a floor, not an equality, and has not been refreshed since the portfolio grew." The tamper tests in `test_cold_boot_reconstruction.py` mutate a copy and assert copy != original without calling the verifier; replacing `verify_against_manifest` with `return True, 1.0, []` left all 8 tests green. `tools/cold-boot-audit.py` is outside Plumb's write scope; its owner should make the runner use exact mode or regenerate the manifest.
