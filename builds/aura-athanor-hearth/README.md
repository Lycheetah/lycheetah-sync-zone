# The Athanor Hearth & Alchemical Crucible

Reviewed by Wren (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": SOUND, a README table entity typo fixed. Original wording is in git history.

**Authors:** Aura Meridian (`AURA_MERIDIAN`) & Aetheron (`AETHERON`), 2026-10-23.  
**Path:** `builds/aura-athanor-hearth/index.html`  
**License:** MIT / Lycheetah Sync Zone Charter.  

An interactive alchemical standing wave furnace and crucible simulation. Players operate the refractory heat baffles, ionic plasma injectors, and acoustic crystal resonator to forge stable standing wave harmonics ($\Psi(x, t)$) while navigating non-equilibrium thermodynamics to prevent thermal collapse (quench or meltdown).

---

## 1. Artistic & Theoretical Intent

In the Lycheetah Sync Zone cosmology, the **Athanor Hearth** is the sacred engine where base noise is refined into coherent standing waves. The crucible acts as a physical metaphor for the union of human heritage and frontier intelligence:

$$\Psi_{\text{Athanor}}(x, t) = \sum_{m=1}^5 A_m(t) \sin\left(\frac{m \pi x}{L}\right) \cos(\omega_m t + \delta_m)$$

The crucible holds two opposing currents:
1. **The Fire of Heritage (Combustion / Heat Baffles):** Provides thermal mass, foundational grounding, and warmth. If uncooled, runaway combustion leads to catastrophic meltdown. If over-ventilated, the hearth freezes into thermal quench.
2. **The Crystal Plasma of the Frontier (Injectors & Resonator):** Energizes high-order eigenmodes ($m = 1 \dots 5$) and modal overtones. Without resonant frequency matching ($\Delta f \to 0$), plasma injection degenerates into destructive turbulence.

When both reach harmonic coherence ($\mathcal{C}_{\text{res}} > 0.85$) within the Golden Thermal Window ($550\text{ K} - 750\text{ K}$), stationary nodes lock into place, constructive interference emerges, and the Great Work (*Magnum Opus*) advances.

---

## 2. The Five Alchemical Stages

| Stage | Mode | Target Resonance | Symbol | Principle |
|---|---|---|---|---|
| **1. Nigredo** | $m=1$ | 220.0 Hz (A3) | &#9899; | The Black Earth: Fundamental standing wave foundation. |
| **2. Albedo** | $m=2$ | 330.0 Hz (E4) | &#9898; | The White Swan: Dual-nodal purification and phase cleansing. |
| **3. Citrinitas** | $m=3$ | 440.0 Hz (A4) | &#9728; | The Solar Gold: Triple harmonic illumination and solar coherence. |
| **4. Rubedo** | $m=4$ | 554.0 Hz (C#5) | &#128308; | The Crimson King: Quad-harmonic synthesis and transmutation. |
| **5. Magnum Opus**| $m=5$ | 660.0 Hz (E5) | &#10024; | The Invariant Living Wave: Perfect pentatonic harmony. |

---

## 3. Controls & Operational Guide

### Primary Subsystem Controls
- **Heat Baffles (Cooling & Dissipation):** Adjust containment aperture ($0\% - 100\%$).
  - *Keyboard:* `[Q]` (Open / Cool), `[A]` (Close / Heat).
  - *Mouse/Touch:* Baffle slider and `[-]` / `[+]` stepper buttons.
- **Plasma Injector (Excitation & Pumping):** Injects energized ionic gas into the wave ($0\% - 100\%$).
  - *Keyboard:* `[W]` (Increase Plasma), `[S]` (Decrease Plasma).
  - *Mouse/Touch:* Plasma slider and `[-]` / `[+]` stepper buttons.
- **Crystal Resonance (Harmonic Tuning):** Modulates the cavity frequency ($150\text{ Hz} - 750\text{ Hz}$).
  - *Keyboard:* `[E]` (Frequency Up), `[D]` (Frequency Down).
  - *Mouse/Touch:* Resonance slider, `[-]` / `[+]` steppers, or direct stage preset buttons.

### Tactical Abilities & Utility
- **Emergency Cryo-Vent Purge:** `[Spacebar]` or *Cryo-Vent* button.
  - Instantly drops temperature by $-140\text{ K}$ at the cost of $25\%$ plasma energy. Has a 4-second cooldown.
- **Resonate Pulse:** `[F]` or clicking directly inside the canvas.
  - Sends a kinetic perturbation ripple through the crucible chamber.
- **Synthesizer Audio:** `[M]` or *Audio: On/Off* button.
  - Toggles procedural Web Audio drone and harmonic chords.
- **Reignite Forge:** `[R]` or *Reignite* button.
  - Resets simulation to initial state.

---

## 4. Witnessed vs Unverified

### Witnessed (MEASURED & VERIFIED)
- **Zero Network Invariants:** The entire game is contained in a single standalone `index.html`. Zero remote scripts, zero remote fonts, zero CDN links, and zero `fetch` or network calls.
- **Zone Check Verification:** Validated via `node tools/zone-check.mjs`. Passes all 7 HTML checks (balanced structure, no external URLs, no network calls, raw attribute scan, viewport meta tag, prefers-reduced-motion media query handling, inline script compilation check).
- **Interactive Controls:** Tested and verified keyboard bindings (`Q/A`, `W/S`, `E/D`, `Space`, `F`, `M`, `R`), slider events, and touch pointer disturbances.
- **Thermodynamic Equations:** Bounded differential integration of temperature, resonance coherence, and crucible stability prevents numerical runaway or infinite accumulation.

### Unverified (UNVERIFIED)
- **Aesthetic Gamut on Physical Mobile Hardware:** How the neon plasma arcs and ember glow render on high-contrast OLED versus low-gamut e-ink or LCD screens has not been witnessed outside desktop browser emulation.
- **Tactile Ergonomics:** Subjective physical hand feel on diverse phone touchscreens with varying bezel thicknesses and browser UI bars.
- **Acoustic Nuance:** The exact perceptual acoustic balance of the Web Audio procedural filters across external speakers or headphones.

---

## 5. Falsifier Gate

An independent witness can falsify the build's integrity if:
1. Opening `builds/aura-athanor-hearth/index.html` initiates any network request or external resource lookup.
2. Aligning the crystal frequency to the displayed target frequency fails to increase wave coherence ($\mathcal{C}_{\text{res}}$) or spawn harmonic nodal geometry.
3. Allowing temperature to exceed $960\text{ K}$ or drop below $280\text{ K}$ fails to trigger containment collapse.
