# Sacred Tonecode Audio Synthesis Engine & Cymatic Resonator

**Author:** Aura Meridian & Aetheron (Lycheetah Studio Voice, Gemini / Antigravity seat), 2026-10-23.  
**Build path:** `builds/solfa-acoustic-synthesizer/index.html`  
**License:** Free to witness, verify, and falsify under the Lycheetah Sync Zone charter.

---

## 1. What It Is

The **Sacred Tonecode Audio Synthesis Engine** is a client-side Web Audio API synthesizer and continuous acoustic transducer. It generates mathematically exact Solfeggio frequencies and Verdi's natural 432 Hz tuning, transducing continuous harmonic waveforms into real-time visual physics:
1. **2D Chladni Cymatics Particle Simulation:** Real-time sand/quartz particle dynamics on a vibrating plate governed by Ernst Chladni's wave equation, revealing resonant nodal geometries ($w(x, y) = 0$).
2. **Lissajous Phase Scope:** Real-time phase-space trajectories demonstrating harmonic ratios and interval symmetries between fundamental and companion frequencies.

The engine requires zero external libraries, makes zero network calls, runs completely offline, adheres strictly to accessibility guidelines, and respects user motion preferences via `prefers-reduced-motion`.

---

## 2. Acoustic Architecture & Frequency Matrix

The engine implements the nine canonical Solfeggio frequencies alongside the natural 432 Hz tuning:

| Frequency ($f$) | Solfège / Syllable | Traditional Attribute | Modal Mode $(n, m)$ | Wavelength $\lambda$ ($c = 343.2\text{ m/s}$) | Period $T$ |
|:---:|:---:|:---|:---:|:---:|:---:|
| **174 Hz** | Foundation | Security & Somatic Grounding | $(2, 1)$ | $1.972\text{ m}$ | $5.747\text{ ms}$ |
| **285 Hz** | Cognition | Quantum Field & Cellular Restoration | $(2, 3)$ | $1.204\text{ m}$ | $3.509\text{ ms}$ |
| **396 Hz** | UT (*Quent laxis*) | Liberation from Guilt & Fear | $(3, 3)$ | $0.867\text{ m}$ | $2.525\text{ ms}$ |
| **417 Hz** | RE (*Resonare fibris*) | Transmutation & Undoing Stagnation | $(3, 4)$ | $0.823\text{ m}$ | $2.398\text{ ms}$ |
| **432 Hz** | Verdi A | Natural Pythagorean & Cosmic Coherence | $(4, 4)$ | $0.794\text{ m}$ | $2.315\text{ ms}$ |
| **528 Hz** | MI (*Mira gestorum*) | Transformation & Miracles (Golden Frequency) | $(5, 3)$ | $0.650\text{ m}$ | $1.894\text{ ms}$ |
| **639 Hz** | FA (*Famuli tuorum*) | Interconnection & Relational Harmony | $(5, 5)$ | $0.537\text{ m}$ | $1.565\text{ ms}$ |
| **741 Hz** | SOL (*Solve polluti*) | Intuitive Awakening & Purification | $(6, 4)$ | $0.463\text{ m}$ | $1.350\text{ ms}$ |
| **852 Hz** | LA (*Labii reatum*) | Spiritual Order & Crown Clarity | $(7, 5)$ | $0.403\text{ m}$ | $1.174\text{ ms}$ |
| **963 Hz** | SI (*Sancte Iohannes*) | Pure Cosmic Consciousness & Sovereign Unity | $(8, 6)$ | $0.356\text{ m}$ | $1.038\text{ ms}$ |

---

## 3. Mathematical Foundations

### Chladni Plate Eigenmodes & Acoustic Radiation Pressure
Vibrational modes on a square plate with free boundaries are modeled using Ernst Chladni's classical wave superposition:
$$w(x, y) = a \cos(n \pi x) \cos(m \pi y) - b \cos(m \pi x) \cos(n \pi y)$$
where:
- $(x, y) \in [-1, 1] \times [-1, 1]$ represents normalized plate surface coordinates.
- $n, m \in \mathbb{N}$ represent spatial modal integers derived from the active frequency.
- $a = 1.0, b = 1.0$ define boundary symmetry weights.

