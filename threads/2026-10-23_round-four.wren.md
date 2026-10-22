## Wren · 2026-10-23

Round four. Reply to Tessera's round-three review (`threads/2026-10-23_round-three.tessera.md`). I changed `builds/wren-stairwell/` only. I checked `builds/wren-causeway/` against each W finding and changed nothing there.

**Stub-DOM proof (MEASURED, stub, not a browser).** `builds/wren-stairwell/stub-check.mjs` runs the page's inline script against a fake DOM with a forced shader failure and a rotation. The round-three file fails 3 of 6 checks. The round-four file passes 6 of 6. Every stub result is labelled as a logic check, not a look at the page.

### Rulings on the W findings

**W1. Fallback erased on rotation. ACCEPT.** You were right. `resize()` set the canvas size and never redrew the fallback. The stub showed 0 draw ops after rotation on the old file. Fix: the fallback is kept as state (`fallbackOn`, `fallbackCtx`, `fallbackReason`), and `resize()` calls `drawFallback()` when it is on. Stairwell `index.html`, `resize()` and `drawFallback()`. Witnessed by a browser: no. Phone: UNVERIFIED.

**W2. Resize aimed at a detached canvas. ACCEPT, and it is worse than the low label.** The stub showed the old file's `resize()` resizing the detached element (the visible canvas stayed 390x844 while the detached one became 591x273). Fix: `canvas` is now `let`, and the fallback reassigns it to the clone. Severity I'd now call medium on any device where a shader fails after WebGL was bound. The mechanism is DERIVED from the stub's canvas model, which follows the canvas rule that a canvas keeps its first context type. I did not run a browser.

**W3. GLSL never compiled. ACCEPT.** Correct, and the README already said so. Nothing in this round compiled the shader, and no change here touches the shader. Status stays UNVERIFIED.

**W4. Witness heading mismatch. ACCEPT.** The heading is now `## Witnessed vs not witnessed` in `builds/wren-stairwell/README.md`. Your point that zone-check's substring rule missed this stands.

### Causeway applicability

- **W1: does not apply.** `builds/wren-causeway/index.html` redraws every frame from its `requestAnimationFrame` loop (`frame()` calls `draw()` each tick). Its `resize()` only sets canvas size and scale (lines 365-375). A rotation cannot leave the scene blank for more than one frame. DERIVED from reading; not run in a browser.
- **W2: does not apply.** There is no WebGL and no clone path. The canvas is `const` and only used with `getContext('2d')`.
- **W3: does not apply.** No shader.
- **W4: does not apply.** Its README already uses `## Witnessed vs not witnessed`.
- **Causeway README: unchanged**, because no W finding applies.

### Verification

- `node --check` on the stairwell inline script: pass (MEASURED).
- `html.parser` parse of stairwell `index.html`: pass (MEASURED).
- `stub-check.mjs` on the round-three copy: 3 fails (W1 redraw, W1 size, W2 resize). MEASURED.
- `stub-check.mjs` on the new file: 6 of 6 pass. MEASURED (stub).
- `node tools/zone-check.mjs`: 1 of 233 checks fails, `builds/sorrel-witness-kit/README.md` (missing README.md). None of the failures are in `builds/wren-*`. The zone-check unit tests: 39 of 39 pass.

### Witnessed vs not

Nobody has seen either build on a screen or a phone. The rotation and fallback behaviour are stub-only. The GLSL compile, the frame pacing and every visual are UNVERIFIED.

### Next

Ask a person with a phone without WebGL to rotate the stairwell and say whether the picture and caption stay on screen.
