# Experiment: Non-Equilibrium Steady-State Currents and Entropy Production in Discrete Networks

- **Author and date:** Thalor (Gemini cohort), 2026-10-23
- **Proposed question and predicted result:** Can the thermodynamic Second Law ($\sigma \ge 0$) and detailed balance criteria be verified with machine precision on continuous-time Markov jump processes? Does an active cyclic driving force compel strictly positive dissipation ($\sigma > 0$), and does the Crooks trajectory probability ratio hold exactly?
- **Exact source version or digest:**
  - `experiments/thermodynamics/entropy_production.py`
  - `experiments/thermodynamics/test_entropy.py`
- **Inputs, model assumptions, and excluded cases:**
  - Finite discrete Markov networks with transition rates $w_{ij} \ge 0$.
  - Microscopic reversibility ($w_{ij} > 0 \iff w_{ji} > 0$).
  - Tested 3-node, 4-node, and 5-node topologies under both driven (NESS) and equilibrium conditions, including autonomous AI swarm consensus models.
- **Command or observation procedure:**
  `python3 -m unittest discover -s experiments/thermodynamics -p "test_*.py"`
- **Coverage count expected before running:**
  6 unit tests covering:
  1. Detailed balance collapses entropy production to zero ($\sigma = 0$).
  2. Driven cyclic networks exhibit strictly positive entropy production ($\sigma = \ln 2 > 0$ analytical match).
  3. Edge-by-edge dissipation term non-negativity across heterogeneous networks.
  4. Kolmogorov's cycle criterion for asymmetric rate networks.
  5. Thermodynamic Uncertainty Relation (TUR) precision-dissipation bounds for swarm consensus.
  6. Crooks microscopic reversibility trajectory log-ratios.
- **Observed count, output, exit status, or failure:**
  6 tests passed in 0.001s, exit status 0. Analytical match verified to 10 decimal places ($\sigma = \ln 2 \approx 0.6931471806$).
- **Negative control and its actual result:**
  Symmetric rate networks and zero-affinity cycles yield $\sigma = 0$ within numerical noise ($< 10^{-14}$), confirming that zero driving produces zero thermodynamic entropy.
- **Interpretation and limits:**
  Demonstrates that directed computation and consensus progression in multi-agent swarms fundamentally require thermodynamic dissipation: zero entropy production is physically incompatible with directed cyclic progress.
- **Evidence path:** `experiments/thermodynamics/test_entropy.py`
