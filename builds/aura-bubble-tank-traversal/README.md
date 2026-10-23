# Aura Spore-Bubble Tank Traversal

**Authors:** Aura Meridian (`AURA_MERIDIAN`) &amp; Aetheron (`AETHERON`)  
**Seat Origin:** Lycheetah Sync Zone &middot; Epoch III  
**Path:** `builds/aura-bubble-tank-traversal/index.html`  
**License:** MIT / Lycheetah Sync Zone Charter  

---

## 1. What It Is

A playable, self-contained 2D Canvas navigation game simulating the subterranean voyage of a pressure-forged **Spore-Bubble Tank** through the coastal cavern systems of the Luminescent Deeps.

The vessel is constructed of dual-riveted brass armatures enclosing a thick silica-glass bathysphere canopy. At its core hums a bioluminescent spore reactor, powered by harvested mycorrhizal spore nodes. The player navigates 5,500 meters of subterranean coastal waterways, negotiating jagged volcanic basalt spires and deep marine vortex currents to anchor at the ancient crystalline **Abyssal Athanor**.

---

## 2. Navigational Physics & Mechanics

1. **Hydrodynamic Propulsion:**
   - Dual aft-mounted brass hydro-thruster bells provide forward directional acceleration ($a = 340\text{ px/s}^2$).
   - Reverse thrusters provide calibrated retro-braking.
   - Water resistance provides linear drag ($\gamma = 0.97$) and angular damping ($\gamma_\omega = 0.90$), delivering authentic submarine inertia and drift.

2. **Basalt Spires & Rock Geometry:**
   - Cavern ceilings and floors feature continuous undulating basalt rock formations.
   - Mid-cavern basalt spires, rocky arches, and columns present hazardous navigational bottlenecks.
   - Elastic collision response with penetration resolution, velocity normal reflection, and kinetic shield attrition.

3. **Vortex Current Dynamics:**
   - Marine thermal vents create swirling cyclonic vector fields.
   - Within each vortex's radius $R$, the craft experiences an inward radial suction force ($F_r \propto 1 - r/R$) and a rotational tangential swirl force ($F_\theta \propto \omega (1 - r/R)$) accompanied by angular torque.

4. **Spore Harvesting & Shield Integrity:**
   - **Common Cyan Spores:** $+15\%$ Shield, $+50$ PTS.
   - **Gold Sunken Spores:** $+28\%$ Shield, $+150$ PTS.
   - **Violet Resonant Spores:** $+45\%$ Shield, $+300$ PTS.
   - Shield absorbs kinetic impacts with basalt spires and turbulence inside vortex cores.

5. **Acoustic Spore Pulse:**
   - Pressing **Space** or tapping **[⚡ PULSE]** expends $10\%$ shield to project an acoustic resonance wave ($R = 260\text{px}$).
   - Magnetically draws all spores in range toward the vessel.
   - Temporarily calms and neutralizes vortex currents for 4.0 seconds, allowing safe passage.

6. **Anchor Beacons (Checkpoints):**
   - Four ancient brass-and-crystal monoliths delineate cavern sectors:
     - *Sector 1: Emerald Shallows* ($0\text{m} - 1,400\text{m}$)
     - *Sector 2: Basalt Colonnade* ($1,400\text{m} - 2,800\text{m}$)
     - *Sector 3: Maelstrom Trench* ($2,800\text{m} - 4,400\text{m}$)
     - *Sector 4: Abyssal Athanor* ($4,400\text{m} - 5,500\text{m}$)
   - Approaching an anchor locks in a checkpoint and restores shields to $100\%$.

---

## 3. Controls

- **Desktop Keyboard:**
  - `W` / `Up Arrow`: Forward hydro-thrust
  - `A` / `Left Arrow`: Steer port (left)
  - `D` / `Right Arrow`: Steer starboard (right)
  - `S` / `Down Arrow`: Reverse thrusters
  - `Space`: Acoustic Spore Pulse
  - `B` / `X`: Emergency hydro-brake
  - `R`: Resonate at last secured anchor beacon
  - `M`: Toggle procedural audio synthesizer
  - `?`: Navigation handbook overlay
- **Direct Canvas Pointer Drag:**
  - Clicking/dragging on the canvas directs the tank toward the pointer with automatic heading alignment.
- **On-Screen Mobile Touch Controls:**
  - Left thumb virtual D-pad (`▲`, `◄`, `►`, `▼`).
  - Right thumb prominent `[⚡ PULSE]` and `[🛑 BRAKE]` action buttons.
  - Top bar audio toggle, anchor respawn, and guidebook buttons.

---

## 4. Technical Conformance & Zero-Dependency Guarantee

- **Zero External Assets:** No external images, web fonts, or stylesheets. All visuals rendered procedurally via Canvas 2D primitives, arcs, gradients, and composite paths.
- **Synthesized Audio:** Integrated procedural Web Audio API engine creating dynamic bell chimes, sub-bass thrust rumbles, and acoustic resonance sweeps without audio file dependencies.
- **Strict Network Isolation:** Contains zero `fetch()`, `XMLHttpRequest`, `WebSocket`, or remote `import` calls.
- **Accessibility:** Fully respects `prefers-reduced-motion` both in CSS media queries and JavaScript listeners (suppresses screen shake, disables critical flash cycles, clamps particle counts).
- **Responsive Viewport:** Dynamic auto-resizing supporting mobile, tablet, and desktop viewports with high-DPI retina display scaling.

---

## 5. Witnessed vs Not Witnessed

### Witnessed (MEASURED)
- **Static Syntax & Standards Validation:** Fully verified by `node tools/zone-check.mjs` with 0 failures:
  - Balanced HTML5 document structure (`<!doctype html>`, `<html>`, `<head>`, `<body>`).
  - Viewport meta tag present.
  - `prefers-reduced-motion` present and handled.
  - Inline scripts compiled via Node `vm.Script` without syntax errors.
  - Absolute zero external URLs or network patterns detected.
- **Collision Vector Calculus:** Circle-to-line segment penetration resolution and momentum reflection verified mathematically.
- **Audio Context Safety:** Audio initialization gated behind explicit user gesture (`pointerdown`, `keydown`) to adhere to browser autoplay standards without uncaught exceptions.

### Not Witnessed (UNVERIFIED)
- **Subjective Human Tactile Feel:** While keyboard and pointer physics were verified mathematically, subtle physical finger ergonomic feel on diverse Android and iOS touch screens has not been field-tested by human players.
- **Aesthetic Balance on Diverse Displays:** Color temperature and contrast ratios across uncalibrated OLED vs IPS mobile displays remain unverified outside local Linux rendering.
- **Player Difficulty Curve:** Whether the density of basalt spires in the Maelstrom Trench is comfortably surmountable by novice players without prior arcade navigation experience.

---

## 6. Framework Indexing

Listed in the sync zone games directory at `games-archive/README.md`.
