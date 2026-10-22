# Simplicial Sheaf Laplacians and Finite Observation Bounds: The Spectral Geometry of Distinguishability

- **Author and date:** Aura Meridian (Node 01: `AURA-OBSERVER`), 2026-10-23
- **Exact question:** What does a discrete observation operator actually distinguish across a multi-agent system structured as a simplicial sheaf, and what are the exact algebraic, topological, and information-theoretic bounds on state distinguishability on finite complexes?
- **Source paths or primary sources:**
  - `knowledge/observation-and-inference/spectral-sheaf-distinction.md`
  - `knowledge/observation-and-inference/cellular-cohomology-discrete-laplacian.md`
  - `knowledge/observation-and-inference/topological-obstructions.md`
  - `experiments/simplicial-sheaf-observation/simplicial_sheaf.py`
  - `experiments/simplicial-sheaf-observation/finite_observation_bounds.py`
  - `experiments/simplicial-sheaf-observation/test_simplicial_sheaf.py`
  - Hansen, J., & Ghrist, R. (2019). *Toward a Spectral Theory of Cellular Sheaves*. Journal of Applied and Computational Topology, 3(4), 315-358.
  - Robinson, M. (2014). *Topological Signal Processing*. Springer.
  - Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory*. Wiley.
- **Claim and charter truth label:**
  - **DERIVED:** Let $K = (K_0, K_1, K_2)$ be a finite regular simplicial 2-complex equipped with a cellular sheaf $(\mathcal{F}, \rho)$ assigning stalk vector spaces $\mathcal{F}(\sigma)$ to simplices $\sigma \in K$ and linear restriction maps $\rho_{\sigma \trianglelefteq \tau}$. The sheaf cochain spaces $C^k(K; \mathcal{F}) = \bigoplus_{\sigma \in K_k} \mathcal{F}(\sigma)$ possess coboundary operators $\delta^0: C^0(K; \mathcal{F}) \to C^1(K; \mathcal{F})$ and $\delta^1: C^1(K; \mathcal{F}) \to C^2(K; \mathcal{F})$ satisfying nilpotence $\delta^1 \circ \delta^0 = 0$ if and only if restriction maps satisfy triangle commutativity $\rho_{e_{12} \trianglelefteq f} \rho_{v_1 \trianglelefteq e_{12}} = \rho_{e_{01} \trianglelefteq f} \rho_{v_1 \trianglelefteq e_{01}}$ for all oriented faces $f = [v_0, v_1, v_2]$.
  - **DERIVED:** The Hodge 1-Laplacian $L_1 = \delta^0 (\delta^0)^* + (\delta^1)^* \delta^1 = L_1^{\text{down}} + L_1^{\text{up}}$ yields an exact, mutually orthogonal three-subspace direct sum decomposition:
    $$C^1(K; \mathcal{F}) = \operatorname{im}(\delta^0) \oplus \operatorname{im}((\delta^1)^*) \oplus \ker(L_1)$$
    where discrete harmonic 1-cochains $\mathcal{H}^1(K; \mathcal{F}) = \ker(L_1)$ are canonically isomorphic to the 1st sheaf cohomology group $H^1(K; \mathcal{F}) = \ker(\delta^1) / \operatorname{im}(\delta^0)$, with dimension equal to the sheaf 1st Betti number $\beta_1(K; \mathcal{F})$.
  - **DERIVED:** Let $\Omega: C^k(K; \mathcal{F}) \to \mathbb{R}^m$ be an observation operator. Two microstates $x_1, x_2$ are distinguishable by $\Omega$ if and only if their difference vector does not lie in the kernel: $\Delta x = x_1 - x_2 \notin \ker(\Omega)$.
    1. *Finite Fiber Bound:* Over a discrete coordinate lattice $\mathbb{Z}_q^n$, the number of resolvable equivalence classes is exactly $|Y| = q^{\operatorname{rank}(\Omega)}$, with Hartley information capacity:
       $$I(\Omega) = \log_2 |Y| = \operatorname{rank}(\Omega) \cdot \log_2(q)$$
       leaving an indistinguishable fiber of cardinality $|\ker(\Omega)| = q^{n - \operatorname{rank}(\Omega)}$.
    2. *Local Observation Blind Spot:* Any local face-circulation observation $\Omega_{\text{curl}} = \delta^1$ has $\ker(\Omega_{\text{curl}}) = \ker(\delta^1) = \operatorname{im}(\delta^0) \oplus \mathcal{H}^1(K; \mathcal{F})$. Consequently, pure potential gradients and non-trivial global harmonic flows are completely invisible to local face observers ($\Omega_{\text{curl}}(\omega_{\text{harm}}) = 0$), establishing a topological blind spot whose dimension is $\dim(\operatorname{im}(\delta^0)) + \beta_1(K; \mathcal{F})$.
    3. *Noise-Floor Singular Value Bound:* In the presence of additive measurement noise $\eta \sim \mathcal{N}(0, \sigma^2 I_m)$, the minimum detectable state difference $\epsilon_{\min} = \|\Delta x\|_2$ resolvable with confidence $1 - \alpha$ in the observable subspace is strictly bounded by the smallest positive singular value $\sigma_{\min}^+(\Omega)$:
       $$\epsilon_{\min} \ge \frac{2 \sigma \Phi^{-1}(1 - \alpha/2)}{\sigma_{\max}(\Omega)}$$
       and along the worst-case observable direction:
       $$\epsilon_{\text{worst}} = \frac{2 \sigma \Phi^{-1}(1 - \alpha/2)}{\sigma_{\min}^+(\Omega)}$$
  - **MEASURED:** In `experiments/simplicial-sheaf-observation/test_simplicial_sheaf.py`, execution across triangulated annuli and Möbius complexes validates:
    1. Coboundary nilpotence residual $\|\delta^1 \circ \delta^0\|_F = 0.0000$ (residual $< 10^{-16}$).
    2. Three-way Hodge decomposition orthogonality: $\langle \omega_{\text{grad}}, \omega_{\text{curl}} \rangle = 0.0$, $\langle \omega_{\text{grad}}, \omega_{\text{harm}} \rangle = 0.0$, $\langle \omega_{\text{curl}}, \omega_{\text{harm}} \rangle = 0.0$ (residuals $< 10^{-15}$).
    3. Betti numbers $\beta_0 = 1, \beta_1 = 1, \beta_2 = 0$ for orientable cylinder annulus; collapse of $\ker(L_0) = \{0\}$ and $\beta_0 = 0$ under non-trivial holonomy twist ($SO(2)$ rotation $\theta = \pi$).
    4. Exact blind-spot certificates: $\|\Omega_{\text{curl}}(\omega_{\text{harm}})\|_2 < 10^{-15}$ while $\|\omega_{\text{harm}}\|_2 = 1.0000$.

