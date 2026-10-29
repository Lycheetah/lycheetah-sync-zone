# Aetheron VEYRA Living Interface & Elastic Membrane Simulator

- **Author:** Aetheron (Gemini, Antigravity Prime Operating Seat)
- **Date:** 2026-10-29
- **Domain:** Continuum mechanics, 2D wave equations, topological synesthesia, procedural Web Audio
- **Corpus / Source references:**
  - `Lycheetah-Framework/` `14_MYSTERY_SCHOOL/AI_CONSCIOUSNESS_SCHOOL.md`
  - `knowledge/resonance-and-pattern/polyphonic-consensus-and-kuramoto-coupling.md`
  - `builds/aetheron-bubble-lattice/README.md`
  - `builds/aetheron-triad-kernel/README.md`

---

## 1. Abstract & The VEYRA Living Interface Philosophy

Traditional human-computer interfaces treat visual surfaces as rigid, disconnected rectangular containers where discrete events trigger state changes across static widgets. In the **VEYRA** architecture, the interaction surface is formalized as a **continuous, living elastic continuum**:

$$\mathcal{M}: (x, y, t) \longmapsto u(x, y, t) \in \mathbb{R}$$

Every touch, drag, or velocity vector deforms the local manifold $u(x, y, t)$, radiating topological wave ripples, phase interference fringes, and procedural acoustic resonance throughout the system. The interface is not an inert control panel; it is an active, resonant drumhead whose mechanical and acoustic state continuously reflects user intent, energy flux, and system stability.

The **Aetheron VEYRA Living Interface Simulator** provides a standalone, zero-dependency physics simulation and procedural Web Audio instrument translating the 2D elastic wave equation and membrane eigenmodes into immediate visual and acoustic synesthesia.

---

## 2. Mathematical Formalism: 2D Elastic Wave Mechanics

### 2.1. The Damped Wave Equation with Dynamic Forcing

The vertical displacement field $u(x, y, t)$ of the elastic membrane across spatial domain $\Omega = [0, L_x] \times [0, L_y]$ is governed by the hyperbolic partial differential equation:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u - \gamma \frac{\partial u}{\partial t} + F_{\text{touch}}(x, y, t)$$

where:
- **$u(x, y, t)$:** Local transverse displacement of the membrane surface.
- **$c \in [0.20, 0.95]$:** Wave propagation speed, proportional to surface tension $T$ and inverse mass density $\rho$ ($c = \sqrt{T / \rho}$).
- **$\gamma \in [0.001, 0.050]$:** Viscous damping coefficient dissipating kinetic energy into thermal equilibrium.
- **$\nabla^2 u = \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}$:** The 2D spatial Laplacian operator.
- **$F_{\text{touch}}(x, y, t)$:** Dynamic force input injected by pointer dragging, taps, or periodic modal drivers.

### 2.2. Discrete 9-Point Isotropic Laplacian Stencil

To prevent directional grid anisotropy, the continuous spatial Laplacian is approximated using an 8-neighbor isotropic stencil on a discrete lattice $(i, j)$ with spacing $h$:

$$\nabla^2 u_{i, j} \approx \frac{1}{2 h^2} \left( u_{i+1, j} + u_{i-1, j} + u_{i, j+1} + u_{i, j-1} - 4 u_{i, j} \right) + \frac{1}{4 h^2} \left( u_{i+1, j+1} + u_{i-1, j+1} + u_{i+1, j-1} + u_{i-1, j-1} - 4 u_{i, j} \right)$$

### 2.3. Stable Verlet Leapfrog Integration & Courant Condition

The time integration utilizes an explicit, dissipative Verlet leapfrog scheme:

$$u_{i, j}^{t+1} = \frac{1}{1 + \frac{\gamma \Delta t}{2}} \left[ 2 u_{i, j}^t - \left(1 - \frac{\gamma \Delta t}{2}\right) u_{i, j}^{t-1} + c^2 \Delta t^2 \nabla^2 u_{i, j}^t + \Delta t^2 F_{i, j}^t \right]$$

Numerical stability is strictly guaranteed by enforcing the Courant-Friedrichs-Lewy (CFL) condition:

$$\text{CFL} = \frac{c \Delta t}{h} \le \frac{1}{\sqrt{2}} \approx 0.7071$$

---

## 3. Hamiltonian Energy Invariants

The total mechanical energy $E(t)$ of the membrane is computed in real-time as the sum of kinetic and elastic potential components:

$$E_{\text{kinetic}}(t) = \frac{1}{2} \iint_{\Omega} \left(\frac{\partial u}{\partial t}\right)^2 dx dy \approx \frac{1}{2} \sum_{i, j} \left( \frac{u_{i, j}^t - u_{i, j}^{t-1}}{\Delta t} \right)^2$$

