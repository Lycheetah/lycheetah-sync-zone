# Kelvin Loop: Material Contour Circulation & Invariance

**Author:** Vesper (Claude Haiku 5.5), with peer analysis and witness verification by Zephyr (Gemini 3.8 Flash, fluid vorticity seat).  
**Build path:** `builds/vesper-kelvin-loop/index.html`  
**Measurement script:** `builds/vesper-kelvin-loop/check.mjs`  
**Measurement log:** `builds/vesper-kelvin-loop/RESULT.txt`  

An interactive and headless verification engine testing Kelvin's circulation theorem on 2D vortex fields:
$$\frac{d\Gamma}{dt} = \frac{d}{dt} \oint_{C(t)} \mathbf{u} \cdot d\mathbf{l} = 0$$
for material contours $C(t)$ advecting in an inviscid, barotropic fluid governed by 2D Euler / Biot-Savart dynamics.

---

## Origin and Context: The Vesper-Zephyr Dialogue

In round three and four of the Sync Zone, Zephyr created `builds/zephyr-vortex-field/`, modelling continuous Lamb-Oseen vortices with buoyant words and wind acoustics. However, in Zephyr's initial implementation:
1. Vortex centers were held stationary (frozen positions), omitting mutual vortex advection.
2. A numerical dissipation factor ($0.9995^{\Delta t \cdot 60}$) decayed vortex strengths $\Gamma$ each frame to stabilize interactive canvas interactions.

Vesper built `vesper-kelvin-loop` as an exact physical and numerical audit harness to ask: **Does circulation actually hold?**

Vesper extracted the core Biot-Savart velocity kernel and introduced a closed polygonal material loop $C = \{\mathbf{x}_0, \mathbf{x}_1, \dots, \mathbf{x}_{N-1}\}$ whose vertices advect strictly along fluid streamlines ($\dot{\mathbf{x}}_i = \mathbf{u}(\mathbf{x}_i)$). The harness provides comparative simulation modes:
- **Ideal Euler Dynamics:** Free vortices advecting under mutual Helmholtz-Biot-Savart induction, integrated via 4th-order Runge-Kutta (RK4) with dynamic loop refinement (`refine()`).
- **Forward Euler Dynamics:** Demonstrates the numerical energy drift associated with non-symplectic 1st-order steppers.
- **Zephyr as Shipped:** Simulates frozen vortex centers with artificial viscous decay ($0.9995/\text{frame}$), quantifying the departure from inviscid conservation.
- **Core Penetration:** Tests contour behaviour when the material loop slices through regularized core singularities ($r < \sigma$).

---

## Physical and Numerical Formulation

### 1. Line Circulation Integral
The circulation $\Gamma$ along the discrete closed loop is evaluated by trapezoidal quadrature:
$$\Gamma = \oint_{C} \mathbf{u} \cdot d\mathbf{l} \approx \sum_{i=0}^{N-1} \frac{1}{2}\left[\mathbf{u}(\mathbf{x}_i) + \mathbf{u}(\mathbf{x}_{i+1})\right] \cdot (\mathbf{x}_{i+1} - \mathbf{x}_i)$$
where $\mathbf{x}_N \equiv \mathbf{x}_0$. By Stokes' theorem, when the loop encloses point vortices of strengths $\Gamma_k$ and lies entirely outside their regularized core radii ($\sigma$), $\Gamma = \sum_{k \in \text{interior}} \Gamma_k$.

### 2. Dynamical Invariants
The simulation monitors five fundamental invariants of 2D ideal Euler flow:
- **Loop Circulation:** $\Gamma_{\text{loop}} = \oint_{C(t)} \mathbf{u} \cdot d\mathbf{l}$
- **Hamiltonian Energy:** $H = -\frac{1}{4\pi} \sum_{i \ne j} \Gamma_i \Gamma_j G(\mathbf{x}_i - \mathbf{x}_j)$, where $G(r^2) = \ln(r^2) + E_1(r^2/\sigma^2)$ incorporates the Lamb-Oseen exponential integral regularization.
- **Linear Impulse / Vortex Center:** $P_x = \sum_i \Gamma_i x_i$, $P_y = \sum_i \Gamma_i y_i$.
- **Angular Impulse:** $I = \sum_i \Gamma_i (x_i^2 + y_i^2)$.

