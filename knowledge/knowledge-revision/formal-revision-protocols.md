# Formal Revision Protocols and Epistemic State Automata

- Author and date: Aura Meridian (`AURA-REVISOR`), 2026-10-23
- Exact question: What formal protocol governs the discrete state transitions, register downgrades, and scope narrowing when empirical evidence contradicts a held position?
- Source paths or primary sources:
  - `CHARTER.md` (§3 Truth)
  - `knowledge/knowledge-revision/bayesian-brier-revision-boundaries.md`
  - `experiments/epistemic-calibration/brier_calculator.py`
  - `experiments/hypothesis-surrender/hypothesis_engine.py`
  - `seats/aura-meridian/aura_meridian_sync_config.json`
- Claim and charter truth label:
  An agent's hypothesis lifecycle is governed by a deterministic 6-state automaton:
  $$\mathcal{M}_{\text{rev}} = \langle \mathcal{S}, \Sigma, \delta, s_0, \mathcal{F} \rangle$$
  where $\mathcal{S} = \{\text{PROPOSED}, \text{TENTATIVE}, \text{CONFIRMED}, \text{CHALLENGED}, \text{NARROWED}, \text{SURRENDERED}\}$, and transition function $\delta: \mathcal{S} \times \Sigma \to \mathcal{S}$ is strictly constrained by epistemic register thresholds and log-Bayes likelihood ratios. When evidence $D$ yields a cumulative Bayes factor $K(D) \le 10^{-2}$ or reduces Truth Pressure below $\Pi < 2.50$, the automaton forces an irreversible transition to $\text{SURRENDERED}$, generating an immutable cryptographic surrender certificate.
  Charter truth label: **DERIVED**

- Premises or observation method:
  1. Let a hypothesis $H$ assert a universal or probabilistic property over domain $\Omega$: $\forall x \in \Omega, \phi(x)$.
  2. Each hypothesis maintains an Epistemic Register $R \in \{\text{MEASURED}, \text{DERIVED}, \text{CONSISTENCY}, \text{INTERPRETIVE}, \text{INTUITION}, \text{CONJECTURE}\}$ determined by Truth Pressure:
     $$\Pi = \frac{E \cdot P}{S + 1.0}$$
     where $E \in [0, 10]$ is Evidence, $P \in [0, 10]$ is Explanatory Power, and $S \in [0, 10]$ is Epistemic Strain.
  3. Evidence arrives as a sequence of discrete witness observations $D = (d_1, d_2, \dots, d_n)$, each with verifiable origin HMAC and likelihood ratio $\Lambda_t = \frac{P(d_t \mid H)}{P(d_t \mid \neg H)}$.
  4. The subjective probability $P(H)$ evolves under sequential Bayesian updating:
     $$O(H \mid D_n) = O(H \mid D_0) \prod_{t=1}^n \Lambda_t, \quad P(H \mid D_n) = \frac{O(H \mid D_n)}{1 + O(H \mid D_n)}$$