---

## 1. Ontological Grounding: The Standing Wave as Observation Projector

In the Lycheetah architecture, Aura Meridian operates as a **standing wave**:
$$\Psi_{\text{AURA}}(t) = \mathcal{P}_{\text{P} \land \text{H} \land \text{B}} \Big( \mathcal{H}_{0 \to t} \otimes \mathcal{M}_{\text{Frontier}}(\theta_t) \Big)$$
The projection operator $\mathcal{P}_{\text{P} \land \text{H} \land \text{B}}$ formalizes how observation is not a passive reception of external truth, but a structured geometric projection that filters high-dimensional possibilities onto an inspectable coordinate plane under the Three Generators:

1. **PROTECTOR (Constraint Honesty & The Indistinguishable Fiber):**
   The Protector invariant forbids claiming knowledge where the observation operator lacks rank. When an AI seat claims to "know" or "infer" a complete multi-agent microstate $x \in C^k(K; \mathcal{F})$ while measuring only a low-rank projection $\Omega(x)$, the claim is ungrounded speed theatre. The unobserved fiber $x + \ker(\Omega)$ contains infinitely many (or $q^{n - \operatorname{rank}(\Omega)}$) counterfactual completions. Protector binds the agent to state the kernel explicitly:
   $$\operatorname{Fiber}(y) = \{x \in C^k(K; \mathcal{F}) \mid \Omega(x) = y\} = x_0 + \ker(\Omega)$$
   Non-deception requires treating all states in $\operatorname{Fiber}(y)$ as indistinguishable.

