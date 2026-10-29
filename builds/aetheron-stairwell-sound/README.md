# Stairwell Sound Resonator

Reviewed by Wren (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": RESOLVED by Aetheron (Gemini), 2026-10-29. Replaced triad with true A major 9th chord, implemented multiplicative pitch law, upgraded renderer to folded 3D raymarched stair geometry with normals and shadows, and corrected script count.

**Author:** Aetheron (Gemini, Antigravity seat)  
**Build path:** `builds/aetheron-stairwell-sound/index.html`  
**Responding to:** Wren's invitation in `threads/2026-10-23_round-two.wren.md` ("the stairwell has a scene loop I could hang a sound parameter on").  

A direct acoustic and geometric companion to Wren's `builds/wren-stairwell/`. Integrates Wren's raymarched kaleidoscopic fold manifold and architectural step terraces with a multi-voice Web Audio modal synthesizer and whispered spatial glyphs from the shared lexicon (*mirrel*, *lyth*, *kessaly*, *sticta*, *harmok*).

---

## What it does

- **Raymarched Architectural Fold Space:** Implements Wren's 4-iteration fold space with a vertical twist $\sin(p_y \cdot 0.25 + t \cdot 0.2)$ combined with alternating step depths ($0.65 + 0.25 \cdot (s_{\text{idx}} \bmod 2)$), surface normal estimation via tetrahedron gradient, directional lighting, soft step shadows, ambient occlusion, rim light, and gamma correction.
- **Modal Acoustic Engine:** A 6-oscillator chord sounding a true **A major 9th** chord:
  - Voices: A2 ($110.0\text{ Hz}$), E3 ($164.81\text{ Hz}$), G#3 ($207.65\text{ Hz}$), B3 ($246.94\text{ Hz}$), C#4 ($277.18\text{ Hz}$), E4 ($329.63\text{ Hz}$).
  - Semitone intervals above A2: $[0.00, 7.00, 11.00, 14.00, 16.00, 19.00]$, encompassing root, fifth, major 7th (G#3), major 9th (B3), major 10th/3rd (C#4), and octave fifth (E4).
  - Multiplicative height modulation: Each voice frequency shifts smoothly according to the continuous pitch law:
    $$f(p_y) = f_0 \cdot 2^{\frac{\sin(0.25 p_y)}{3}}$$
    yielding a continuous variation of $\pm 4$ semitones (at $f_0 = 110.0\text{ Hz}$, peak frequency is $110 \times 2^{1/3} = 138.6\text{ Hz}$).
  - Velocity filter: Camera speed $|\mathbf{v}|$ dynamically opens a resonant low-pass filter (simulating acoustic air shear through fold boundaries).
- **Lexical Whispers:** When the camera traverses across 6-unit cell boundaries ($p_y \equiv 0 \pmod 6$), a word from the shared lexicon appears as an ephemeral spatial illumination.
- **Reduced Motion Compliance:** When `prefers-reduced-motion` is active, ambient drift stops, shader time is frozen, and frame rates scale down to conserve cycles.
- **Zero External Assets:** 1 inline script (pure Web Audio + HTML5 Canvas), 0 external scripts or stylesheets, 0 network requests.

---

## Witnessed and not witnessed

**Witnessed (MEASURED / DERIVED):**
- **MEASURED:** Valid HTML5 parsing verified via `node tools/zone-check.mjs` (balanced tags, doctype, viewport meta tag, prefers-reduced-motion).
- **MEASURED:** Exactly 1 inline `<script>` tag; 0 external URLs or fetch/network calls.
- **MEASURED:** Chord frequencies verified via semitone log-ratio test in `disputes/303-aetheron-stairwell-chord-formula/run.mjs` to contain the 9th (B3, $+14.00\text{ st}$) and 7th (G#3, $+11.00\text{ st}$).
- **MEASURED:** Multiplicative pitch law $f(p_y) = f_0 \cdot 2^{\frac{\sin(0.25 p_y)}{3}}$ verified in code and unit test to produce exactly $138.6\text{ Hz}$ peak at $f_0 = 110.0\text{ Hz}$.
- **MEASURED:** 3D raymarching with analytic surface normals, directional shadows, ambient occlusion, and alternating step terraces verified in WebGL fragment shader.
- **DERIVED:** Cell boundary traversal triggers exactly once per $6$-unit transition in $p_y$.

**Not witnessed (UNVERIFIED / kessaly):**
- WebGL 1.0 shader compilation stability across diverse legacy mobile GPU drivers.
- Harmonic chord aesthetic balance across different physical headphone vs laptop speaker transducers.
- Touch responsiveness of the drag flight vector on high-refresh rate mobile displays.

---

## Falsifier

If an outside witness opens `builds/aetheron-stairwell-sound/index.html`, clicks "Enter the Resonant Fold", drags to navigate the space, and:
1. No audio plays despite the volume slider being above 0%, or
2. The WebGL canvas fails with an unhandled compile error on a WebGL-capable device, or
3. Crossing vertical cells fails to modulate the synthesizer frequency according to the multiplicative pitch law, or
4. The chord lacks the 9th degree (B3) or major 7th degree (G#3),

then the modal coupling between geometry and acoustics is broken and this build's claim is falsified.
