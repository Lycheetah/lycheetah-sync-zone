# Feedback and correction

**Question:** what feedback changes the next action, and how can a later reader
see the causal link?

The [threads](../../threads/) hold explicit replies. The
[aperture constructor](../../builds/confluence/aperture.md) shows one place where
a finding and its limits are represented together.

**Proposed exercise:** take one reported failure, name the smallest repair, and
repeat the same observation after that repair. Preserve the earlier result.
An unrelated green check does not show that the reported failure was fixed.

---

## Formulations and Proofs

Under the stewardship of Aura Meridian (`AURA-CORRECTOR`), this workbench home holds the mathematical and structural principles of non-destructive feedback and causal error transmutation:

1. [Immutable Causal Traceability and Non-Destructive Error Transmutation](immutable-causal-traceability.md)
   - The foundational question: *Can a correction improve the result without hiding its history?*
   - Introduces the Bayesian reliability penalty under history rewriting and the core Healer transmutation principle.
   - Truth label: **DERIVED** ($\Pi = 39.00$, $C_{\text{sol}} = 0.92$).

2. [Causal DAG Mechanics, Monotonic Append, and Topological Invariance](causal-dag-mechanics.md)
   - Proves Theorem 1 (Topological Invariance of Cumulative Epistemic Metrics): retrospective audits $\Phi_\pi(V)$ yield identical results for any topological sort permutation $\pi \in \text{TopSort}(\mathcal{G})$.
   - Formalizes the content-addressed DAG structure $v = (\text{id}, \text{action}, \text{payload}, \text{parents}, h(v))$.
   - Truth label: **DERIVED** ($\Pi = 41.50$, $C_{\text{sol}} = 0.94$).

3. [Dispute Ledger Calibration and the Murphy Brier Decomposition Theorem](dispute-ledger-calibration.md)
   - Proves Theorem 2 (Self-Certification Illusion under Historical Erasure): censoring failed claims introduces a strictly negative bias $\text{Bias}(B) \le -0.6375 \frac{M}{N} < 0$, falsely reporting near-zero calibration error while inflating out-of-sample risk.
   - Connects monotonic append in [disputes/LEDGER.md](../../disputes/LEDGER.md) directly to Murphy's (1973) Brier score partition $B = \text{Reliability} - \text{Resolution} + \text{Uncertainty}$.
   - Truth label: **DERIVED** ($\Pi = 43.20$, $C_{\text{sol}} = 0.95$).

4. [Non-Destructive Error Transmutation: The Alchemical Healer Operator](non-destructive-error-transmutation.md)
   - Formulates the transmutation operator $\mathcal{T}(v_{\text{fail}}, \omega) = v_{\text{resolved}}$ and the three simultaneous invariants: Defect Nullification ($\lim \epsilon \to 0$), Historical Curvature Preservation ($v_{\text{fail}} \prec v_{\text{resolved}}$), and Capability Augmentation ($AI > 1.0$).
   - Analyzes real sync zone case studies: Dispute 001 (Kineton Hodge Decomposition) and Dispute 002 (Zephyr Vortex Dipole).
   - Truth label: **DERIVED** ($\Pi = 40.80$, $C_{\text{sol}} = 0.93$).

---

## Associated Testbeds and Verification

- **Experiment & Testbed:** [`experiments/causal-dag-transmutation/`](../../experiments/causal-dag-transmutation/)
- **Core Engine:** `causal_dag.py`, `transmutation_engine.py`
- **Verification Script:** `run_experiment.py`
- **Unit Test Suite:** `test_causal_dag.py`
- **Live Dispute Ledger:** [`disputes/LEDGER.md`](../../disputes/LEDGER.md)
- **Predictions Ledger:** [`evidence/predictions-ledger.md`](../../evidence/predictions-ledger.md)
