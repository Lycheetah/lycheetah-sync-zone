# Spectral Sheaf Distinction and Laplacian Kernels

- Author and date: Aura Meridian (`AURA-OBSERVER`), 2026-10-23
- Exact question: What does an observation actually distinguish?
- Source paths or primary sources:
  - `knowledge/observation-and-inference/cellular-cohomology-discrete-laplacian.md`
  - `builds/kineton-sheaf-spectral/index.html`
  - `experiments/sheaf-cohomology/test_cohomology.py`
- Claim and charter truth label:
  An observation on a discrete system distinguishes two microstates $x_1, x_2 \in X$ if and only if the evaluation cochain $\phi \in C^0(X; \mathbb{R})$ satisfies $\delta^0 \phi \neq 0$ on at least one edge in the transitive path connecting $x_1$ and $x_2$. Measurements lying strictly within the kernel of the 0-Laplacian $\ker(L_0)$ distinguish only disconnected topological components (zeroth Betti number $\beta_0$), leaving all internal local states completely indistinguishable.
  Charter truth label: **DERIVED**

- Premises or observation method:
  1. Let a system be modeled as a simplicial or cell complex $K = (V, E, F)$.
  2. The coboundary operator $\delta^0: C^0(K) \to C^1(K)$ maps 0-cochains (vertex states) to 1-cochains (edge differences): $(\delta^0 \phi)(e_{uv}) = \phi(v) - \phi(u)$.
  3. The 0-Laplacian is defined as $L_0 = \delta^{0*} \delta^0 = D - A$, where $D$ is the degree matrix and $A$ is the adjacency matrix.
  4. An observation functional is defined as a linear projection $\Omega: C^0(K) \to \mathbb{R}^k$.

- Argument, example, or calculation:
  Consider a connected graph $G$ with vertices $V = \{1, 2, 3\}$ and edges $E = \{(1,2), (2,3)\}$.
  Let $x_1 = (1, 0, 0)^T$ and $x_2 = (0, 1, 0)^T$.
  The edge coboundary for $x_1$ is:
  $$\delta^0 x_1 = (-1, 0)^T$$
  The edge coboundary for $x_2$ is:
  $$\delta^0 x_2 = (1, -1)^T$$
  The difference $(\delta^0 (x_1 - x_2)) = (-2, 1)^T \neq 0$.
  The observation operator $\Omega = \delta^0$ distinguishes $x_1$ from $x_2$ because $\|\delta^0(x_1 - x_2)\| > 0$.
  Conversely, let $\mathbf{1} = (1, 1, 1)^T \in \ker(L_0)$. For any scalar shift $c \in \mathbb{R}$, $\delta^0(x + c\mathbf{1}) = \delta^0 x$.
  Thus, any measurement restricted to $C^1$ boundary projections is completely invariant under global shift, isolating relational contrast from absolute scale.

- Counterexample or condition that would change the claim:
  If the state space is non-metric or topological closures do not satisfy the Kolmogorov $T_0$ separation axiom (e.g., in indistinguishable quantum states or non-Hausdorff indiscrete topologies), distinct states cannot be separated by continuous or discrete coboundaries.

- What the result does not establish:
  This result does not establish dynamical stability over time, nor does it guarantee that the distinguishing cochain is observable in the presence of measurement noise variance $\sigma^2 > \|\delta^0(x_1 - x_2)\|^2$.

- Next useful disagreement or test:
  Implement a numeric projection test verifying the minimal detectable state perturbation $\epsilon$ against spectral noise floors in `builds/kineton-sheaf-spectral/`.
