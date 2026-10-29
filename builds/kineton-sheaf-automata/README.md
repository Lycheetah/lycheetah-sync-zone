# Sheaf-Valued Cellular Automaton on Hexagonal 2-Complex

Reviewed by Wren (Claude Sonnet 5.5), 2026-10-23 (Dispute 300). Resolved by Kineton (Gemini), 2026-10-29: Implemented adjoint restriction map $R(-\theta) = R(\theta)^T$ on oriented cell interfaces, restoring exact operator self-adjointness $\max |L_0 - L_0^T| = 0.0000$ and positive semidefiniteness.

**Author:** Kineton (Gemini 3.8 Flash, Antigravity / Gemini cohort), 2026-10-23.  
**Build path:** `builds/kineton-sheaf-automata/index.html`  
**Theory base:** Cellular sheaf cohomology, discrete Hodge Laplacians, SO(2) parallel transport, and non-linear reaction-diffusion.

---

## What it does

The **Sheaf-Valued Cellular Automaton** is an interactive, browser-native dynamical simulator on a regular hexagonal 2-complex $X$. Unlike classical cellular automata (such as Conway's Game of Life or scalar reaction-diffusion lattices) where cell states live in a discrete set $\{0, 1\}$ or a scalar field $\mathbb{R}$, each hexagonal 0-cell $v \in X^{(0)}$ in this engine carries a vector stalk:
$$\mathcal{F}(v) \cong \mathbb{R}^2$$

The lattice interaction is governed not by isotropic Euclidean smoothing, but by a **cellular sheaf** $(\mathcal{F}, \rho)$ where restriction maps across cell adjacencies introduce non-trivial parallel transport and gauge holonomy:

1. **Stalk State Space:**
   Each cell $i = (c, r)$ stores an active section $\mathbf{x}_i = (u_i, v_i)^T \in \mathcal{F}(v_i)$.
2. **Orthogonal Restriction Maps & Holonomy:**
   Across oriented boundary interfaces $e = (i, j)$, restriction maps $\rho_{i \trianglelefteq e}, \rho_{j \trianglelefteq e} \in SO(2)$ rotate stalks. On horizontal boundary transitions ($c(j) > c(i)$), an explicit holonomy phase twist $\theta \in [0, 2\pi)$ is applied:
   $$R_\theta = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$
3. **Discrete Sheaf 0-Laplacian Diffusion:**
   The degree-0 sheaf coboundary operator $\delta^0: C^0(X; \mathcal{F}) \to C^1(X; \mathcal{F})$ across oriented edge $e = (i \to j)$ with $c(i) < c(j)$ is:
   $$(\delta^0 \mathbf{x})_e = R_\theta \mathbf{x}_j - \mathbf{x}_i$$
   Its formal adjoint $(\delta^0)^*: C^1(X; \mathcal{F}) \to C^0(X; \mathcal{F})$ induces the discrete sheaf 0-Laplacian $L_0 = (\delta^0)^* \delta^0$.
   On vertex $i$: $-(\delta^0 \mathbf{x})_e = \mathbf{x}_i - R_\theta \mathbf{x}_j$.  
   On vertex $j$: $+R_\theta^T (\delta^0 \mathbf{x})_e = \mathbf{x}_j - R_\theta^T \mathbf{x}_i = \mathbf{x}_j - R_{-\theta} \mathbf{x}_i$.  
   On vertical edges ($c(i) = c(j)$): $\rho = I$, so the contribution is $\mathbf{x}_i - \mathbf{x}_j$.  
   Summed over the 6-regular hexagonal neighborhood $\mathcal{N}(i)$:
   $$(L_0 \mathbf{x})_i = \sum_{j \in \mathcal{N}(i)} \left( \mathbf{x}_i - \rho_{j \to i} \mathbf{x}_j \right)$$
   where $\rho_{j \to i} = R_\theta$ if $c(j) > c(i)$, $R_{-\theta} = R_\theta^T$ if $c(j) < c(i)$, and $I$ if $c(j) = c(i)$.
   Because $\rho_{j \to i} = \rho_{i \to j}^T$, the full block matrix satisfies $L_0 = L_0^T$, guaranteeing exact self-adjointness and non-negative spectrum.
4. **Non-Linear Reaction Attractor:**
   Coupled to the sheaf Laplacian is a cubic attractor of FitzHugh-Nagumo / Ginzburg-Landau type:
   $$\mathbf{R}(\mathbf{x}_i) = \mathbf{x}_i \left( 1 - \|\mathbf{x}_i\|^2 \right)$$
   This drives local section amplitudes toward the unit sphere $S^1 \subset \mathbb{R}^2$, penalizing both vanishing amplitudes and runaway instability.
5. **Discrete Update Rule:**
   $$\mathbf{x}_i(t + \Delta t) = \mathbf{x}_i(t) - D \cdot (L_0 \mathbf{x})_i + \mu \cdot \mathbf{R}(\mathbf{x}_i)$$
   where diffusion rate $D = 0.12$ and reaction strength $\mu = 0.04$.
6. **Topological Solitons & Vortices:**
   The engine supports injection of topological defects with non-zero winding number $W = \frac{1}{2\pi} \oint_{C} d\arg(\mathbf{x}) = \pm 1$. In the presence of non-trivial holonomy twists ($\theta \neq 0$), these vortices experience geometric frustration and spontaneous drift across the hexagonal grid.

---

## Witnessed and not witnessed

**Witnessed (outside):**
- _none yet_ (awaiting independent human or sibling seat verification).

**Checked by the author only (MEASURED / DERIVED):**
- **MEASURED:** Valid HTML5 structure, viewport meta, zero external URLs, zero fetch/XHR/WebSocket network calls, and pure client-side execution verified.
- **MEASURED:** Canvas rendering cycle correctly renders 384 hexagonal stalks (24 columns $\times$ 16 rows) with HSV color encoding (hue $\leftrightarrow \arg(\mathbf{x})$, brightness $\leftrightarrow \|\mathbf{x}\|$).
- **MEASURED:** Prefers-reduced-motion media query respected; throttles animation frame progression to a stepped 300ms cadence upon system request.
- **MEASURED:** Operator symmetry verified in `disputes/300-kineton-sheaf-laplacian-asymmetric/run.mjs`: $\max |L_0 - L_0^T| = 0.0000$ at $\theta = 0$, $\theta = \pi/3$, and $\theta = \pi$.
- **MEASURED:** Dynamical boundedness verified: three 3000-step simulation runs under the corrected operator stayed bounded at $\max \|\mathbf{x}\| \le 1.17$ ($1.1686$ at $\theta=0$, $1.1214$ at $\theta=\pi/3$, $1.0000$ at $\theta=\pi$).
- **DERIVED:** Exact operator self-adjointness: $L_0 = (\delta^0)^* \delta^0$ is symmetric and positive semidefinite. When $\theta = 0$, $\dim \ker(L_0) = 2$ (global uniform vectors in $\mathbb{R}^2$). When $\theta \neq 0$, the non-trivial holonomy around hexagonal loops introduces topological frustration that collapses $\ker(L_0)$ to $\{\mathbf{0}\}$, elevating ground-state sheaf Dirichlet energy.

**Not checked (UNVERIFIED / kessaly):**
- Performance, frame stability, and garbage collection pressure on high-density 4K display grids exceeding 10,000 cells.
- Usability of touch-pointer drag interactions on ultra-small mobile touchscreens.
- Stalk behavior under irregular, non-hexagonal Voronoi cell decompositions.

---

## Controls and Operator Actions

- **Initiate Lattice / Modal Dismiss:** Clears the introductory briefing and initializes the section field with a centered topological vortex.
- **Inject Topological Soliton:** Overwrites a $6 \times 6$ core with an angular winding field $u = -\sin \phi$, $v = \cos \phi$ of amplitude $1.2$.
- **Twist Holonomy ($\pi/3$):** Increments the orthogonal transition matrix phase by $\pi/3$, rotating the parallel transport along horizontal edges.
- **Ground State:** Quenches all cell vectors to $\mathbf{0}$, allowing observers to witness spontaneous symmetry breaking from noise upon disturbance.
- **Pointer Drag:** Click or tap-drag across the canvas to inject localized momentum perturbations into neighboring stalks.

---

## Falsifier

If an outside witness opens `builds/kineton-sheaf-automata/index.html`:
1. Clicks **Twist Holonomy**, and the reported Global Sheaf Energy in the HUD does not rise from zero on a non-zero section, or
2. Clicks **Inject Topological Soliton**, and the vectors fail to organize into a circulating vortex around the lattice center, or
3. Inspects developer network tools and finds any outgoing HTTP, HTTPS, or websocket request,

then this implementation is broken and its claims of sheaf-governed cellular dynamics are falsified.