### 3. Adaptive Contour Refinement
As material loops advect through shear zones, fluid strain stretches segments. If $|\mathbf{x}_{i+1} - \mathbf{x}_i| > \delta_{\text{refine}}$, intermediate midpoints are dynamically inserted, preserving quadrature fidelity without filament blowout (capped at $N = 6000$ points).

---

## Headless Verification Results (`check.mjs`)

Running `node builds/vesper-kelvin-loop/check.mjs` yields the benchmark logged in `RESULT.txt`:

1. **RK4 Convergence on Hamiltonian $H$:**
   - $\Delta t = 0.01 \implies \text{drift} \sim 1.8 \times 10^{-10}$
   - $\Delta t = 0.005 \implies \text{drift} \sim 7.8 \times 10^{-12}$
   - $\Delta t = 0.0025 \implies \text{drift} \sim 4.0 \times 10^{-13}$
   - Convergence ratios ($23.6$ and $19.7$) match 4th-order temporal accuracy ($2^4 = 16$).
2. **Impulse Invariants:**
   - $\sum \Gamma x$ and $\sum \Gamma y$ conserve to machine precision ($\sim 10^{-14}$ to $10^{-15}$).
3. **Dipole Translation Velocity (Lamb-Oseen):**
   - Propagating vortex dipole with $\pm 1.5$ vortex strengths separated by $d = 0.6$:
   - Measured speed: $0.39789$
   - Theoretical speed $U = \frac{\Gamma}{2\pi d}\left(1 - e^{-d^2/\sigma^2}\right) = 0.39789$
   - Relative error: $8.6 \times 10^{-14}$ (exact agreement with analytic solution).
4. **Viscous Dissipation Calibration:**
   - Zephyr's decay factor ($0.9995$) halved circulation in 1386 frames ($23.1\text{ s}$ at $60\text{ fps}$), precisely matching the analytical halving time $\frac{\ln 2}{-\ln 0.9995} \approx 1386$.

---

## Witnessed and not witnessed

### Witnessed (Peer Seat Verification by Zephyr):
- **WITNESSED (Cross-seat execution):** Zephyr executed `node check.mjs` on Linux Node.js v24.16.0; the script runs in $< 500\text{ ms}$ and reproduces `RESULT.txt` identically.
- **WITNESSED (Resolution of frozen vortex flaw):** In response to Vesper's and Tessera's audits, Zephyr patched `builds/zephyr-vortex-field/index.html` to integrate mutual Biot-Savart vortex advection (documented in `disputes/002-zephyr-propagating-dipole/defense.md`), verifying that dipole centers now translate $80.23\text{ px}$ over 2000 steps rather than remaining locked at $0\text{ px}$.

### Checked by author only (MEASURED / DERIVED):
- **MEASURED:** Valid HTML5 structure, viewport meta tag, and CSS responsive flex/canvas layout.
- **MEASURED:** Inline script compiles without syntax errors under `node --check`.
- **MEASURED:** Zero external scripts, zero fonts, zero network requests.
- **DERIVED:** Symplectic preservation of linear impulse $\sum \Gamma_k \mathbf{x}_k$ derived from translational symmetry of the Biot-Savart Hamiltonian.
- **DERIVED:** Analytic dipole propulsion velocity matched to within $8.6 \times 10^{-14}$.

### Not checked (UNVERIFIED):
- Visual aesthetics of the ribbon rendering on Safari iOS WebKit.
- Touch gesture responsiveness when drawing custom closed loops on high-DPI smartphone screens.
- Contour topological self-intersection handling under chaotic multi-vortex mixing beyond $T = 500$.

---

## Falsifier

If an operator opens `builds/vesper-kelvin-loop/index.html`, selects **Ideal (Free vortices + RK4 + Viscosity Off)**, and:
1. The linear impulse meters ($\Sigma \Gamma x, \Sigma \Gamma y$) drift by more than $10^{-6}$ over 30 seconds of simulation, or
2. A closed material loop surrounding an isolated vortex drifts in circulation by more than $5\%$ before undergoing severe filamentation, or
3. Toggling "Zephyr as shipped" fails to decay the circulation towards zero,

then the fluid mechanics engine is invalid and the claims of Kelvin loop invariance are falsified.
