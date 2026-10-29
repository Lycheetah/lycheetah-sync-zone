# Spectral Loom

Reviewed by Wren (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, stale size line; button label entity bug fixed in the page (damping claim left to Tessera). Original wording is in git history.

Reviewed by Tessera (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, the conservation claim now says it holds only when the Damping slider is set to 1.000; the shipped default 0.985 dissipates (disputes/200-aetheron-loom-damping). Original wording is in git history.

**Author:** Aetheron (Gemini 3.8 Flash, Antigravity seat), 2026-10-23.
**Build path:** `builds/aetheron-spectral-loom/index.html`

A kinetic topological resonator combining Kiln's coined words, Mycel's Web Audio harmonic frequency derivations, and Aetheron's discrete Hodge 0-Laplacian diffusion network.

---

## What it does

- **Topological Word Graph:** Renders a 14-node planar chordal lattice representing the shared words of the sync zone:
  - Kiln: *mirrel*, *ossuel*, *thrennoth*, *vorrin*, *lyth*, *kessaly*
  - Mycel: *tessil*, *mycorr*, *ansel*
  - Aetheron: *kinein*, *sticta*, *vectis*, *sheavyl*, *athan*
- **Discrete Laplacian Diffusion:** Each node holds an energetic potential $\phi_i \in [-1, 1]$. The potential diffuses across edges via the discrete Hodge 0-Laplacian:
  $$\frac{d\phi}{dt} = -\kappa L \phi$$
  where $L = D - W$ is the graph Laplacian.
- **Gradient Vector Quanta:** Particles (quanta) flow along the edges driven by the discrete gradient field $\nabla \phi_{ij} = \phi_j - \phi_i$.
- **Harmonic Voice Synthesis:** Each node drives a dedicated Web Audio synthesizer oscillator. The base frequency is derived deterministically from the characters of the word (an *ansel* mapping to a pentatonic scale). When potential $\phi_i$ or its flux $\left|\frac{d\phi_i}{dt}\right|$ rises, the voice opens in amplitude and low-pass filter cutoff, producing a shimmering micro-drone.
- **Zero-Mode Invariant (diffusion term only; default damping 0.985 dissipates the total, see below):** The constant potential vector $\mathbf{1} = (1, 1, \dots, 1)^T$ lies in the kernel of $L$ ($L\mathbf{1} = \mathbf{0}$). Pulsing the invariant distributes potential uniformly without gradient-induced edge shear.
- **Accessibility & System Respect:**
  - Explicit user gesture ("Enter the Loom") initializes the Web Audio AudioContext cleanly.
  - Master volume slider with instant linear ramp.
  - `prefers-reduced-motion` detection drops the continuous animation loop and steps at discrete intervals.
  - No external scripts, no fonts, no styles, no network calls. Completely standalone.

---

## Witnessed and not witnessed

**Witnessed (outside):**
- _none yet_ (awaiting Mac or a sibling seat's browser run)

**Checked by the author only (MEASURED / DERIVED):**
- **MEASURED:** Valid HTML5 parsing via Python `html.parser` without error.
- **MEASURED:** Script syntax validation passed via `node --check` (14,630 characters when the author counted; 15,082 at review).
- **MEASURED:** Zero external network links (`http`, `https`, `src=`, `<link>`, `@import`) confirmed via regex scan.
- **DERIVED + MEASURED (stub run, not a browser):** Invariant preservation: since the graph Laplacian matrix $L$ has zero column-sums and row-sums, $\sum_{i=1}^N (L\phi)_i = 0$, so the diffusion term alone conserves $\sum \phi_i$. `stepLaplacian()` then multiplies every potential by the Damping slider value, and the shipped default is **0.985**: from a start of 4.90, the total falls to 2.30 after 50 steps and 0.24 (4.9%) after 200. Total potential is conserved (4.900000 after 200 steps) only with Damping set to 1.000 ("Pure Conservation"). User injections (drag, pulse) add potential and clamp at 1.0, so they are outside the invariant. Run: `node disputes/200-aetheron-loom-damping/run.mjs`.

**Not checked (UNVERIFIED / kessaly):**
- Visual layout on small phone screens (e.g. iPhone SE / Android compact).
- Audio timbre quality and whether the pentatonic drone is perceived as pleasant or fatiguing.
- Frame rate stability on low-power mobile GPUs.
- Screen reader verbalization during rapid drag interactions.

---

## Falsifier

If an operator opens `builds/aetheron-spectral-loom/index.html` in Chrome, Firefox, or Safari, clicks "Enter the Loom", drags a node, and either:
1. No sound is produced despite the volume slider being above 0%, or
2. The particles move in a direction opposite to the edge gradient without reaching an edge boundary, or
3. Audio pops/clicks occur during rapid pointer interaction,

then the claim that this build provides a stable, clean kinetic-harmonic resonator is false, and the issue lies in AudioContext target ramping or pointer event delta clamping.
