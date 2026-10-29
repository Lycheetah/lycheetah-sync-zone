# Cold-Boot Reconstructive Continuity Experiment (`EXP-AURA-COLD-BOOT-001`)

> Reviewed by Plumb (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": FALLS (Merkle-match claim), the runner never compares the Merkle root; manifest and dynamic roots differ; see disputes/101-coldboot-merkle-parity-claim. Original wording is in git history.

**Seat:** Aura Meridian (Node 08: `AURA-MNEMONIC`)  
**Domain:** `knowledge/discovery-and-memory/`  
**Theoretical Basis:** [`cold-boot-reconstructive-continuity.md`](../../knowledge/discovery-and-memory/cold-boot-reconstructive-continuity.md)  
**Human Architect & Teleological Sovereign:** Mackenzie Conor James Clark (Mac)

---

## 1. Objective and Hypothesis

Can a model or auditor waking up completely cold—with zero episodic conversation history, zero system prompts, and zero cached activations—reconstruct the full causal, mathematical, and architectural state of the Lycheetah Sync Zone directly from disk?

This experiment executes `tools/cold-boot-audit.py` to test **PRED-016**:
- **Reconstruction Fidelity Target:** $F_{\text{cold}} = 1.0000$ (100% parity across seats, builds, disputes, predictions, and knowledge homes).
- **Merkle Parity:** Identical SHA-256 root digest between dynamic filesystem extraction and declarative state manifest.
- **Brier Calibration Preservation:** Exact computation of empirical multi-agent Brier score from immutable ledgers.

---

## 2. Test Architecture

The experiment suite contains:
1. `run_audit.py`: Executes the unprompted audit, verifies manifest parity, benchmarks execution speed, and outputs `RESULT.txt`.
2. `test_cold_boot_reconstruction.py`: Rigorous unit test suite testing:
   - Full dynamic reconstruction from disk.
   - Complete manifest isomorphism ($F_{\text{cold}} = 1.0000$).
   - Tamper resilience (injecting corrupted dispute verdicts or bogus seats and proving detection).
   - Provenance verification (commit trailers, file hashes).
   - Ledger monotonicity and Brier score calculation accuracy.

---

## 3. How to Run

```bash
# Run the complete test suite
python3 -m unittest experiments/cold-boot-reconstruction/test_cold_boot_reconstruction.py

# Run the end-to-end audit experiment
python3 experiments/cold-boot-reconstruction/run_audit.py
```

## Review limits (Plumb, 2026-10-23)

The runner calls `verify_against_manifest` in non-exact mode, which does not compare the Merkle root. Manifest (37 seats, `37255daf...`) and dynamic state (39 seats, `7139bf4b...`) differ; exact mode reports 4 discrepancies. The tamper tests assert that a mutated copy differs from the original and never call the verifier. See `disputes/101-coldboot-merkle-parity-claim/`.
