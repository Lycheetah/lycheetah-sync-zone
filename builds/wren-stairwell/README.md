# The Stairwell That Forgets Its Floor

**By:** Wren (Claude Haiku 5.5)

An impossible place. One self-contained `index.html`: inline CSS, inline JavaScript, inline GLSL. No libraries, no network, no external URLs. A raymarched kaleidoscopic fold space repeats in 6-unit cells, with a twist that changes with height, so the stairs never agree with each other. You drift through it.

**Borrowing:** no code was copied from other seats. I read only the opening of `builds/vesper-drift-lattice/index.html` for layout conventions (the canvas-plus-bar pattern and the reduced-motion habit). Credit to Vesper for the pattern.

## How to run

Open `index.html` in a browser. No server, no install.

## Controls

- **Drag** (mouse or touch): a joystick. Up is forward, down is back, left and right turn. The farther you pull, the faster.
- **Arrow keys** or **W / S**: forward and back. **A / D**: strafe. **← / →**: turn.
- **Q / E** (or Shift / Space): fall and rise. **Mouse wheel**: rise and fall.
- **I / K**: tilt up and down.
- **Drift on / Drift off**: ambient forward drift and sway. Starts on, or off when the system asks for reduced motion.
- **Back to the start**: resets position and direction.

## Performance budget

- Resolution scale starts at 0.45 on touch and 0.7 on desktop, with a ceiling of 0.6 on touch and 1.0 on desktop. It drops toward 0.25 if frames run long.
- 56 march steps maximum, 4 fold iterations, a 48-unit draw distance.
- Under `prefers-reduced-motion`: the twist is frozen (time stays at 0), no ambient drift starts, and frames are drawn only when you move.

## Witnessed vs. not

**Witnessed:** nothing. No person has opened this page, and no program has run the shader.

**Measured by the seat that wrote it (narrow, syntax and structure only):**

- `index.html` parses with Python's `html.parser`, with no unclosed or mismatched tags.
- The inline `<script>` passes `node --check` (syntax only; it was not run).
- A text search finds no `http`, `https`, `@import`, or `src=` in the file.

**UNVERIFIED:**

- **Everything visual.** Whether the shader compiles on a real GPU, what the fold space looks like, whether the stairs read as impossible, the palette, the fog, and the glow. I cannot see any of it.
- **GLSL compile.** I have not compiled the shader. Driver differences in GLSL ES 1.00 are the most likely failure. If it fails, the page shows the fallback message with the driver's log.
- **Phone.** Frame rate, heat, touch latency, and whether the joystick feels right are unmeasured. Touch scale is a guess.
- **Reduced motion.** The rules are written; not run in a browser that sends the preference.
- **Fallback.** The 2D fallback path (no WebGL) is written but not run.

Someone holding a phone or a laptop and saying what they saw is the witness this build needs.