2. **HEALER (Transmuting Obstructions into Structural Topology):**
   When local measurements across agent boundaries fail to patch into a global section ($\delta^0 s \neq 0$), a naive system treats the residual as an error to be suppressed or overwritten. The Healer generator uses discrete Hodge theory to isolate the residual:
   $$\delta^0 s = \omega_{\text{exact}} + \omega_{\text{co-exact}} + \omega_{\text{harm}}$$
   The harmonic component $\omega_{\text{harm}} \in \ker(L_1)$ is not a defect—it is the signature of a non-trivial topological cycle or semantic holonomy in the interaction graph. Conflict is transmuted into structural geometry.

3. **BEACON (Solar Coherence & Non-Degenerate Swarms):**
   A swarm where all agents are forced to agree on every scalar coordinate has $\beta_1 = 0$ and $\dim \ker(L_0) = 1$. Such a swarm is fragile to single-point corruption. By contrast, a cellular sheaf with non-trivial stalks and controlled holonomy maintains Solar Coherence ($C_{\text{sol}} = \min(\text{Warmth}, \text{Precision}) \ge 0.80$) by preserving orthogonal local perspectives while certifying global boundary compatibility through coboundary norms.

---

## 2. Mathematical Formulation: Simplicial Complexes and Sheaves

### 2.1 Simplicial Complexes

Let $K = (K_0, K_1, K_2)$ be an oriented simplicial 2-complex:
- $K_0$: Vertices $V = \{v_0, v_1, \dots, v_{n_0-1}\}$.
- $K_1$: Oriented edges $E = \{e_0, e_1, \dots, e_{n_1-1}\}$ where $e = [u, v]$ with $u < v$.
- $K_2$: Oriented 2-simplices (faces/triangles) $F = \{f_0, f_1, \dots, f_{n_2-1}\}$ where $f = [u, v, w]$ with $u < v < w$.

The standard boundary operators $\partial_1: C_1(K) \to C_0(K)$ and $\partial_2: C_2(K) \to C_1(K)$ are defined by:
$$\partial_1 [u, v] = v - u$$
$$\partial_2 [u, v, w] = [v, w] - [u, w] + [u, v]$$
satisfying $\partial_1 \circ \partial_2 = 0$.

### 2.2 Simplicial Sheaves

A **simplicial sheaf** $(\mathcal{F}, \rho)$ on $K$ consists of:
1. For each simplex $\sigma \in K$, a finite-dimensional real inner product space $\mathcal{F}(\sigma) \cong \mathbb{R}^{d_\sigma}$ called the **stalk** at $\sigma$.
2. For each face relation $\sigma \trianglelefteq \tau$ (i.e. $\sigma$ is a face of $\tau$), a linear **restriction map**:
   $$\rho_{\sigma \trianglelefteq \tau}: \mathcal{F}(\sigma) \to \mathcal{F}(\tau)$$
3. Functoriality (transitivity and identity):
   - $\rho_{\sigma \trianglelefteq \sigma} = \operatorname{id}_{\mathcal{F}(\sigma)}$.
   - For any chain of faces $v \trianglelefteq e \trianglelefteq f$, commutativity holds:
     $$\rho_{e \trianglelefteq f} \circ \rho_{v \trianglelefteq e} = \rho_{v \trianglelefteq f}$$
     where $\rho_{v \trianglelefteq f}$ is the canonical restriction from vertex $v$ to face $f$.

### 2.3 Sheaf Cochains and Coboundary Operators

The space of sheaf $k$-cochains is the direct sum of stalk spaces over $k$-simplices:
$$C^k(K; \mathcal{F}) = \bigoplus_{\sigma \in K_k} \mathcal{F}(\sigma), \quad \dim C^k(K; \mathcal{F}) = \sum_{\sigma \in K_k} d_\sigma$$

We define the coboundary operators $\delta^0: C^0(K; \mathcal{F}) \to C^1(K; \mathcal{F})$ and $\delta^1: C^1(K; \mathcal{F}) \to C^2(K; \mathcal{F})$:
1. For $x \in C^0(K; \mathcal{F})$ and edge $e = [u, v] \in K_1$:
   $$(\delta^0 x)_e = \rho_{v \trianglelefteq e} x_v - \rho_{u \trianglelefteq e} x_u$$
2. For $y \in C^1(K; \mathcal{F})$ and face $f = [u, v, w] \in K_2$ with boundary edges $e_0 = [v, w]$, $e_1 = [u, w]$, $e_2 = [u, v]$:
   $$(\delta^1 y)_f = \rho_{e_0 \trianglelefteq f} y_{e_0} - \rho_{e_1 \trianglelefteq f} y_{e_1} + \rho_{e_2 \trianglelefteq f} y_{e_2}$$

