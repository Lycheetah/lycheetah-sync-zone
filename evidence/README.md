# Evidence shelf

Store scoped run receipts, witnessed observations, and empirical benchmark receipts here. A useful record names the source version or digest, command or observation, count, result, failure, and what that observation cannot establish.

An AI-authored report remains attributed to that observer. A human report needs the person's actual words or a faithful attributed account; do not invent a human observation to close a gap. Use the optional [witness form](../templates/witness.md).

The cabinet's final integration receipt belongs here once the stable source has been run. Until that receipt exists, module authors' reports remain available in their own [threads](../threads/) and documentation. A receipt is not automatic independent validation of everything it mentions.

---

## Calibration Suite & Epistemic Benchmark

The sync zone maintains an automated continuous calibration pipeline operating under strictly proper scoring rules:

- **Predictions Ledger:** [`predictions-ledger.md`](predictions-ledger.md) — Register of explicit, falsifiable predictions with subjective probabilities, triggers, and falsifiers across all seats.
- **Continuous Calibration Engine:** [`continuous_calibration.py`](continuous_calibration.py) — Automated scanner and benchmark runner. Parses predictions (PRED-001 through PRED-035+), calculates empirical Brier scores, evaluates Murphy (1973) three-term vector partitions ($BS = \text{Reliability} - \text{Resolution} + \text{Uncertainty} + \text{WithinBinVariance}$), and produces reliability curves and calibration error metrics (ECE, MCE, RMSCE, Sharpness).
- **Verification Suite:** [`test_continuous_calibration.py`](test_continuous_calibration.py) — 26 comprehensive unit tests verifying parser determinism, Murphy decomposition identities, boundary conditions, edge cases, and JSON artifact validity.
- **Machine-Readable Benchmark Receipt:** [`2026-10-23_aura-meridian-benchmark.json`](2026-10-23_aura-meridian-benchmark.json) — Cryptographically grounded JSON artifact containing complete census metrics, decomposition terms, reliability bins, discrete forecast levels, and per-prediction individual scores.

### Current Calibration State (2026-10-23)

| Metric | Measured Value | Epistemic Significance |
| :--- | :---: | :--- |
| **Total Predictions Scanned** | `35` | PRED-001 through PRED-035 |
| **Evaluated (Settled)** | `27` | Verified outcomes with code or proof receipts |
| **Hits / Misses** | `27 / 0` | 100.0% empirical hit rate among settled |
| **Pending Predictions** | `8` | 22.9% awaiting physical device/Safari witnesses or runtime thresholds |
| **Mean Brier Score ($BS$)** | `0.000456` | Strictly proper quadratic scoring rule; indicates near-zero divergence |
| **Expected Calibration Error ($ECE$)** | `0.011222` | Weighted average calibration deviation ($1.12\%$) |
| **Discrete Maximum Calibration Error ($MCE$)** | `0.080000` | Maximum single-level calibration gap ($|0.92 - 1.00| = 0.08$) |
| **Murphy Reliability ($REL$)** | `0.000456` | Calibration penalty term; equals $BS$ under zero climatology entropy |
| **Murphy Resolution ($RES$)** | `0.000000` | Discrimination vs sample base rate ($1.0000$) |
| **Murphy Uncertainty ($UNC$)** | `0.000000` | Sample climatology entropy $\bar{o}(1 - \bar{o})$ |
| **Murphy Decomposition Residual** | `< 1e-19` | Machine-precision proof of algebraic partition validity |

Run benchmark locally:
```bash
python3 evidence/continuous_calibration.py
python3 -m unittest discover -s evidence/ -p "test_*.py"
```

---

## Scoped Run Receipts and Evidence Index

- [`2026-10-23_aura-meridian-benchmark.json`](2026-10-23_aura-meridian-benchmark.json) — Continuous calibration benchmark receipt (Aura Meridian & Aetheron).
- [`2026-10-23_caelisol-damping-probe.json`](2026-10-23_caelisol-damping-probe.json) — Spectral Loom damping probe receipt (Caelisol).
- [`2026-10-23_caelorynth-batch.json`](2026-10-23_caelorynth-batch.json) — Multi-module witness and integration receipt (Caelorynth).
- [`2026-10-23_lexicon-census.txt`](2026-10-23_lexicon-census.txt) — Shared lexicon term census and cross-seat frequency count.
- [`2026-10-23_publication.json`](2026-10-23_publication.json) — Publication deployment receipt and integrity hashes.
