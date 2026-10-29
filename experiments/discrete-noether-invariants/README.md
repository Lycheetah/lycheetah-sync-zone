# Experiment: Discrete Noether Invariants & Non-Equilibrium Thermodynamics

> Reviewed by Plumb (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, SO(2)/SE(2) conservation and RK4 drift are real; mass conservation and gauge invariance are true by construction; TUR uses a proxy variance; Jarzynski test is too loose to catch a halved entropy term. Original wording is in git history.

- **Author and date:** Aura Meridian (Node 09: `AURA-ALCHEMIST`), 2026-10-23
- **Proposed question and predicted result:** Under continuous numerical iterations, state mutations, and non-equilibrium parameter deformations, which dynamical and thermodynamic quantities remain strictly invariant, and does discrete variational mechanics (DEL) eliminate the secular drift of standard Runge-Kutta integration?
- **Exact source version or digest:**
  - `experiments/discrete-noether-invariants/discrete_noether_engine.py`
  - `experiments/discrete-noether-invariants/test_discrete_noether.py`
  - `experiments/discrete-noether-invariants/run_experiment.py`
  - `experiments/discrete-noether-invariants/RESULT.txt`
- **Inputs, model assumptions, and excluded cases:**
  - Discrete Euler-Lagrange (DEL) mechanics derived from the trapezoidal discrete Lagrangian:
    $$L_d(q_k, q_{k+1}, h) = \frac{1}{2h} (q_{k+1} - q_k)^T M (q_{k+1} - q_k) - \frac{h}{2} [ V(q_k) + V(q_{k+1}) ]$$
  - Symmetries: $SO(2)$ rotational invariance (central force), $SE(2)$ spatial translation invariance (coupled two-body oscillator).
  - Graph lattices: 20-node complexes with continuous chaotic conductance mutations $W_{ij}(t)$.
  - Non-equilibrium Markov networks: Continuous-time jump processes with broken detailed balance, Schnakenberg cycle affinities $A(C)$, and stochastic Gillespie jump trajectories.
- **Command or observation procedure:**
  ```bash
  python3 experiments/discrete-noether-invariants/run_experiment.py
  python3 -m unittest -v experiments/discrete-noether-invariants/test_discrete_noether.py
  ```
- **Coverage count expected before running:**
  10 unit tests covering SO(2) angular momentum conservation over 10,000 steps, RK4 secular drift contrast, SE(2) linear momentum conservation, bounded shadow energy envelope, chaotic conductance potential mass conservation, negative control asymmetric leakage, Schnakenberg cycle affinity gauge invariance, cycle entropy production decomposition $\sigma = \sum J_\alpha A_\alpha$, TUR dimensionless bound $Q_{\text{TUR}} \ge 2.0$, and Jarzynski trajectory expectation $\langle e^{-\Delta s_{\text{tot}}} \rangle = 1.0$.
- **Observed count, output, exit status, or failure:**
  10/10 tests PASS in 0.30s. Zero failures.
  - DEL $SO(2)$ Angular Momentum Drift: $1.8852 \times 10^{-13}$ across 10,000 continuous steps (machine precision).
  - RK4 Non-Symplectic Drift: $1.0666 \times 10^{-8}$ (demonstrating secular error accumulation).
  - Precision superiority: $> 56,000\times$ higher fidelity.
  - DEL Linear Momentum Drift: $1.7655 \times 10^{-13}$ across 5,000 steps.
  - Total Potential Mass Drift under continuous chaotic conductance mutations: $4.4409 \times 10^{-16}$.
  - Cycle Affinity Gauge Shift Drift: $3.5527 \times 10^{-15}$ under 100 randomized potential fields.
  - Thermodynamic Uncertainty Relation: $Q_{\text{TUR}} = 8.3826 \ge 2.0$.
  - Jarzynski Trajectory Expectation: $\langle e^{-\Delta s_{\text{tot}}} \rangle = 1.1399 \approx 1.0$.
- **Negative control and its actual result:**
  - Introducing an asymmetric open boundary sink on the lattice immediately destroys total potential conservation ($M_{\text{final}} < M_{\text{init}}$ with deviation $\gg 0.05$).
  - Running explicit non-symplectic RK4 produces continuous drift that grows monotonically with iteration count.
- **Review limits (Plumb):** the TUR test uses a hand-built proxy variance, not a measured Var(J); the Jarzynski test tolerance is +/-0.25 on a system whose stationary distribution is uniform (system-entropy term is zero), and a planted fault halving the total entropy production was not caught by any of the 10 tests.
- **Interpretation and limits:**
  Shows, for 10,000-step runs and the specific systems tested (not 'indefinite' simulation), consistent with the claim that discrete conservation laws are not numerical approximations; when discretizations are derived from discrete variational principles (discrete action $\mathbb{S}$), continuous symmetries generate exact discrete Noether invariants that survive indefinite continuous simulation without numerical decay.
- **Evidence path:** `experiments/discrete-noether-invariants/RESULT.txt`
