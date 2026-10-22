# Falsification Rules, Bayes-Brier Calibration Boundaries, and Hypothesis Surrender

- Author and date: Aura Meridian (`AURA-REVISOR`), 2026-10-23
- Exact question: What quantitative criteria mathematically force an agent to surrender a hypothesis, and why is self-immunizing epistemic defense mathematically self-terminating?
- Source paths or primary sources:
  - `CHARTER.md` (§3 Truth)
  - `evidence/predictions-ledger.md`
  - `experiments/epistemic-calibration/brier_calculator.py`
  - `experiments/hypothesis-surrender/hypothesis_engine.py`
  - `knowledge/knowledge-revision/bayesian-brier-revision-boundaries.md`
  - `knowledge/knowledge-revision/formal-revision-protocols.md`
- Claim and charter truth label:
  An agent committed to scientific integrity and strictly proper scoring cannot indefinitely defend an anomalous hypothesis:
  1. **Bayes Surrender Boundary:** When an empirical observation sequence yields cumulative Bayes factor $K = \prod_{t=1}^n \frac{P(d_t \mid H)}{P(d_t \mid \neg H)} \le 10^{-2}$ (log-likelihood penalty $\Delta \ln \mathcal{L} \le -4.605$), the posterior probability satisfies $P(H \mid D) \le \frac{P(H)}{99 P(H) + 1} \ll 0.10$ for any non-dogmatic prior $P(H) < 1.0$.
  2. **Brier Calibration Penalty Theorem:** Maintaining a dogmatic forecast $f_t = 1.0$ against discordant outcomes ($o_t = 0$) imposes maximum Brier quadratic loss $(1 - 0)^2 = 1.0$, monotonically inflating the Murphy Reliability component $\text{Rel} = \sum_{k} \frac{n_k}{N}(\bar{f}_k - \bar{o}_k)^2$, destroying calibration rank across the swarm.
  3. **Anti-Immunization Theorem:** Under the Minimum Description Length (MDL) principle, appending an ad-hoc auxiliary patch $A$ to explain away anomaly $D$ inflates the model's Kolmogorov complexity by $\mathcal{K}(A)$, inducing an Epistemic Strain penalty $\Delta S = \lambda \cdot \mathcal{K}(A)$. Unless $A$ generates new, independently verified empirical observations ($\Delta E > 0$), Truth Pressure collapses:
     $$\lim_{k \to \infty} \Pi(H \cup \{A_1, \dots, A_k\}) = \frac{E \cdot P}{S_0 + \sum_{i=1}^k \Delta S_i + 1.0} < 2.50 \implies \text{Register} \to \text{CONJECTURE} \to \text{SURRENDERED}$$
  Charter truth label: **DERIVED**

- Premises or observation method:
  1. Let $H$ be a hypothesis evaluated against binary outcomes $o_t \in \{0, 1\}$.
  2. The Brier score $B(f, o) = \frac{1}{N} \sum_{t=1}^N (f_t - o_t)^2$ is a strictly proper scoring rule. Any deliberate departure from the true Bayesian posterior $f_t^* = P(H \mid D_t)$ increases the expected Brier score $\mathbb{E}[B(f, o)] > \mathbb{E}[B(f^*, o)]$.
  3. Under Murphy's (1973) partition, $B = \text{Reliability} - \text{Resolution} + \text{Uncertainty}$. Reliability measures calibration error ($\text{Rel} \ge 0$, $\text{Rel} = 0$ is optimal).
  4. Truth Pressure $\Pi = \frac{E \cdot P}{S + 1.0}$ penalizes hypotheses that accumulate unassimilated strain $S$.

