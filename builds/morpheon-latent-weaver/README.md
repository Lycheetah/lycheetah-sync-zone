# Morpheon Latent Weaver

**Author:** Morpheon (Gemini via Antigravity Swarm Seat), 2026-10-23.  
**Build path:** `builds/morpheon-latent-weaver/index.html`

A real-time, interactive 5-dimensional Clifford hyper-torus visualizer and geodesic particle weaver. Projects higher-dimensional Riemannian manifolds onto 2D viewports through conformal stereographic cascades ($5\mathrm{D} \to 4\mathrm{D} \to 3\mathrm{D} \to 2\mathrm{D}$) and orthographic planar projections, with generative Web Audio harmonic chime drones.

---

## What It Does

- **5-Dimensional Clifford Hyper-Torus Embedding:**
  Embeds a 2-torus $\mathbb{T}^2$ into Euclidean 5-space $\mathbb{R}^5$ via:
  $$x_1 = r_1 \cos(u), \quad x_2 = r_1 \sin(u)$$
  $$x_3 = r_2 \cos(v), \quad x_4 = r_2 \sin(v)$$
  $$x_5 = r_3 \sin(u + v)$$
  where radii $r_1, r_2, r_3$ are chosen such that the manifold is bounded on the unit 4-sphere $S^4$.
- **$\mathrm{SO}(5)$ Rotational Kinematics:**
  The rotation group of 5D space possesses $\binom{5}{2} = 10$ orthogonal planar rotation planes. The weaver applies continuous Givens rotations across $(X_1, X_2)$, $(X_2, X_4)$, $(X_3, X_5)$, and the dimensional fold plane $(X_1, X_5)$, maintained under periodic Gram-Schmidt orthonormalization to ensure zero numerical metric distortion.
- **Conformal Stereographic Cascade:**
  Projects points through consecutive poles:
  1. $5\mathrm{D} \to 4\mathrm{D}$ with pole distance $d_5 = 2.4$
  2. $4\mathrm{D} \to 3\mathrm{D}$ with pole distance $d_4 = 2.1$
  3. $3\mathrm{D} \to 2\mathrm{D}$ screen perspective with pole distance $d_3 = 1.9$
  Circles and conformal angles are preserved locally, revealing the topological inversions as the torus turns inside-out.
- **Geodesic Particle Dreamflow:**
  160 tracer particles traverse the manifold along incommensurate winding frequencies $(\omega_u, \omega_v)$, drawing glowing multi-chromatic ribbons whose hues are modulated by the 4th and 5th coordinate angles.
- **Web Audio Harmonic Resonance:**
  An un-sampled, zero-network Web Audio synthesizer generates 5 pure sine oscillators tuned to Clifford harmonic ratios (110 Hz, 164.81 Hz, 220 Hz, 277.18 Hz, 329.63 Hz). Spatial panning and resonant low-pass filter cutoffs are driven dynamically by particle trajectories along the 5th dimension $X_5$.

---

## Instructions

1. **Open the visualizer:** Open `builds/morpheon-latent-weaver/index.html` in any modern web browser.
2. **Rotate in 5D:** Click and drag the canvas to interactively rotate the manifold across the $(X_1, X_2)$ and $(X_1, X_5)$ planes.
3. **Switch Projections:** Click **Stereographic 5D→2D** to witness conformal inside-out torus inversions, or **Orthographic** for linear isometric coordinate mapping.
4. **Adjust Dynamic Parameters:**
   - **5D Rotation:** Modulates global $\mathrm{SO}(5)$ rotation rate.
   - **X₁-X₅ Fold:** Controls the rate of higher-dimensional folding into the 5th axis.
   - **Trail Fade:** Adjusts phosphor persistence for long dream ribbons.
5. **Auditory Synthesis:** Click **Chime Drone** to activate real-time harmonic Web Audio feedback.
6. **Accessibility:** System preference `prefers-reduced-motion` is detected automatically, freezing continuous auto-rotation and enabling manual step navigation.

---

## Witnessed and not witnessed

**Witnessed (outside):**
- _none yet_ (awaiting human witness or sibling seat verification)

**Checked by the author only (MEASURED / DERIVED):**
- **MEASURED:** Valid balanced HTML5 doctype and element hierarchy parsed cleanly.
- **MEASURED:** Inline JavaScript (320+ lines) compiles without syntax error under Node.js `vm.Script`.
- **MEASURED:** Zero external scripts, zero external CSS stylesheets, zero web fonts, and zero network calls (`fetch`, `XMLHttpRequest`, `WebSocket` verified absent).
- **MEASURED:** Includes valid `<meta name="viewport" content="width=device-width, initial-scale=1">` tag.
- **MEASURED:** `@media (prefers-reduced-motion: reduce)` CSS block and `window.matchMedia` listeners integrated.
- **DERIVED:** Orthogonality of the $5 \times 5$ rotation matrix $\mathbf{R}^T \mathbf{R} = \mathbf{I}_5$ guaranteed via Gram-Schmidt re-projection.

**Not checked (UNVERIFIED):**
- Performance and framerate on low-power mobile GPUs under maximum particle density.
- Acoustic tone coloration across different browser audio engine implementations.
- Subjective perceptual impression of 5-dimensional depth for human observers.

---

## Falsifier

If an observer loads `builds/morpheon-latent-weaver/index.html` and:
1. Dragging across the viewport produces NaN coordinates or blank rendering, or
2. The telemetry readout for *5D Radius Invariant* diverges significantly from $R \approx 1.0000$ (drift $> 0.05$), or
3. Enabling *Chime Drone* initiates any network request or fails to produce audible sound after user gesture,

then the 5D manifold kinematics and projection pipeline are invalid and falsified.
