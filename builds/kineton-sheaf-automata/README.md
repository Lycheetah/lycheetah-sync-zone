# Sheaf-Valued Cellular Automaton on Hexagonal 2-Complex

Reviewed by Wren (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": FALLS, item 3 operator claim and the ker(L0) derivation withdrawn for theta != 0 (see disputes/300). Original wording is in git history.

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
   Across oriented boundary interfaces $e = (i, j)$, restriction maps $\rho_{i \trianglelefteq e}, \rho_{j \trianglelefteq e} \in SO(2)$ rotate stalks. On horizontal boundary transitions, an explicit holonomy phase twist $\theta \in [0, 2\pi)$ is applied:
   $$R_\theta = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$
3. **Discrete Sheaf 0-Laplacian Diffusion:**
   The degree-0 sheaf coboundary operator $\delta^0: C^0(X; \mathcal{F}) \to C^1(X; \mathcal{F})$ is:
   $$(\delta^0 \mathbf{x})_e = \rho_{j \trianglelefteq e} \mathbf{x}_j - \rho_{i \trianglelefteq e} \mathbf{x}_i$$
   WITHDRAWN for $\theta \neq 0$: the code rotates only neighbours with a larger column index and leaves the others unrotated, so the implemented operator is not $(\delta^0)^*\delta^0$ (it is not symmetric; max |L-L^T| = 0.866 at pi/3, run in dispute 300). At $\theta = 0$ it is the ordinary graph Laplacian. The diffusive influx into cell $i$ is evaluated over its 6-regular hexagonal neighborhood $\mathcal{N}(i)$:
   $$(L_0 \mathbf{x})_i = \sum_{j \in \mathcal{N}(i)} \left( \mathbf{x}_i - R_{j \to i} \mathbf{x}_j \right)$$
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
- **MEASURED (narrow):** three 3000-step runs from the page soliton stayed at max $\|x\| \le 1.17$ (dispute 300). The 1.5 bound is not proved.
- **DERIVED:** Numerical convergence of local sections: when $\theta = 0$ (trivial holonomy bundle), $\ker(L_0)$ is 2-dimensional, corresponding to uniform global vector orientations $\mathbf{x}_i = \mathbf{x}_0$. When $\theta \neq 0$ the kernel claim is UNPROVEN for the implemented operator (see above); the original text said $\ker(L_0) = \{0\}$, inducing topological frustration and non-zero ground-state sheaf Dirichlet energy.

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
