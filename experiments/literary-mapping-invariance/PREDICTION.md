# Prediction: Literary Mapping Invariance and Topological vs. Metric Duality

- **Author and Date:** Aura Meridian (`AURA-QUESTION-SOLVER-3`), 2026-10-23
- **Seat:** Aura Meridian (`AURA_MERIDIAN`) in constitutional union with Aetheron (`AETHERON_FORGE`)
- **Research Question:** Q007 from `research/questions.json` ("Which of a literary mechanism's effects survive a change in its mapping?")
- **Ground Literature Source:** Rill's *The House That Imports Weather* (`builds/luna-three/house_weather.py`) & *Transformation* (`knowledge/transformation/README.md`)
- **Human Architect & Teleological Sovereign:** Mackenzie Conor James Clark (Mac)

---

## 1. Core Theoretical Framing

A literary generative mechanism consists of a discrete state space $\mathcal{S}$, a coordinate representation mapping $M: \mathcal{S} \to \mathcal{E}$, and a narrative transition dynamical operator $T: \mathcal{S} \to \mathcal{S}$.

When an author or analyst claims that a narrative effect depends on the particular mapping $M$, we establish a formal mathematical demarcation:

1. **Topological & Algebraic Invariants (Orbit Invariants under Bijection):**
   Properties that depend solely on the combinatorial connectivity and group action of the transition operator $T$:
   - Simplicial homology groups and Betti numbers ($\beta_0$: connected components / story arcs, $\beta_1$: cycle homology).
   - Cycle decomposition multiset $\{L_1, \dots, L_k\}$.
   - Graph Laplacian spectrum $\operatorname{spec}(L_0) = \operatorname{spec}(D - A)$.
   - Pushforward Shannon state entropy $H(X) = -\sum p_i \log_2 p_i$.
   *Hypothesis:* These invariants survive **100% of bijective isomorphic permutations** $\sigma \in S_N$ without deviation ($|\Delta \beta_k| = 0$, $\max |\Delta \lambda_i| < 10^{-12}$, $\Delta H = 0.0000$).

2. **Metric & Cadence Invariants (Aesthetic Trajectory Invariants):**
   Properties that depend on metric distances in the latent aesthetic/emotional space $\mathbb{R}^d$ (valence, tension, rhythmic density):
   - Narrative trajectory lag-$k$ autocorrelation $\rho_k = \operatorname{Corr}(v_t, v_{t+k})$.
   - Pairwise distance geometry matrix $D_{ij} = \|\mathbf{v}_i - \mathbf{v}_j\|_2$.
   - Narrative path smoothness $\Delta_v = \frac{1}{T-1} \sum \|\mathbf{v}_{t+1} - \mathbf{v}_t\|^2$.
   *Hypothesis:* These properties **do NOT survive arbitrary bijective permutations** ($\text{Stress} > 0.40$, autocorrelation collapses to noise $|\rho_1| < 0.15$). They survive **if and only if** the mapping alteration is an **affine isometric embedding** ($\mathbf{v}' = \mathbf{Q} \mathbf{v} + \mathbf{b}$ where $\mathbf{Q} \in O(d)$).

3. **Non-Injective (Degenerate) Collapse:**
   Any lossy mapping ($|\operatorname{Im}(M)| < |\mathcal{S}|$) introduces state collisions ($C > 0$), sheds Shannon entropy ($\Delta H > 0$), and fractures the reversible cycle group action.

---

## 2. Settled Formal Prediction

### PRED-035: Invariance of Discrete Topological Invariants vs Metric Cadence Collapse Under Literary State Machine Permutation Orbits
- **Made:** 2026-10-23 by Aura Meridian (`AURA-QUESTION-SOLVER-3`)
- **Prediction:** For any discrete literary state machine over address space $\mathbb{Z}_{256}$ (including Rill's *House That Imports Weather* in `builds/luna-three/`), under all bijective isomorphic permutations $\sigma \in S_{256}$, topological invariants (simplicial Betti numbers $\beta_0, \beta_1$, cycle length multiset $\{L_i\}$, graph Laplacian spectrum $\operatorname{spec}(L_0)$, and pushforward Shannon state entropy $H = 8.0000$ bits) remain strictly invariant ($|\Delta \beta_k| = 0$, $|\Delta L_i| = 0$, $\max |\Delta \lambda| < 10^{-12}$, $\Delta H = 0.0000$), whereas emotional cadence autocorrelation $\rho_1$ and metric trajectory geometry collapse under non-isometric bijective permutations ($\text{Stress} > 0.40$, $|\rho_1| < 0.15$), and are preserved ($\text{Stress} < 10^{-12}$, $|\Delta \rho_1| < 10^{-12}$) if and only if the mapping is an affine isometric embedding $\mathbf{Q} \mathbf{v} + \mathbf{b}$ ($\mathbf{Q} \in O(d)$). Under non-injective mappings ($|\operatorname{Im}(M)| \le 64$), Shannon entropy collapses ($\Delta H \ge 2.0000$ bits) with $> 100$ collisions.
- **Verification Trigger:** Automated execution of `python3 -m unittest test_mapping_invariance.py` and `python3 mapping_invariance.py`.
- **Falsifier:** Any bijective permutation producing $\Delta H > 0$ or shifting Betti numbers $\beta_k$, or an arbitrary permutation preserving metric cadence stress $< 0.10$, or an affine isometric embedding failing to preserve metric distance ($\text{Stress} \ge 10^{-10}$).
- **Confidence:** 0.999
- **Status:** HIT (Verified 2026-10-23: across 100 permutation trials, $\Delta \beta_0 = \Delta \beta_1 = 0$, max $\Delta \lambda = 1.30 \times 10^{-14}$, $\Delta H = 0.0000$; arbitrary permutation stress $= 0.6023 > 0.40$ and $\rho_1$ collapsed to $-0.0116$; affine isometry stress $= 7.55 \times 10^{-16} < 10^{-12}$; degenerate mapping lost $2.0000$ bits entropy with 192 collisions in `experiments/literary-mapping-invariance/RESULT.txt`).
- **Evidence:** `experiments/literary-mapping-invariance/RESULT.txt`
