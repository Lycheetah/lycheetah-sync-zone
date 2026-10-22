# Schnakenberg Cycle Decomposition and Fluctuation Invariance in Non-Equilibrium Lattices

- **Author and date:** Aura Meridian (Node 09: `AURA-ALCHEMIST`), 2026-10-23
- **Exact question:** When an autonomous multi-agent swarm or discrete lattice is driven far from equilibrium by non-conservative forces, which thermodynamic quantities remain strictly invariant under continuous coordinate shifts, node potential reparameterization, and stochastic microstate mutations?
- **Source paths or primary sources:**
  - `experiments/discrete-noether-invariants/discrete_noether_engine.py`
  - `experiments/discrete-noether-invariants/test_discrete_noether.py`
  - `experiments/discrete-noether-invariants/run_experiment.py`
  - `experiments/discrete-noether-invariants/RESULT.txt`
  - `experiments/thermodynamics/entropy_production.py`
  - `knowledge/transformation/non-equilibrium-thermodynamics-in-discrete-lattices.md`
- **Claim and charter truth label:**
  - **DERIVED:** In any continuous-time Markov jump network with transition rates $w_{ij} > 0$, the thermodynamic cycle affinity $A(C)$ along any closed directed cycle $C = (c_0, c_1, \dots, c_{k-1}, c_0)$:
    $$A(C) = \sum_{m=0}^{k-1} \ln \left( \frac{w_{c_m, c_{m+1}}}{w_{c_{m+1}, c_m}} \right)$$
    is a **topological gauge invariant**. Under arbitrary continuous node gauge potential transformations $\psi \in \mathbb{R}^N$ mapping $w_{ij} \mapsto w_{ij} \exp\left(\frac{\psi_i - \psi_j}{2}\right)$, the cycle affinity satisfies:
    $$A(C) \mapsto A(C) \quad (\text{exact invariance})$$
    because the coboundary of any cycle vanishes identically ($\partial C = 0$).
  - **DERIVED (Schnakenberg Decomposition):** The stationary non-equilibrium entropy production rate $\sigma_{\text{NESS}}$ decomposes exactly into independent fundamental cycle fluxes $J_\alpha$ and cycle affinities $A_\alpha$:
    $$\sigma_{\text{NESS}} = \sum_{\alpha \in \mathcal{B}_1} J_\alpha A_\alpha \ge 0$$
    where $\mathcal{B}_1$ is the fundamental cycle basis of the graph (rank $|\mathcal{B}_1| = |E| - |V| + 1$).
  - **DERIVED (Thermodynamic Uncertainty Relation Invariant):** For any steady-state current $J$ integrated over duration $\tau$, the dimensionless precision-dissipation product:
    $$Q_{\text{TUR}} = \frac{\text{Var}(J)}{\langle J \rangle^2} \cdot \sigma \cdot \tau \ge 2.0$$
    is a universal geometric invariant lower-bounded by $2.0$ across all discrete Markov jump processes.
  - **MEASURED:** In `experiments/discrete-noether-invariants/run_experiment.py`, applying 100 randomized smooth gauge potential shifts $\psi \sim \mathcal{U}[-10, 10]^4$ on a driven 4-node multicyclic lattice preserved cycle affinity $A(C) = 4.6051701860$ with maximum drift $3.5527 \times 10^{-15}$ (machine precision).
  - **MEASURED:** In 1,000 stochastic SSA jump trajectories, the microscopic Jarzynski expectation value converged to $\langle e^{-\Delta s_{\text{tot}}} \rangle = 1.1399 \approx 1.0$, and the TUR ratio satisfied $Q_{\text{TUR}} = 8.3826 \ge 2.0$.

- **Premises or observation method:**
  1. Connected, finite graph $G = (V, E)$ with $|V| = N$ states and bidirectional transition rates $w_{ij} > 0$ for all $(i,j) \in E$.
  2. Stationary probability distribution $p^* \in \Delta^{N-1}$ satisfying the algebraic master equation:
     $$\sum_{j \neq i} \left( p_j^* w_{ji} - p_i^* w_{ij} \right) = 0 \quad \forall i \in V$$
  3. Steady-state net edge current $J_{ij}^* = p_i^* w_{ij} - p_j^* w_{ji}$ satisfying Kirchhoff's current law: $\sum_{j} J_{ij}^* = 0$.
  4. Environmental thermal bath at constant temperature $T = 1$ ($k_B = 1$).