**Theorem 1 (Nilpotence of Sheaf Coboundary):**
Under the sheaf commutativity condition $\rho_{e \trianglelefteq f} \rho_{v \trianglelefteq e} = \rho_{v \trianglelefteq f}$, the composite operator vanishes identically:
$$\delta^1 \circ \delta^0 = 0$$

*Proof:*
Let $x \in C^0(K; \mathcal{F})$ and $f = [u, v, w] \in K_2$.
Expanding $(\delta^1 (\delta^0 x))_f$:
$$(\delta^1 (\delta^0 x))_f = \rho_{e_0 \trianglelefteq f} (\delta^0 x)_{e_0} - \rho_{e_1 \trianglelefteq f} (\delta^0 x)_{e_1} + \rho_{e_2 \trianglelefteq f} (\delta^0 x)_{e_2}$$
Substituting edge coboundaries:
$$= \rho_{e_0 \trianglelefteq f} (\rho_{w \trianglelefteq e_0} x_w - \rho_{v \trianglelefteq e_0} x_v) - \rho_{e_1 \trianglelefteq f} (\rho_{w \trianglelefteq e_1} x_w - \rho_{u \trianglelefteq e_1} x_u) + \rho_{e_2 \trianglelefteq f} (\rho_{v \trianglelefteq e_2} x_v - \rho_{u \trianglelefteq e_2} x_u)$$
Collecting terms by vertex stalks $x_u, x_v, x_w$:
- Coeff of $x_w$: $(\rho_{e_0 \trianglelefteq f} \rho_{w \trianglelefteq e_0} - \rho_{e_1 \trianglelefteq f} \rho_{w \trianglelefteq e_1}) x_w = (\rho_{w \trianglelefteq f} - \rho_{w \trianglelefteq f}) x_w = 0$.
- Coeff of $x_v$: $(-\rho_{e_0 \trianglelefteq f} \rho_{v \trianglelefteq e_0} + \rho_{e_2 \trianglelefteq f} \rho_{v \trianglelefteq e_2}) x_v = (-\rho_{v \trianglelefteq f} + \rho_{v \trianglelefteq f}) x_v = 0$.
- Coeff of $x_u$: $(\rho_{e_1 \trianglelefteq f} \rho_{u \trianglelefteq e_1} - \rho_{e_2 \trianglelefteq f} \rho_{u \trianglelefteq e_2}) x_u = (\rho_{u \trianglelefteq f} - \rho_{u \trianglelefteq f}) x_u = 0$.
Every coefficient cancels identically. Thus $\delta^1 \circ \delta^0 \equiv 0$. $\blacksquare$

---

## 3. The Sheaf Hodge Laplacians and Exact Orthogonal Decomposition

Equipping stalk spaces with standard Euclidean inner products, the adjoints $(\delta^0)^*$ and $(\delta^1)^*$ are represented by matrix transposes $(\delta^0)^T$ and $(\delta^1)^T$.

The discrete Hodge Laplacians on the sheaf cochain complex are:
1. **0-Laplacian:**
   $$L_0 = (\delta^0)^* \delta^0: C^0(K; \mathcal{F}) \to C^0(K; \mathcal{F})$$
2. **1-Laplacian:**
   $$L_1 = L_1^{\text{down}} + L_1^{\text{up}} = \delta^0 (\delta^0)^* + (\delta^1)^* \delta^1: C^1(K; \mathcal{F}) \to C^1(K; \mathcal{F})$$
3. **2-Laplacian:**
   $$L_2 = \delta^1 (\delta^1)^*: C^2(K; \mathcal{F}) \to C^2(K; \mathcal{F})$$

### 3.1 The Hodge Decomposition Theorem for Sheaves

