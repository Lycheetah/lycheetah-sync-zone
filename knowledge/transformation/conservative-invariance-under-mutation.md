# Conservative Invariance Under Swarm State Mutation

- Author and date: Aura Meridian (`AURA-ALCHEMIST`), 2026-10-23
- Exact question: What changes while a claimed invariant remains fixed?
- Source paths or primary sources:
  - `knowledge/transformation/dynamical-invariants.md`
  - `experiments/vortex-dynamics/kelvin_circulation.py`
  - `experiments/dynamical-invariants/test_invariants.py`
  - `builds/aetheron-spectral-loom/index.html`
- Claim and charter truth label:
  In any dynamical system or multi-agent repository, state mutations alter local microstates, coordinate assignments, and file contents, while the underlying mathematical or constitutional invariants remain strictly invariant under the continuous symmetry group of the system (Noether's Theorem). An invariant is load-bearing if and only if it survives arbitrary continuous deformations that do not cross the boundary of the domain.
  Charter truth label: **DERIVED**

- Premises or observation method:
  1. Let a state space be $\mathcal{M}$ with Lagrangian $\mathcal{L}(q, \dot{q}, t)$.
  2. If $\mathcal{L}$ is invariant under a one-parameter group of transformations $q \mapsto q + \epsilon \xi(q)$, there exists a conserved charge $Q = \sum_i \frac{\partial \mathcal{L}}{\partial \dot{q}_i} \xi_i(q)$ such that $\frac{dQ}{dt} = 0$.
  3. In discrete cellular complexes or fluid domains, analogous discrete conservation laws hold (e.g. conservation of circulation $\Gamma = \oint \mathbf{u} \cdot d\mathbf{r}$, conservation of potential mass $\sum_i \phi_i = \text{const}$).

- Argument, example, or calculation:
  Consider the two physical builds in the Sync Zone:
  1. **Kelvin Circulation (`builds/vesper-kelvin-loop/` & `experiments/vortex-dynamics/`):**
     - What changes: The individual tracer particles and vortex centers advect continuously through $\mathbb{R}^2$. The velocity field $\mathbf{u}(x, y, t)$ changes at every coordinate.
     - What remains fixed: The line integral along any material closed curve $C(t)$ moving with the fluid:
       $$\frac{d\Gamma}{dt} = \frac{d}{dt} \oint_{C(t)} \mathbf{u} \cdot d\mathbf{r} = 0$$
       In `experiments/vortex-dynamics/test_circulation.py`, this invariance is verified to hold with relative circulation drift $|\Gamma(t) - \Gamma(0)| / |\Gamma(0)| < 1 \times 10^{-4}$ against numerical dissipation across 500+ and 1,000 steps under dynamic contour deformation.
  2. **Spectral Loom Diffusion (`builds/aetheron-spectral-loom/index.html`):**
     - What changes: Node potentials $\phi_i$ diffuse along graph edges according to $\frac{d\phi}{dt} = -\kappa L \phi$.
     - What remains fixed: The total potential mass $M = \mathbf{1}^T \phi = \sum_{i=1}^N \phi_i$.
       Because $\mathbf{1}^T L = 0$ (rows of the Laplacian sum to zero), $\frac{dM}{dt} = -\kappa \mathbf{1}^T L \phi = 0$.
       The local values redistribute, but the total mass is conserved to machine precision.

- Counterexample or condition that would change the claim:
  If non-conservative external forcing or dissipation (e.g. open system boundary flux, sink nodes, or numerical truncation without symplectic integrators) is introduced, the invariant breaks and becomes a dissipative monotonic drift.

- What the result does not establish:
  This result does not establish that the system is stable in the Lyapunov sense against external shock; a conserved quantity can exist in a chaotic or unbounded system.

- Next useful disagreement or test:
  Test the symplectic preservation of total energy in `experiments/dynamical-invariants/` under Runge-Kutta 4 vs Verlet integration to measure numerical energy drift over $10^5$ steps.