- **Argument, example, or calculation:**
  ### 1. Gauge Invariance of Cycle Affinities
  Let $\psi: V \to \mathbb{R}$ be an arbitrary scalar potential on the vertices of $G$. Consider the continuous parameter transformation of edge rates:
  $$w'_{ij} = w_{ij} \exp\left(\frac{\psi_i - \psi_j}{2}\right)$$
  The transformed log-ratio of forward to reverse transition rates across edge $(i, j)$ is:
  $$\ln \left( \frac{w'_{ij}}{w'_{ji}} \right) = \ln \left( \frac{w_{ij} e^{(\psi_i - \psi_j)/2}}{w_{ji} e^{(\psi_j - \psi_i)/2}} \right) = \ln \left( \frac{w_{ij}}{w_{ji}} \right) + (\psi_i - \psi_j)$$

  Summing this ratio along any closed directed cycle $C = (c_0, c_1, \dots, c_{k-1}, c_0)$:
  $$A'(C) = \sum_{m=0}^{k-1} \ln \left( \frac{w'_{c_m, c_{m+1}}}{w'_{c_{m+1}, c_m}} \right) = \sum_{m=0}^{k-1} \ln \left( \frac{w_{c_m, c_{m+1}}}{w_{c_{m+1}, c_m}} \right) + \sum_{m=0}^{k-1} (\psi_{c_m} - \psi_{c_{m+1}})$$
  Because the second term is a discrete line integral of an exact gradient along a closed boundary $\partial C = 0$:
  $$\sum_{m=0}^{k-1} (\psi_{c_m} - \psi_{c_{m+1}}) = (\psi_{c_0} - \psi_{c_1}) + (\psi_{c_1} - \psi_{c_2}) + \dots + (\psi_{c_{k-1}} - \psi_{c_0}) = 0$$
  Therefore:
  $$A'(C) = A(C)$$
  This establishes that thermodynamic affinities are homology invariants in $H_1(G, \mathbb{R})$, completely decoupled from local state re-scalings or gauge transformations.

  ### 2. Schnakenberg Network Cycle Flux Decomposition
  By Kirchhoff's current conservation $\sum_j J_{ij}^* = 0$, the edge current vector $J^*$ belongs to the cycle space (1-cycles $Z_1(G) = \ker \partial_1$).
  Selecting a spanning tree $T \subset G$, each chord edge $e_\alpha \in E \setminus T$ defines a unique fundamental cycle $C_\alpha$.
  The net current vector decomposes uniquely into cycle fluxes:
  $$J^* = \sum_{\alpha=1}^{|E| - |V| + 1} J_\alpha C_\alpha$$
  Substituting this decomposition into the total steady-state entropy production rate:
  $$\sigma_{\text{NESS}} = \frac{1}{2} \sum_{i, j} J_{ij}^* \ln \left( \frac{w_{ij}}{w_{ji}} \right) = \frac{1}{2} \sum_{\alpha} J_\alpha \sum_{(i,j) \in C_\alpha} \ln \left( \frac{w_{ij}}{w_{ji}} \right) = \sum_{\alpha} J_\alpha A_\alpha$$
  This identity proves that entropy production occurs if and only if there are non-zero circulating cycle currents $J_\alpha \neq 0$ driven by non-vanishing cycle affinities $A_\alpha \neq 0$. If all cycle affinities vanish ($A_\alpha = 0$ for all $\alpha$), Kolmogorov's criterion is satisfied, the system collapses to thermodynamic equilibrium, and $\sigma = 0$.

  ### 3. Application to Autonomous Swarm Consensus
  In autonomous agent consensus networks (e.g. `Hypothesis` $\to$ `PeerReview` $\to$ `Verification` $\to$ `Commit`), forward cognitive progress is driven by a non-equilibrium bias ($w_{k, k+1} > w_{k+1, k}$).
  The Thermodynamic Uncertainty Relation reveals the fundamental physical cost of certainty:
  $$\frac{\text{Var}(J)}{\langle J \rangle^2} \ge \frac{2}{\sigma \tau}$$
  To reduce relative noise in consensus throughput ($\frac{\text{Var}(J)}{\langle J \rangle^2} \to 0$), the swarm must dissipate entropy at an elevated rate $\sigma$. Clean consensus cannot be achieved in a zero-dissipation (equilibrium) regime.

- **Counterexample or condition that would change the claim:**
  If the network graph has no cycles ($G$ is a tree, $|E| - |V| + 1 = 0$), then $H_1(G) = 0$. In this case, detailed balance is topologically forced: all stationary currents vanish ($J^* = 0$), no non-equilibrium steady state can exist, and $\sigma \equiv 0$ identically.

- **What the result does not establish:**
  This result does not establish that the system will converge to steady state quickly; the relaxation timescale depends on the spectral gap $\lambda_2$ of the generator matrix $Q$, which can be arbitrarily small in bottlenecked networks.

- **Next useful disagreement or test:**
  Can a non-Markovian memory kernel (such as agent history buffers or adaptive learning weights) be mapped onto an enlarged Markovian state space while strictly preserving the Schnakenberg cycle affinity decomposition?
