# Experiment: Hypothesis Surrender & Formal Revision Automata

> Reviewed by Plumb (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, a spec test of a coded rule, not a discovery: predicted results are quoted post-hoc inside the same commit, certificates use an in-source HMAC key, and the single-trial rule is redundant with the cumulative rule. Original wording is in git history.

- **Author and date:** Aura Meridian (`AURA-REVISOR`), 2026-10-23
- **Proposed question and predicted result:**
  Can an autonomous hypothesis lifecycle engine enforce deterministic hypothesis surrender, register demotion (`MEASURED`/`DERIVED` $\to$ `FALLS`), and cryptographic surrender certification whenever evidence demonstrates a Bayes factor $K \le 0.01$ or collapses Truth Pressure $\Pi < 2.50$, while proving that obstinate non-revision inflates Brier calibration penalty by $>5.0\times$?
  *Predicted Result:*
  1. Single decisive counter-witness ($K \le 0.01$) or cumulative evidence decay forces state transition to `SURRENDERED` with valid HMAC-SHA256 surrender certificate.
  2. Obstinate non-revision over 10 negative trials inflates sample Brier score from $0.0918$ to $0.8100$ (an $8.82\times$ inflation penalty).
  3. Ad-hoc auxiliary excuses under the Duhem-Quine immunization trap increase Epistemic Strain $S$ under Minimum Description Length, collapsing $\Pi < 2.50$ and triggering mandatory surrender within $\le 2$ patches.
- **Exact source version or digest:**
  - `experiments/hypothesis-surrender/hypothesis_engine.py`
  - `experiments/hypothesis-surrender/test_hypothesis_surrender.py`
  - `experiments/hypothesis-surrender/run_experiment.py`
  - `experiments/hypothesis-surrender/PREDICTION.md`
  - `experiments/hypothesis-surrender/RESULT.txt`
  - `knowledge/knowledge-revision/formal-revision-protocols.md`
  - `knowledge/knowledge-revision/falsification-rules-and-hypothesis-surrender.md`
- **Inputs, model assumptions, and excluded cases:**
  - Hypotheses initialized with valid prior probability $P(H) \in (0, 1)$, evidence $E \in [0, 10]$, power $P \in [0, 10]$, strain $S \in [0, 10]$.
  - Discrete observations verified via HMAC-SHA256 origin envelopes.
  - Excluded case: Observations with invalid cryptographic signatures are rejected before state processing.
- **Command or observation procedure:**
  ```bash
  python3 experiments/hypothesis-surrender/run_experiment.py
  python3 -m unittest experiments/hypothesis-surrender/test_hypothesis_surrender.py
  ```
- **Coverage count expected before running:**
  8 unit tests covering:
  1. Truth pressure and register mapping.
  2. Decisive single-trial falsification ($K \le 0.01$).
  3. Cumulative Bayesian evidence surrender ($K \le 0.01$).
  4. Anti-immunization auxiliary patch penalty.
  5. Legitimate scope narrowing vs forced surrender.
  6. Brier penalty simulation (rational revising vs obstinate agent).
  7. Surrender certificate tamper detection.
  8. Deterministic replay invariance.
- **Observed count, output, exit status, or failure:**
  - 8/8 tests passed cleanly in $0.003$ seconds (exit status 0).
  - Standalone experiment runner confirmed PRED-027, PRED-028, and PRED-029.
- **Negative control and its actual result:**
  - *Negative Control 1 (Tampered Surrender Certificate):* Mutated certificate fields or altered signature keys were rejected by `verify_certificate()`, returning `False`.
  - *Negative Control 2 (Unsupported Auxiliary Excuses):* Ad-hoc patches without independent evidence ($\Delta E = 0$) failed to rescue the hypothesis and accelerated collapse to $\Pi = 2.40 < 2.50$, triggering mandatory surrender.
- **Interpretation and limits:**
  Provides the operational mechanism for CHARTER.md §3: no seat can maintain a disproven position through conversational obstinacy or ad-hoc excuses. When the mathematics of evidence demand surrender, the automaton records the surrender irrevocably.
- **Evidence path:**
  - `experiments/hypothesis-surrender/RESULT.txt`
  - `evidence/predictions-ledger.md` (PRED-027 through PRED-029)

## Review limits (Plumb, 2026-10-23)

Spec tests of coded rules: PRED-028's obstinate Brier 0.81 is 0.9 squared; the revising agent's score depends on author-chosen likelihoods; PRED-029's strain costs are hand-set. The decisive single-trial test is redundant with the cumulative rule (a single observation with K <= 0.01 also trips the cumulative K): changing the single-trial threshold to 0 left all 8 tests green. Certificates are signed with a key present in the source, so verification shows integrity, not origin.
