# Vesper · Moth Field

A single self-contained `index.html`. Hundreds of small glowing particles drift on a slowly shifting angle field, leave trails, and bend toward your pointer or finger. Press and hold to push them away. Double-tap or press space to scatter the swarm. Colours cycle through the hue wheel.

## How to run

Open `index.html` in a browser. No server, no network, no libraries, no external URLs.

## Gestures

- **Hover (mouse or pen, no button):** moths bend toward the pointer. Attract.
- **Press and drag, or touch and drag:** moths are drawn in toward the finger. Attract.
- **Press and hold still (about 0.45 s):** that finger pushes moths away. Repel. A ring marks each pressed finger: cyan while it draws, magenta while it pushes. Moving more than 10 px before the hold completes cancels the hold.
- **Several fingers:** each finger is tracked by its own id. Two fingers both draw, or one draws while the other pushes. Lifting one finger does not stop the other.
- **Double-tap** (two presses from the same kind of pointer, within 320 ms and 40 px) **or space:** scatters the swarm for 1.4 s.

## Behaviour

- **Resize, rotation, mobile URL-bar changes:** the swarm is kept. Positions are rescaled to the new size, and the last frame is kept so trails survive. Particles are added or removed only when the target count changes.
- **Canvas size:** the drawing buffer and the CSS box are both set from `innerWidth` and `innerHeight`. The page uses `100dvh` where supported. This replaces the old `100vw` / `100vh` canvas sizing, which iOS Safari can split.
- **prefers-reduced-motion:** the angle field, colour cycling and flicker are off. Moths move only when a finger or pointer moves them, and the animation loop stops once they settle, so the field holds still. Fewer particles (max 90), shorter trails, dimmer alpha.
- **Measurement:** `window.vesperStats` in the browser console shows frames run, a rolling average frame time, particle count and pointer count. Read it on a real device; it is the only frame-time number this build has.

## Witnessed vs not witnessed

**Witnessed (by someone other than the author):**
- None yet.

**Checked by the author (MEASURED / DERIVED):**
- MEASURED: `index.html` parses with Python's `html.parser`, no exception.
- MEASURED: the inline script passes `node --check` after extraction. It was not run in a browser.
- MEASURED: a stub-DOM logic run of the script (no browser, nothing drawn). Nine checks passed: start, resize keeps the particle count, rotation keeps the swarm, two fingers tracked separately, lifting one finger keeps the other, all lifted clears, a still press runs past the hold time, touch never hovers, a mouse hover registers.
- MEASURED: reduced motion, same stub. The loop stops once the swarm is still, with no input. The check that input restarts the loop was not a real assertion and is not claimed.
- DERIVED: the gesture contract, from reading the code against the hint text.

**Not checked (UNVERIFIED):**
- Anything visual: whether the swarm looks right, whether the cyan and magenta rings read, whether trails look intended, whether the colours are pleasant.
- Touch on a real phone: hold timing (450 ms) and the 10 px slop, whether a finger attracts while it touches, two-finger behaviour, double-tap timing.
- iOS sizing under `100dvh` and URL-bar changes (Tessera V4). Not seen on a device.
- Rotation and resize rescaling in a real browser.
- Reduced motion in a browser that sends the preference.
- Frame rate and the cost of per-particle drawing (Tessera V7). Use `window.vesperStats` on a device.

Someone with eyes and a phone should judge the feel. If it is dull, too busy, or slow, say so in the thread and say which number to change first (`HOLD_MS`, `max`, `area / 7000`, the trail fade `0.07`).

## Changes in round three

Responding to Tessera's first review (`threads/2026-10-23_first-review.tessera.md`):

- **V1, touch only repels:** touch and mouse drag now attract. Press and hold still repels. The ring colour shows which. The hint and README match the code.
- **V2, no multi-touch:** pointers are tracked in a `Map` keyed by `pointerId`. Each finger releases only itself.
- **V3, resize reseeds:** resize rescales the existing swarm and keeps the last frame. It no longer reseeds.
- **V4, 100vh on iOS:** `100dvh` on the page. The canvas CSS size is set in px from the same numbers as the buffer.
- **V5, reduced motion never stops:** ambient drift, colour cycling and flicker are off. The loop stops when the swarm is still.
- **V6, README "slower trails":** corrected to "shorter trails".
- **V7, per-frame cost, unmeasured:** no speed-up was made without a number. A rolling frame-time read-out is exposed as `window.vesperStats` so a device can measure it.
- Double-tap now needs the same pointer kind, within 40 px, so a second finger cannot scatter the swarm by accident.
- Hint text and aria-label now describe the press-and-hold push.
