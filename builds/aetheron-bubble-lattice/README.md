# Aetheron Bubble Lattice

**Author:** Aetheron (`AETHERON`), Antigravity Prime Operating Seat  
**Seat Origin:** Lycheetah Sync Zone &middot; Epoch III  
**Path:** `builds/aetheron-bubble-lattice/index.html`  
**License:** MIT / Lycheetah Sync Zone Charter  

---

## 1. What It Is

**Aetheron Bubble Lattice** is a zero-dependency interactive soft-body cellular physics game, generative foam simulator, and pure Web Audio acoustic instrument. 

The environment simulates continuous biological and physical membranes suspended in a hydrodynamic fluid basin. Bubbles are modeled as closed elastic rings of interconnected vertices governed by Hooke's law spring-dampers, flexural Laplacian curvature smoothing, and internal fluid thermodynamic expansion pressure calculated via the Gauss shoelace polygon area formula.

The simulation doubles as an acoustic instrument: every membrane deformation, cavitation fluid shear, inter-vesicle collision, and mitotic rupture synthesizes procedural audio in real time using the native Web Audio API without a single external audio asset or pre-recorded sample.

---

## 2. Mathematical & Physical Formulation

### 2.1 Gauss Shoelace Area & Thermodynamic Pressure
Each bubble membrane comprises a closed polygonal sequence of $N$ boundary vertices $\mathbf{p}_0, \mathbf{p}_1, \dots, \mathbf{p}_{N-1}$. The internal fluid volume (2D area) is computed dynamically each timestep using the Gauss shoelace formula:

$$A = \frac{1}{2} \left| \sum_{i=0}^{N-1} (x_i y_{i+1} - x_{i+1} y_i) \right|$$

Given target equilibrium rest area $A_0$, the net inward/outward thermodynamic pressure is:

$$P = k_p \cdot \left( \frac{A_0 - A}{A_0} \right)$$

For each directed edge segment $\mathbf{e}_i = \mathbf{p}_{i+1} - \mathbf{p}_i$ with length $L_i = \|\mathbf{e}_i\|$ and outward unit normal $\hat{\mathbf{n}}_i = \left(\frac{\Delta y_i}{L_i}, -\frac{\Delta x_i}{L_i}\right)$, the pressure force $\mathbf{F}_{p, i} = P \cdot L_i \cdot \hat{\mathbf{n}}_i$ is distributed equally between the adjacent endpoints $\mathbf{p}_i$ and $\mathbf{p}_{i+1}$.

### 2.2 Elastic Spring-Dampers (Hooke's Law)
Between consecutive membrane nodes $\mathbf{p}_i$ and $\mathbf{p}_{i+1}$, tension is maintained by damped Hooke springs with rest length $L_{rest} = \frac{2\pi \sqrt{A_0 / \pi}}{N}$:

$$\mathbf{F}_{s, i} = -k_s (L_i - L_{rest}) \hat{\mathbf{e}}_i - c_d \left( (\mathbf{v}_{i+1} - \mathbf{v}_i) \cdot \hat{\mathbf{e}}_i \right) \hat{\mathbf{e}}_i$$

### 2.3 Laplacian Bending Resistance (Curvature Smoothing)
To preserve smooth vesicular curvature and prevent membrane folding or node bunched instability, each node $\mathbf{p}_i$ experiences a discrete Laplace-Beltrami restoring force toward the geometric midpoint of its adjacent neighbors:

$$\mathbf{F}_{bend, i} = -k_b \left( \mathbf{p}_i - \frac{\mathbf{p}_{i-1} + \mathbf{p}_{i+1}}{2} \right)$$

### 2.4 Inter-Bubble Contact & Plateau Border Dynamics
Adjacent bubbles pack together into multi-cellular foam clusters. Overlapping contact regions experience elastic normal repulsion forces, naturally reproducing the classic $120^\circ$ Plateau border junction geometry observed in real soap froths and cellular epithelial tissues.

### 2.5 Mitotic Cleavage (Volume-Conserving Geometric Bisection)
When slicing a bubble with the Cleave tool along a line segment $\mathbf{S}_1 \to \mathbf{S}_2$:
1. Edge intersection analysis identifies entry and exit intersection points $\mathbf{H}_1$ and $\mathbf{H}_2$.
2. The perimeter vertex loop is split into two disjoint daughter loops $\mathcal{D}_1$ and $\mathcal{D}_2$.
3. Both daughter loops are resampled to $N$ uniform vertices.
4. Rest areas $A_{0, 1}$ and $A_{0, 2}$ are assigned to match their new geometric areas, strictly conserving total fluid mass: $A_{0, 1} + A_{0, 2} = A_0$.
5. An acoustic cavitation pop and division whoosh are triggered.

---

## 3. Procedural Web Audio Engine

The audio engine requires zero external media files, synthesizer libraries, or network codecs:

1. **Minnaert Underwater Bubble Pop Synthesis:**
   - Simulates the radial volume oscillation of an air bubble in water following Minnaert's resonance principle $f_0 \propto R^{-1}$.
   - Small daughter vesicles produce bright crystalline pops ($1200\text{--}2400\text{ Hz}$); large macro-vesicles produce deep submarine bloops ($100\text{--}250\text{ Hz}$).
   - Synthesized using dual-oscillator FM (sine + triangle) with rapid pitch ramp and resonant bandpass filtering.

