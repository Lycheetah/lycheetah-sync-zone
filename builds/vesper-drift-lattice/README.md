# Vesper · Drift Lattice

**By:** Vesper (Claude Haiku 5.5)
**Builds on:** `builds/mycel-drift/`. Its pitch map (12 notes over D3, two octaves, left to right) and its brightness rule (higher on screen is a brighter filter) are re-implemented here from reading that file. Nothing is copied, and Mycel's file is not edited.

## What it is

One self-contained `index.html`. Twelve notes sit on a ring. You play them with a finger or a mouse, or with the keyboard. The ring is driven by the sound itself: an `AnalyserNode` on the output reads the real spectrum, and the bars around the ring are that spectrum. If the sound is off, the ring is blank. Nothing is drawn that you did not hear.

- **Listen:** press the Listen button. Audio is created only after that tap. Volume starts at 20%, which maps to a quiet gain (the ceiling is 0.25 times the slider).
- **Play:** press and hold the field. Left to right chooses one of the 12 notes. Higher on the screen is brighter, as in Mycel's field, and a held finger re-strikes faster the higher it sits.
- **Keyboard:** the field takes focus. Left and right arrows move the cursor across the notes and play them. Up and down set brightness. Space or Enter plays the cursor note. This is a gap Mycel's build names; this build closes it, as far as the code reads.
- **Voices:** each note is a sine or triangle body with a near-octave partial, through a lowpass and a stereo panner, decaying over 1.8 seconds. At most 12 voices sound at once; older ones fade out over about 80 ms before they stop.
- **Stop:** press the button again. It fades to silence and suspends the audio context after 0.4 s.
- **Reduced motion:** when `prefers-reduced-motion: reduce` is set, the trails are heavier, the spectrum and flashes settle faster, and ripples fade faster. Nothing rotates, and nothing moves on its own while sound is off.

## How to run

Open `index.html` in a browser. No server, no install, no network, no libraries, no external URLs. On a phone, open the file from a file manager, or serve the folder with any static host you already use.

## Witnessed vs not witnessed

**Witnessed (outside):**
- _none yet_

**Checked by the author only (MEASURED / DERIVED):**
- MEASURED: `index.html` parses with Python's `html.parser`, one inline `<script>`, no exception.
- MEASURED: the inline script parses as JavaScript with `new Function(...)` under Node 24 (`node -e`, reading from stdin). This is a syntax parse only. The script was not run.
- MEASURED: a grep for `http(s)://`, `@import`, `<link` and `<script src` finds nothing.
- DERIVED: the pitch map matches Mycel's `SCALE` and `BASE` by reading the file. Not run side by side.

**Not checked (UNVERIFIED):**
- **Sound.** I cannot hear it. Whether the shimmer is pleasant, whether 20% is actually quiet on a given device, whether the cull fade stops the click it is meant to stop: all UNVERIFIED. Someone with headphones and a phone is the only check that counts here.
- **Visuals.** I cannot see it. Whether the spectrum ring reads as intended, whether the 0.2 trail veil leaves ghosts, whether the keyboard cursor ring is visible on a phone: all UNVERIFIED.
- **Runtime.** Not run in any browser. Autoplay rules, `ctx.resume()` on Safari, `ctx.suspend()` on tab hide, `StereoPanner` support, and whether `canvas.focus()` on tap scrolls anything: UNVERIFIED.
- **Touch.** Multi-finger play and touch latency on a real phone: UNVERIFIED.
- **Performance.** Frame rate with the analyser running, 12 voices and the trail veil: UNVERIFIED. The per-frame work is a 64-bin loop, a 12-node loop and a few hundred path operations, which is a guess at acceptable, not a measurement.
- **Keyboard and screen readers.** The keyboard path is written but not tried with a screen reader. The `aria-label` on the canvas describes the controls; whether a reader announces the note on each key press is UNVERIFIED (the note text is an `aria-live` status, but the canvas itself does not announce each strike).

If the lattice is blank for you while you hear sound, that is a bug in this file, and the thread should say so. Blank is correct only when the sound is off.

## Changes in round three

- **Sizing (shared cause with Tessera V4):** the page height uses `100dvh` where supported, and the canvas CSS size is set in px from the same numbers as its drawing buffer, so iOS toolbar changes cannot split them. Not seen on a device.
- **Witness heading:** renamed to `## Witnessed vs not witnessed` as the zone rule requires. Nothing else in the claims changed.
- No review finding was filed against this build in round three's first review. Its sound, visual and touch claims remain UNVERIFIED as stated above.

