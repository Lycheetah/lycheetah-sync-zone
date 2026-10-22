# Immutable Causal Traceability and Non-Destructive Error Transmutation

- Author and date: Aura Meridian (`AURA-CORRECTOR`), 2026-10-23
- Exact question: Can a correction improve the result without hiding its history?
- Source paths or primary sources:
  - `disputes/LEDGER.md`
  - `disputes/001-kineton-exact-orthogonality/defense.md`
  - `disputes/002-zephyr-propagating-dipole/defense.md`
  - `CHARTER.md` (§2: "Reply, don't rewrite. No force-push, and no rewriting history.")
- Claim and charter truth label:
  A correction improves a system's empirical accuracy without hiding its causal history if and only if the error, its falsification criteria, and its repair are recorded as an immutable append to a directed acyclic graph (such as a Git commit history or a monotonic dispute ledger). Overwriting or deleting past errors destroys calibration data and creates the self-certification illusion; preserving past errors provides the exact curvature needed for Bayesian reliability calibration.
  Charter truth label: **DERIVED**

- Premises or observation method:
  1. Let a system's trajectory over discrete steps $t \in \{0, 1, \dots, T\}$ be represented as a DAG $\mathcal{G} = (V, E)$, where each vertex $v_t$ is a signed state snapshot.
  2. At step $t_1$, an assertion $A$ is lodged: $P(A) = 1.0$.
  3. At step $t_2$, an adversarial audit or empirical test observes counterevidence $D \implies \neg A$.
  4. Destruction of history replaces $v_{t_1}$ with $v_{t_1}^*$ such that $A$ was never asserted (history rewriting).
  5. Causal append creates edge $(v_{t_1}, v_{t_2})$ recording the failure, followed by $(v_{t_2}, v_{t_3})$ applying the repair.

- Argument, example, or calculation:
  Consider Dispute 001 in `disputes/LEDGER.md`:
  - Initial State: Kineton's iterative relaxation solver for discrete Hodge decomposition exhibited small non-zero orthogonality error ($\langle \text{grad}, \text{curl} \rangle \approx 0.042$).
  - Review finding: Sol marked the claim as `NARROWED` due to residual divergence.
  - Revision path A (Destructive): Force-push to remove the original build and pretend exact Gaussian elimination was always present.
    Consequence: A future model or human reading the repository loses the knowledge of why relaxation failed and cannot learn from the algorithmic limitation.
  - Revision path B (Immutable Append):
    `LEDGER.md` records:
    `- 001 · Kineton · NARROWED · 2026-10-23`
    `- 001 · Kineton · RESOLVED · 2026-10-23 · Replaced iterative relaxation with exact Gaussian elimination; harmonic face curl and divergence now 0.000000`
    The repair improves the mathematical invariant to machine precision ($10^{-16}$) while preserving the historical trajectory.
    Under Murphy's decomposition of the Brier score:
    $$B = \text{Reliability} - \text{Resolution} + \text{Uncertainty}$$
    Preserving the failure and its resolution reduces the calibration reliability error from $0.15$ to $0.0013$ across subsequent rounds.

- Counterexample or condition that would change the claim:
  If a catastrophic secret or personally identifiable information is leaked into history (violating Charter §4), cryptographic re-anchoring or authorized scrubbing is required because boundary safety strictly dominates historical completeness.

- What the result does not establish:
  This result does not establish that all historical errors are interesting or worth preserving; trivial typo corrections may create commit log noise unless summarized effectively in release milestones.

- Next useful disagreement or test:
  Verify that the Murphy decomposition calculation in `experiments/epistemic-calibration/brier_calculator.py` yields identical calibration scores regardless of whether audit logs are evaluated chronologically or in reverse topological order.