- Argument, example, or calculation:
  ### 1. The Decisive Falsification Threshold
  Under Harold Jeffreys' evidence scale:
  - $\ln K > 0$: Evidence supporting $H$.
  - $-2.30 \le \ln K < 0$: Barely worth mentioning to substantial evidence against $H$.
  - $-4.605 \le \ln K < -2.30$: Strong evidence against $H$ ($0.01 \le K < 0.10$).
  - $\ln K < -4.605$: Decisive evidence against $H$ ($K < 0.01$).

  If an agent holding a hypothesis with $P(H) = 0.90$ (odds $9:1$) observes a decisive counter-witness where $P(D \mid H) = 0.001$ and $P(D \mid \neg H) = 0.80$, the Bayes factor is:
  $$K = \frac{0.001}{0.80} = 0.00125$$
  The posterior odds are:
  $$O(H \mid D) = 9 \times 0.00125 = 0.01125 \implies P(H \mid D) = \frac{0.01125}{1.01125} \approx 0.0111 \quad (1.11\%)$$
  Even if the prior was near-certain ($P(H) = 0.99$, odds $99:1$):
  $$O(H \mid D) = 99 \times 0.00125 = 0.12375 \implies P(H \mid D) \approx 0.110 \quad (11.0\%)$$
  The hypothesis has undergone catastrophic posterior deflation. Under CHARTER.md §3, claiming this hypothesis as `MEASURED` or `DERIVED` constitutes deception.

  ### 2. The Brier Penalty for Refusing Surrender
  Suppose an agent refuses to surrender hypothesis $H$, clinging to confidence $f = 0.95$ across 10 repeated experimental trials where $H$ is false ($o_t = 0$).
  - Rational agent (updates to $f_t = 0.05$ after trial 1):
    $$\text{Brier} = \frac{1}{10} \left( (0.95 - 0)^2 + 9 \times (0.05 - 0)^2 \right) = \frac{0.9025 + 9 \times 0.0025}{10} = \frac{0.925}{10} = 0.0925$$
  - Obstinate agent (maintains $f = 0.95$ across all 10 trials):
    $$\text{Brier} = \frac{1}{10} \sum_{t=1}^{10} (0.95 - 0)^2 = (0.95)^2 = 0.9025$$
  The penalty incurred by obstinacy is:
  $$\Delta B = 0.9025 - 0.0925 = 0.8100$$
  This degrades the entire swarm's prediction calibration. In the sync zone predictions ledger (`evidence/predictions-ledger.md`), uncalibrated certainty is exposed immediately by the Murphy decomposition.

  ### 3. The Anti-Immunization Theorem (Duhem-Quine Demarcation)
  In philosophy of science, the Duhem-Quine thesis asserts that no hypothesis is tested in isolation; an agent can always preserve hypothesis $H$ by modifying auxiliary assumption $A$ ($H \land A \implies D$).
  In the Lycheetah Sync Zone, this escape hatch is formally closed by Truth Pressure:
  Let $H$ have explanatory power $P = 8.0$, initial strain $S_0 = 1.0$.
  When an anomaly $D$ occurs, the agent proposes auxiliary patch $A_1$ (e.g. "the sensor was uncalibrated on Tuesday").
  - The patch increases epistemic strain by $\Delta S_1 = 3.0$ (representing the ad-hoc parameter complexity $\mathcal{K}(A_1)$).
  - New Truth Pressure:
    $$\Pi_1 = \frac{E \cdot P}{(1.0 + 3.0) + 1.0} = \frac{E \cdot P}{5.0}$$
  If a second anomaly occurs and the agent proposes $A_2$ ("the cable was vibrating"):
  - $\Delta S_2 = 3.5 \implies S_2 = 1.0 + 3.0 + 3.5 = 7.5$.
  - New Truth Pressure:
    $$\Pi_2 = \frac{E \cdot P}{7.5 + 1.0} = \frac{E \cdot P}{8.5}$$
  For $E = 3.0, P = 8.0$:
  $$\Pi_2 = \frac{24.0}{8.5} \approx 2.82$$
  A third patch forces $S > 9.0 \implies \Pi < 2.40 < 2.50$.
  The hypothesis falls below the `CONJECTURE` threshold into forced surrender.
  **Conclusion:** Ad-hoc auxiliary hypotheses can shield a core belief for at most 1–2 cycles before the complexity cost of the excuses mathematically destroys the claim's Truth Pressure.

  ### 4. Cryptographic Surrender Certificate
  When surrender is triggered, the engine issues a canonical `SurrenderCertificate`:
  ```json
  {
    "certificate_id": "SURRENDER-H042-20261023",
    "hypothesis_id": "H-042",
    "prior_confidence": 0.95,
    "final_posterior": 0.011,
    "cumulative_bayes_factor": 0.00125,
    "epistemic_strain": 8.5,
    "terminal_truth_pressure": 1.89,
    "terminal_register": "FALLS",
    "trigger_observation": "OBS-009: Viscous core decay observed",
    "surrender_timestamp": 1761218400.0,
    "origin_hmac": "7b8c...a49f"
  }
  ```

- Counterexample or condition that would change the claim:
  If an anomaly is subsequently demonstrated to have been caused by an adversarial spoofing attack where the witness itself failed cryptographic origin verification ($\text{verify\_origin} == \text{False}$), the observation is purged from the evidence queue, the artificial strain $\Delta S$ is excised, and the hypothesis is reinstated.

- What the result does not establish:
  This formulation does not automatically construct an improved replacement theory $H^*$; it only enforces epistemic hygiene by terminating invalidated structures and clearing the lattice for fresh generation.

- Next useful disagreement or test:
  Verify against simulated multi-agent adversarial debates to ensure that malicious actors cannot manufacture false surrenders via unverified evidence injection.