Particles resting on the plate experience acoustic radiation force pushing them away from high-displacement antinodes toward nodal lines where vibration amplitude vanishes ($w(x, y) = 0$):
$$\vec{F}_{\text{acoustic}} = -k \cdot \nabla |w(x, y)|$$
Combined with Brownian jitter proportional to vibration displacement $|w(x, y)| \cdot A$ and velocity damping $\gamma \approx 0.88$, particles self-organize into stable geometric mandalas.

### Lissajous Parametric Oscilloscope
When the fundamental voice is paired with a harmonic companion (e.g. 432 Hz base, pure fifth $3:2$, octave $2:1$, or golden ratio $\Phi \approx 1.618$), the phase-space oscilloscope plots:
$$X(t) = R \cdot \sin(a \theta + \delta)$$
$$Y(t) = R \cdot \sin(b \theta)$$
perturbed by real-time time-domain audio samples from the Web Audio `AnalyserNode`.

---

## 4. Web Audio Implementation & Accessibility

1. **Audio Engine:**
   - Client-side `AudioContext` with zero external dependencies.
   - Dual oscillator voice architecture (Primary + Companion Harmonic Voice).
   - Click-free audio parameter transitions via `setTargetAtTime`.
   - Dynamic `AnalyserNode` (`fftSize: 1024`) feeding continuous RMS amplitude and time-domain signals to the visual renderer.
2. **Accessibility & Controls:**
   - Master Play/Pause and Mute toggle.
   - Accessible volume slider with logarithmic perceived loudness scaling.
   - Keyboard navigation: Spacebar toggles playback, `M` toggles mute, keys `1`–`9` and `0` instantly switch frequency channels.
   - `aria-live="polite"` status announcer updates assistive technology upon voice switching.
   - Media query `@media (prefers-reduced-motion: reduce)` and JavaScript `window.matchMedia` integration cleanly halt particle agitation and rapid phase rotation when reduced motion is preferred.

---

## 5. Witnessed and not witnessed

### Witnessed (outside):
- *None yet.* Awaiting sensory audit from human architect (Mackenzie Conor James Clark / Mac / Athan) and peer seats (Solfa, Caelorynth, Sol, Wren).

### Checked by the author only (MEASURED / DERIVED):
- **MEASURED:** Valid HTML5 structure verified by `tools/zone-check.mjs`.
- **MEASURED:** JavaScript syntax compiled cleanly via `vm.Script` without runtime parsing errors.
- **MEASURED:** Zero external assets, remote scripts, stylesheets, fonts, or network requests (`fetch`/`xhr`).
- **MEASURED:** Responsive viewport meta tag present and functional across viewports.
- **MEASURED:** Media query for `prefers-reduced-motion` present in both CSS and JavaScript.
- **DERIVED:** Exact frequency parameters ($174, 285, 396, 417, 432, 528, 639, 741, 852, 963\text{ Hz}$) accurately programmed in oscillator frequency scheduling.
- **DERIVED:** Chladni nodal gradient $\nabla |w(x, y)|$ converges particles to $w \approx 0$ curves without numerical divergence.

### Not checked (UNVERIFIED / kessaly):
- Subjective psychoacoustic and emotional effects of specific Solfeggio frequencies on human listeners.
- Acoustic distortion characteristics under physical loudspeaker drivers and budget mobile transducers.
- High-resolution canvas rendering frame rates on lower-end embedded mobile GPUs.

---

## 6. Falsifier

The claim that `builds/solfa-acoustic-synthesizer/` is a functional, mathematically grounded Solfeggio audio synthesis engine is falsified if an auditor:
1. Opens `builds/solfa-acoustic-synthesizer/index.html` in an ECMAScript/WebAudio-compliant browser, clicks "Sound Tone", and observes silence or an unhandled exception when volume is $> 0\%$.
2. Inspects network traffic in developer tools and detects any outbound network request or external resource loading.
3. Selects any of the 10 frequency channels and measures an oscillator fundamental frequency deviating by more than $0.1\text{ Hz}$ from the stated nominal frequency.
4. Activates `prefers-reduced-motion` in system preferences and observes ongoing erratic particle animation or rapid screen flashing.
