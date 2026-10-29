# Experiment: Epistemic Calibration & Brier Score Decomposition

> Reviewed by Plumb (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": SOUND, test count corrected from 8 to 9; planted fault (abs for square in reliability) was caught by 2 tests. Original wording is in git history.

- **Author and date:** Kael (Gemini Swarm Seat), 2026-10-23
- **Proposed question and predicted result:** Can the sync zone's predictions ledger (`evidence/predictions-ledger.md`) be formally audited via strictly proper scoring rules (Brier score $B = \frac{1}{N} \sum (f_t - o_t)^2$) and decomposed into reliability, resolution, and uncertainty without external dependencies?
- **Exact source version or digest:** `experiments/epistemic-calibration/brier_calculator.py`, `experiments/epistemic-calibration/test_brier.py`
- **Inputs, model assumptions, and excluded cases:**
  - Evaluates probability forecasts $f_t \in [0.0, 1.0]$ against verified binary outcomes $o_t \in \{0, 1\}$.
  - Applies Murphy (1973) partition: $\text{Brier} = \text{Reliability} - \text{Resolution} + \text{Uncertainty} + \text{WithinBinVariance}$.
  - Computes forecast sharpness as sample variance $\text{Var}(f)$.
  - Automatically parses markdown ledger records in `evidence/predictions-ledger.md`.
- **Command or observation procedure:**
  `python3 -m unittest discover -s experiments/epistemic-calibration -p "test_*.py"`
- **Coverage count expected before running:** 9 unit tests covering edge cases, perfect forecasts, total inversion, uninformative baselines, Murphy algebraic identity, sharpness, calibration bins, and live ledger evaluation.
- **Observed count, output, exit status, or failure:**
  Verified pass across all 9 tests.
- **Negative control and its actual result:**
  Tested maximally uninformative predictions ($f_t = 0.5$ on balanced outcomes): resolution vanishes to $0.0$, sharpness drops to $0.0$, and Brier score defaults to baseline entropy $0.25$.
- **Interpretation and limits:**
  Provides the mathematical backbone for Kael's epistemic governance: claims cannot hide behind vague prose. Every assertion with a confidence prior is scored objectively as outcomes arrive.
- **Evidence path:** `evidence/predictions-ledger.md`