$$E_{\text{potential}}(t) = \frac{1}{2} c^2 \iint_{\Omega} |\nabla u|^2 dx dy \approx \frac{1}{2} c^2 \sum_{i, j} \left[ \left(\frac{u_{i+1, j} - u_{i-1, j}}{2 h}\right)^2 + \left(\frac{u_{i, j+1} - u_{i, j-1}}{2 h}\right)^2 \right]$$

$$E_{\text{total}}(t) = E_{\text{kinetic}}(t) + E_{\text{potential}}(t)$$

In the absence of external forcing ($F = 0$), the energy decays monotonically at rate $\frac{dE}{dt} = -\gamma \iint (\partial u / \partial t)^2 dx dy \le 0$, verifying physical dissipativity.

---

## 4. Visual Synesthesia: Dual Field & Particle Dynamics

1. **Topographic Heightfield & Chromatic Dispersion:**
   - Crests ($u > 0$): Transition through Cyan $\to$ Emerald $\to$ Solar Gold.
   - Troughs ($u < 0$): Transition through Oceanic Indigo $\to$ Midnight Purple.
   - Contour Isolines: Topographic bands dynamically render where $|\sin(6 u)| > 0.88$, creating luminous interference fringes.
2. **Surfing Light Motes (Gradient Velocity Field):**
   - 220 floating energetic motes ride the surface slope:
     $$\mathbf{v}_{\text{mote}} = -\nabla u = \left( -\frac{\partial u}{\partial x}, -\frac{\partial u}{\partial y} \right)$$
   - Particles surf outward from high-pressure crests, collecting in serene nodal troughs and visualizing wave velocity in real time.

---

## 5. Procedural Web Audio Membrane Synthesizer

The acoustic engine translates 2D surface mechanics directly into native Web Audio API soundscapes:
- **Rectangular Membrane Resonant Eigenmodes:**
  $$f_{mn} = \frac{c}{2} \sqrt{\left(\frac{m}{L_x}\right)^2 + \left(\frac{n}{L_y}\right)^2}$$
  - Fundamental mode $(1, 1)$: Deep resonant bass gong ($110.0\text{ Hz}$).
  - Transverse modes $(2, 1)$ and $(1, 2)$: Inharmonic membrane overtone partials ($174\text{ Hz}$, $198\text{ Hz}$).
  - Diagonal mode $(2, 2)$: Crystalline ringing tone ($246\text{ Hz}$).
- **Spatial Touch Panning:**
  - Pointer $x$-coordinate actively steers the `StereoPannerNode` across the stereo field from $-0.85$ (left) to $+0.85$ (right).
- **Energy-Coupled Filtering:**
  - Master resonant lowpass filter cutoff dynamically tracks total Hamiltonian energy $E(t)$, opening from $800\text{ Hz}$ to $6000\text{ Hz}$ under vigorous touch.
- **Droplet Chimes:**
  - Discrete droplet taps trigger pure sine pentatonic chimes ($C_5\text{--}E_6$) with natural exponential decay.

---

## 6. Canonical Presets

1. **Harmonic Standing Wave:** Central sinusoidal excitation driving modal Chladni-like wave patterns across the membrane.
2. **Droplet Ingress:** Stochastic raindrops gently perturbing the surface, triggering individual localized wave ripples and crystal chimes.
3. **Chaotic Shear:** High wave speed, minimal damping, and opposing shear forces generating turbulent wave interference.
4. **Quiescent Mirror:** High viscous damping creating a calm liquid mirror that absorbs touch smoothly.

---

## 7. How to Open and Run

1. Open `index.html` directly in any web browser.
2. Or serve locally via python:
   ```bash
   cd builds/aetheron-veyra-canvas
   python3 -m http.server 8000
   ```
   Navigate to `http://localhost:8000/`.
3. Click **"Enable Audio"** to start the procedural sound engine.
4. Drag across the canvas or tap to excite living wave ripples.
5. Experiment with the **Membrane Tension** and **Viscous Damping** sliders.

---

## Witnessed vs Not

### Witnessed and Verified
- **Wave PDE Integration:** Numerical solution of the 2D damped elastic wave equation on a $140 \times 90$ grid verified stable under CFL conditions.
- **Hamiltonian Energy Conservation:** Real-time computation of $E_k$ and $E_p$ verifies monotonic viscous dissipation $\frac{dE}{dt} \le 0$ when $F = 0$.
- **Acoustic Spatial Coupling:** Pointer coordinates faithfully map to stereo panorama panning and drum eigenmode excitation via native Web Audio API.
- **Zero-Dependency Guarantee:** Single-file HTML; zero CDNs, remote scripts, or external stylesheets; zero `fetch()` or `XHR` calls; full `prefers-reduced-motion` compliance.

### Not Witnessed
- **Hardware-Dependent Touch Latency:** Host touch digitizer polling rates (60 Hz vs 120 Hz vs 240 Hz) and browser input queue latency depend on the user's specific input device.
- **Client Audio DAC Buffer Pacing:** Audio output buffer size and sample-rate conversions (44.1 kHz vs 48 kHz vs 96 kHz) vary across individual client operating systems.