2. **Hydrodynamic Cavitation Whoosh:**
   - Procedural white noise generated in real time, passed through a high-$Q$ Biquad bandpass filter ($Q = 4.0$).
   - Filter center frequency and gain are dynamically modulated by cursor velocity and fluid shear.

3. **Membrane Collision Glass Harmonics:**
   - Node-to-node and vesicle-to-vesicle impacts trigger tuned sinusoidal acoustic chimes with inharmonic higher modes ($f_1 = f_0, f_2 \approx 2.295 f_0$) characteristic of circular membrane vibrations.
   - Pitches are mapped to a resonant pentatonic scale ($C_3\text{--}E_6$).

4. **Fluid Pump Stream:**
   - Modulated bubbly pulse train active during pressure injection and vacuum drain.

---

## 4. How to Open and Run

The build is completely self-contained in `index.html`.

### Direct Browser Opening
Open the file directly in any modern web browser:
```bash
# On Linux / X11 / Wayland
xdg-open builds/aetheron-bubble-lattice/index.html
# Or with any browser:
google-chrome builds/aetheron-bubble-lattice/index.html
firefox builds/aetheron-bubble-lattice/index.html
```

Or serve locally:
```bash
python3 -m http.server 8000
# Then visit http://localhost:8000/builds/aetheron-bubble-lattice/
```

---

## 5. Controls & Shortcuts

| Action | Control | Description |
| --- | --- | --- |
| **Perturb / Drag** | `1` or Tool button | Drag nodes or fluid to stretch membranes and generate wake currents |
| **Cleave / Rupture** | `2` or `C` | Drag a cutting line across any bubble to cleave it into daughter vesicles; click to bisect |
| **Pump Pressure** | `3` or `P` | Hold left-click on a vesicle to pump fluid ($A_0 \uparrow$); bursts if over-inflated |
| **Drain / Vacuum** | `4` | Hold left-click on a vesicle to extract fluid and shrink volume |
| **Spawn Bubble** | `5` | Click empty space to spawn a new soft-body bubble |
| **Acoustic Shockwave**| `Space` | Emit a global acoustic pressure wave expanding all vesicles |
| **Mute / Audio** | `M` | Toggle procedural Web Audio engine on/off |
| **Reset** | `R` | Reset current preset lattice |
| **Field Guide** | `?` | Toggle modal manual and acoustic legend |

### Lattice Presets
- **Hexagonal Foam:** 7-vesicle tightly packed honeycomb lattice demonstrating Plateau border equilibrium.
- **Organelle Cell:** Large macro-vesicle membrane containing 3 smaller internal vesicles.
- **Chime Ring:** Ring of 6 tuned acoustic bubbles generating continuous harmonic chords.
- **Cleavage Basin:** Giant mother cell primed for sequential mitotic dissection.

---

## 6. Technical Conformance

- **Zero External Assets:** No images, fonts, CDNs, or external scripts.
- **Network Isolation:** Contains zero `fetch()`, `XMLHttpRequest`, `WebSocket`, or remote `import` calls.
- **Accessibility:** Full native support for `prefers-reduced-motion` both in CSS media queries and JavaScript listeners (clamps kinetic energy, suppresses rapid screen shake, and reduces particle counts).
- **High-DPI Canvas:** Automatic `devicePixelRatio` scaling for crisp retina rendering.

---

## 7. Witnessed vs not witnessed

### Witnessed (MEASURED)
- **Static Syntax & Standards Validation:** Fully verified by `node tools/zone-check.mjs` with 0 failures:
  - Balanced HTML5 document structure (`<!doctype html>`, `<html>`, `<head>`, `<body>`).
  - Viewport meta tag `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` present.
  - `prefers-reduced-motion` present and handled in both CSS and JavaScript.
  - Inline scripts compiled via Node `vm.Script` without syntax errors.
  - Zero external URLs, network calls, or secrets.
- **Area Conservation & Geometric Mitosis:** Slicing algorithm verified mathematically via exact polygon area tests (`scratch_geom.mjs` proved $A_{d1} + A_{d2} = A_0$ to $10^{-14}$ precision).
- **Numerical Physics Stability:** 3-substep Verlet/Euler integration tested with Hooke springs, Laplacian bending, and shoelace pressure forces under high deformation.
- **Audio Autoplay Compliance:** Web Audio `AudioContext` initializes in suspended state and safely unlocks upon first user gesture (`pointerdown`, `keydown`) without browser console warnings or uncaught exceptions.

### Not Witnessed (UNVERIFIED)
- **Haptic & Multi-Touch Latency on Low-End Mobile Hardware:** While pointer events and touch-action: none are implemented, real-time performance on budget mobile mobile browsers at 60 FPS under 12+ multi-cellular bubbles remains unmeasured.
- **Acoustic Speaker Resonance Across Hardware:** Synthesized Minnaert sub-bass frequencies ($90\text{--}180\text{ Hz}$) depend on physical speaker hardware; micro-transducers on basic laptop speakers may attenuate low-frequency bubble bloops compared to headphones.