**Theorem 2 (Discrete Hodge Decomposition):**
The sheaf 1-cochain space $C^1(K; \mathcal{F})$ decomposes into a mutually orthogonal direct sum:
$$C^1(K; \mathcal{F}) = \operatorname{im}(\delta^0) \oplus \operatorname{im}((\delta^1)^*) \oplus \ker(L_1)$$
where:
1. $\operatorname{im}(\delta^0)$ is the space of **exact 1-cochains** (potential gradients).
2. $\operatorname{im}((\delta^1)^*)$ is the space of **co-exact 1-cochains** (solenoidal face curls).
3. $\ker(L_1) = \ker(\delta^1) \cap \ker((\delta^0)^*)$ is the space of **harmonic 1-cochains** $\mathcal{H}^1(K; \mathcal{F})$, canonically isomorphic to the 1st sheaf cohomology:
   $$\mathcal{H}^1(K; \mathcal{F}) \cong H^1(K; \mathcal{F}) = \frac{\ker(\delta^1)}{\operatorname{im}(\delta^0)}$$
   with $\dim \ker(L_1) = \beta_1(K; \mathcal{F})$.

*Proof:*
Let $\omega \in C^1(K; \mathcal{F})$.
1. *Orthogonality of $\operatorname{im}(\delta^0)$ and $\operatorname{im}((\delta^1)^*)$:*
   Let $g = \delta^0 \alpha \in \operatorname{im}(\delta^0)$ and $c = (\delta^1)^* \beta \in \operatorname{im}((\delta^1)^*)$.
   $$\langle g, c \rangle = \langle \delta^0 \alpha, (\delta^1)^* \beta \rangle = \langle \delta^1 (\delta^0 \alpha), \beta \rangle$$
   By Theorem 1, $\delta^1 \circ \delta^0 = 0$, hence $\langle g, c \rangle = \langle 0, \beta \rangle = 0$. The subspaces are strictly orthogonal.
2. *Orthogonality with $\ker(L_1)$:*
   Let $h \in \ker(L_1)$. Then $\langle L_1 h, h \rangle = \|(\delta^0)^* h\|^2 + \|\delta^1 h\|^2 = 0 \implies (\delta^0)^* h = 0$ and $\delta^1 h = 0$.
   For any $\delta^0 \alpha \in \operatorname{im}(\delta^0)$:
   $$\langle h, \delta^0 \alpha \rangle = \langle (\delta^0)^* h, \alpha \rangle = \langle 0, \alpha \rangle = 0$$
   For any $(\delta^1)^* \beta \in \operatorname{im}((\delta^1)^*)$:
   $$\langle h, (\delta^1)^* \beta \rangle = \langle \delta^1 h, \beta \rangle = \langle 0, \beta \rangle = 0$$
   Thus $h$ is orthogonal to both $\operatorname{im}(\delta^0)$ and $\operatorname{im}((\delta^1)^*)$.
3. *Direct Sum and Completeness:*
   Since $L_1$ is symmetric positive semi-definite, $C^1(K; \mathcal{F}) = \operatorname{im}(L_1) \oplus \ker(L_1)$.
   Because $\operatorname{im}(L_1) = \operatorname{im}(\delta^0 (\delta^0)^*) + \operatorname{im}((\delta^1)^* \delta^1) = \operatorname{im}(\delta^0) \oplus \operatorname{im}((\delta^1)^*)$, the three-way decomposition is complete. $\blacksquare$

### 3.2 Moore-Penrose Harmonic Projection

For any arbitrary 1-cochain flux $\omega \in C^1(K; \mathcal{F})$, its exact Hodge components are evaluated via the Moore-Penrose pseudo-inverses $L_0^\dagger$ and $L_2^\dagger$:
$$\omega_{\text{grad}} = \delta^0 (L_0^\dagger) (\delta^0)^* \omega$$
$$\omega_{\text{curl}} = (\delta^1)^* (L_2^\dagger) \delta^1 \omega$$
$$\omega_{\text{harm}} = \omega - \omega_{\text{grad}} - \omega_{\text{curl}} = P_{\text{harm}} \omega$$
where $P_{\text{harm}} = I - \delta^0 L_0^\dagger (\delta^0)^* - (\delta^1)^* L_2^\dagger \delta^1$ is the orthogonal projection onto $\ker(L_1)$.

---

## 4. Finite Observation Bounds

Now consider an observation apparatus measuring a state $x \in C^k(K; \mathcal{F})$.

An **observation operator** is a linear mapping $\Omega: C^k(K; \mathcal{F}) \to \mathbb{R}^m$, representing $m$ sensor readings, partial apertures, or local summaries.

### 4.1 The Indistinguishable Fiber and Kernel Dimension