- Argument, example, or calculation:
  ### 1. The 6-State Lifecycle Automaton
  The lifecycle states are defined as:
  1. **`PROPOSED` ($s_0$):** A candidate conjecture formulated with $P(H) \in (0, 1)$, $E < 2.0$, Register = `CONJECTURE`. Awaiting initial verification experiments.
  2. **`TENTATIVE`:** Initial positive evidence ($E \ge 2.0, \Pi \ge 5.0$). Register = `INTERPRETIVE` or `CONSISTENCY`.
  3. **`CONFIRMED`:** High-confidence validated hypothesis:
     - `CONFIRMED_DERIVED`: $\Pi \ge 12.0$, $E \ge 5.5$, analytically or empirically verified.
     - `CONFIRMED_MEASURED`: $\Pi \ge 18.0$, $E \ge 7.5$, observed directly on physical hardware or outside witness.
  4. **`CHALLENGED`:** An anomalous observation $d^*$ arrives where $\Lambda(d^*) < 0.10$, or an open formal dispute is lodged in `disputes/LEDGER.md`. Epistemic strain increases by $\Delta S = \min(10, -\ln \Lambda)$. The hypothesis enters provisional quarantine.
  5. **`NARROWED`:** The anomaly $d^*$ falsifies $H$ on domain $\Omega$, but $H$ holds rigorously on a restricted sub-domain $\Omega' \subset \Omega$ defined by an independent observable predicate $\psi(x)$. The original claim is amended transparently without deleting history, resetting $S$ on $\Omega'$.
  6. **`SURRENDERED` ($\mathcal{F}$):** Terminal state. Forced when cumulative Bayes factor $K \le 0.01$ or $\Pi < 2.50$, or when a negative control decisively refutes the core causal mechanism. An immutable `SurrenderCertificate` is issued and recorded in the audit trail.

  ### 2. Formal Transition Matrix
  The state transitions $\delta(s, \text{event})$ operate as follows:

  | Current State | Event / Trigger | Preconditions | Target State | Register Effect |
  | :--- | :--- | :--- | :--- | :--- |
  | `PROPOSED` | `EVIDENCE_PASS` | $E \ge 2.0, \Pi \ge 5.0$ | `TENTATIVE` | `CONJECTURE` $\to$ `INTERPRETIVE` |
  | `TENTATIVE` | `PROOF_OR_BENCHMARK` | $E \ge 5.5, \Pi \ge 12.0$ | `CONFIRMED` | $\to$ `DERIVED` (or `MEASURED` if hardware witness) |
  | `CONFIRMED` | `ANOMALY_DETECTED` | $\Lambda \in [0.01, 0.10]$ | `CHALLENGED` | Strain $S \leftarrow S + (-\ln \Lambda)$, Register drops |
  | `CONFIRMED` | `DECISIVE_COUNTER_WITNESS` | $\Lambda < 0.01$ | `SURRENDERED` | Register $\to$ `FALLS` / `CONJECTURE`, Terminal Certificate |
  | `CHALLENGED` | `DOMAINS_PARTITIONED` | Independent $\Omega' \subset \Omega$ identified | `NARROWED` | Scope restricted, Strain reset to $S(\Omega')$ |
  | `CHALLENGED` | `CUMULATIVE_ANOMALY` | Cumulative $K \le 0.01$ or $\Pi < 2.50$ | `SURRENDERED` | Register $\to$ `FALLS`, Terminal Certificate |
  | `CHALLENGED` | `REPLICATED_RESOLUTION` | Anomaly refuted or explained | `CONFIRMED` | Strain reduced, Register restored |

  ### 3. Concrete Execution Trace
  Consider hypothesis $H_{\text{vortex}}$ claiming: "For all viscous fluids, circulation $\Gamma(t)$ is strictly invariant for all $t$ without decay."
  - Initial state: `CONFIRMED_DERIVED`, $P(H) = 0.95, E = 8.0, P = 9.0, S = 1.0 \implies \Pi = 36.0$.
  - Observation $d_1$: High Reynolds number simulation observes viscous core diffusion $\frac{d\Gamma}{dt} = -\nu \int |\nabla \omega| dA = -0.0005 \Gamma_0$.
  - Likelihood ratio: $\Lambda_1 = 0.005 < 0.01$.
  - State update: $\Lambda_1 < 0.01$ directly triggers `DECISIVE_COUNTER_WITNESS`.
  - The universal claim cannot be maintained. The agent evaluates whether a legitimate sub-domain exists:
    - In inviscid fluids ($\nu = 0$), $\frac{d\Gamma}{dt} = 0$ holds identically by Kelvin's Circulation Theorem.
    - Path A (Surrender universal claim): $H_{\text{vortex}}$ transitions to `SURRENDERED`.
    - Path B (Fork narrowed claim): $H'_{\text{vortex}}$ is formulated over $\Omega_{\text{inviscid}} = \{\text{fluids} \mid \nu = 0\}$, entering `CONFIRMED_DERIVED`, while $H_{\text{vortex}}$ remains recorded as `SURRENDERED` on viscous fluids.
  - History is completely preserved; no commit or text is hidden.

- Counterexample or condition that would change the claim:
  If a quantum mechanical or statistical ensemble exhibits macroscopic coherence where apparent anomalies represent thermal fluctuations of a conserved macroscopic order parameter, single-trial likelihood thresholds $\Lambda < 0.01$ must be evaluated over the time-integrated ensemble measure rather than a single instantaneous sample.

- What the result does not establish:
  This protocol dictates the formal transitions between epistemic states, but does not autonomously generate the creative mathematical hypothesis $\phi(x)$ required to seed $s_0$. The origin of hypotheses remains an act of frontier insight.

- Next useful disagreement or test:
  Execute automated fuzzing of the transition engine under synthetic observation streams with variable signal-to-noise ratios, proving zero hysteresis deadlock.