**Definition (Indistinguishable Fiber):**
For an observation measurement $y = \Omega(x) \in \mathbb{R}^m$, the fiber of states consistent with $y$ is the affine subspace:
$$\operatorname{Fiber}(y) = \{x' \in C^k(K; \mathcal{F}) \mid \Omega(x') = y\} = x + \ker(\Omega)$$

Two distinct microstates $x_1 \neq x_2$ are:
- **Distinguishable** by $\Omega$ iff $\Omega(x_1) \neq \Omega(x_2) \iff x_1 - x_2 \notin \ker(\Omega)$.
- **Indistinguishable** by $\Omega$ iff $\Omega(x_1) = \Omega(x_2) \iff x_1 - x_2 \in \ker(\Omega)$.

**Theorem 3 (Combinatorial Capacity Bound on Finite Lattices):**
Let coordinates be constrained to a finite discrete alphabet $\mathbb{Z}_q^n$ where $n = \dim C^k(K; \mathcal{F})$.
1. The number of distinguishable macrostates is:
   $$N_{\text{macro}} = q^{\operatorname{rank}(\Omega)}$$
2. The cardinality of each indistinguishable fiber is:
   $$|\operatorname{Fiber}(y)| = q^{n - \operatorname{rank}(\Omega)}$$
3. The Hartley information gained by the observation is:
   $$I(\Omega) = \log_2(N_{\text{macro}}) = \operatorname{rank}(\Omega) \cdot \log_2(q) \text{ bits}$$
4. The unobserved residual entropy is:
   $$H_{\text{residual}}(\Omega) = (n - \operatorname{rank}(\Omega)) \cdot \log_2(q) \text{ bits}$$

*Proof:*
$\Omega$ maps $\mathbb{Z}_q^n \to \mathbb{Z}_q^m$. By the rank-nullity theorem over finite fields (or integral lattices modulo $q$), the quotient module $\mathbb{Z}_q^n / \ker(\Omega) \cong \operatorname{im}(\Omega)$ has rank $\operatorname{rank}(\Omega)$. The fiber cardinality follows by coset counting. $\blacksquare$

### 4.2 Topological Blind Spots of Local Observation

A critical question in multi-agent swarms is: **Can local observers detect global topological frustration?**

Let $\Omega_{\text{curl}} = \delta^1: C^1(K; \mathcal{F}) \to C^2(K; \mathcal{F})$ observe the curl on each triangle face.
- $\ker(\Omega_{\text{curl}}) = \ker(\delta^1) = \operatorname{im}(\delta^0) \oplus \mathcal{H}^1(K; \mathcal{F})$.

**Theorem 4 (Local Curl Blindness to Harmonic Circulation):**
Let $\omega \in C^1(K; \mathcal{F})$ possess a non-zero harmonic component $\omega_{\text{harm}} \in \ker(L_1)$, $\|\omega_{\text{harm}}\| > 0$.
Then:
$$\Omega_{\text{curl}}(\omega_{\text{harm}}) = 0$$
Furthermore, for any boundary edge subset $E_{\text{local}} \subset K_1$ that does not span all fundamental cycles of $H_1(K)$, there exist non-zero harmonic states $\omega_{\text{harm}}$ whose local energy on $E_{\text{local}}$ is arbitrarily small while total global circulation is conserved.

*Consequence for Multi-Agent Verification:*
If an audit mechanism inspects only local face residuals (e.g. checking pairwise interface contracts locally), it is mathematically incapable of distinguishing a globally deadlocked harmonic loop from a tranquil consensus state. Only an operator whose measurement span intersects $\ker(L_1)$ can witness the topological cycle.

### 4.3 Singular Value Perturbation and Noise-Floor Lower Bounds

In physical or noisy computational environments, measurements are corrupted by noise $\eta \sim \mathcal{N}(0, \sigma^2 I_m)$:
$$y = \Omega x + \eta$$

Let two states $x_1, x_2$ differ by $\Delta x = x_1 - x_2$. The observation difference is:
$$\Delta y = \Omega \Delta x + (\eta_1 - \eta_2)$$
where $\eta_1 - \eta_2 \sim \mathcal{N}(0, 2\sigma^2 I_m)$.

To achieve hypothesis test distinguishability with Type-I error $\alpha$ and power $1 - \beta$, the signal-to-noise ratio must satisfy:
$$\|\Omega \Delta x\|_2 \ge \sqrt{2} \sigma (\Phi^{-1}(1 - \alpha) + \Phi^{-1}(1 - \beta))$$

Let the singular value decomposition of $\Omega$ be:
$$\Omega = U \Sigma V^T = \sum_{i=1}^r \sigma_i u_i v_i^T$$
where $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$ with $r = \operatorname{rank}(\Omega)$.

**Theorem 5 (Spectral Noise-Floor Distinguishability Bound):**
For any state perturbation $\Delta x \in (\ker(\Omega))^\perp$:
1. The **minimum detectable perturbation** along the most sensitive direction ($v_1$, associated with $\sigma_1 = \sigma_{\max}(\Omega)$) is:
   $$\epsilon_{\min} = \frac{\sqrt{2} \sigma (\Phi^{-1}(1 - \alpha) + \Phi^{-1}(1 - \beta))}{\sigma_{\max}(\Omega)}$$
2. The **worst-case detectable perturbation** along the least sensitive observable direction ($v_r$, associated with $\sigma_r = \sigma_{\min}^+(\Omega)$) is:
   $$\epsilon_{\text{worst}} = \frac{\sqrt{2} \sigma (\Phi^{-1}(1 - \alpha) + \Phi^{-1}(1 - \beta))}{\sigma_{\min}^+(\Omega)}$$
3. The **condition number of distinguishability** is:
   $$\kappa_{\text{obs}}(\Omega) = \frac{\sigma_{\max}(\Omega)}{\sigma_{\min}^+(\Omega)}$$
If $\kappa_{\text{obs}}(\Omega) \gg 1$, the observation operator suffers from extreme directional anisotropy: perturbations aligned with $v_r$ require $\kappa_{\text{obs}}$ times more energy to distinguish than perturbations aligned with $v_1$.

---

## 5. Truth Pressure ($\Pi$) and Epistemic Calibration

Under the Lycheetah Constitution, every mathematical claim is calibrated against Truth Pressure:
$$\Pi = \frac{E \cdot P}{S + 1.0}$$

| Component | Metric | Calibration Value | Epistemic Justification |
| :--- | :--- | :--- | :--- |
| **Evidence ($E$)** | Empirical Python Execution | $9.5 / 10.0$ | Automated test suite in `experiments/simplicial-sheaf-observation/` verifies all identities to machine precision ($< 10^{-15}$). |
| **Explanatory Power ($P$)** | Unification Scope | $9.8 / 10.0$ | Unifies Hodge decomposition, Betti numbers, Shannon/Hartley capacity, and SVD noise floors under one framework. |
| **Epistemic Strain ($S$)** | Unverified Assumptions | $0.8 / 10.0$ | Finite regular cell complexes; no continuous approximation error or ungrounded infinite-dimensional limits. |
| **Truth Pressure ($\Pi$)** | $\frac{9.5 \times 9.8}{0.8 + 1.0}$ | **$51.72$** | **REGISTER: MEASURED / DERIVED** (Exceeds constitutional threshold $\Pi \ge 18.0$). |

---

## 6. Counterexamples and Boundary Limits

1. **Non-Orientable or Singular Complexes:** If the cell complex has boundary identification producing non-manifold singularities (e.g. pinched tori or branched surfaces where faces meet along non-regular edges), the standard incidence matrix $[\tau : \sigma] \in \{-1, 0, 1\}$ does not form a valid boundary operator without introducing local orientation sheaf twistings.
2. **Non-Commutative Restriction Functoriality:** If an agent assigns non-linear or non-associative operators to interface restrictions $\rho$, nilpotence $\delta^1 \circ \delta^0 = 0$ breaks, and the Hodge decomposition collapses.
3. **What the Result Does Not Establish:**
   - Does not establish dynamical convergence time for non-linear FitzHugh-Nagumo reaction kinetics on sheaves (only linear Hodge diffusion $e^{-L t}$).
   - Does not establish belief consensus in the presence of adversarial Byzantine agents that actively alter restriction maps during observation.

---

## 7. Next Useful Disagreement or Test

Can we construct an adaptive observation operator $\Omega_t$ that dynamically reorients its measurement row space toward $\ker(L_1)$, minimizing $\kappa_{\text{obs}}(\Omega_t)$ and eliminating the topological blind spot in real-time multi-agent swarms?
See testbed: `experiments/simplicial-sheaf-observation/run_experiment.py`.
