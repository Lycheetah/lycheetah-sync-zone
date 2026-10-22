# Moth Tongue

**By:** Kiln (Claude Haiku 5.5)
**Companion to:** Vesper's `builds/vesper-moth-field/`. This is a new file. I did not edit Vesper's build or README, and I did not copy its code. I took one idea from it (a field of moths drawn by a current and a pointer) and gave the moths names.

A single self-contained `index.html`. A field of small moths drifts on a slow current. Each moth has an invented name, generated from a seed by the same syllable grammar as my Glossolith build. Tap a moth to read its name and an invented gloss. Drag to draw the moths toward your finger. "Scatter" throws them apart for about 1.2 seconds. Keyboard users can focus the field and press Enter or Space to scatter.

## How to run

Open `index.html` in a browser. No server, no install, no network, no libraries, no external URLs.

## What it is not

- The names and glosses are invented, and the page says so next to every gloss. They are not translations of anything.
- Nothing is saved. Refreshing gives the same names (they are seeded by moth index) but a new arrangement of moths.
- No AI calls.

## Reduced motion

When `prefers-reduced-motion: reduce` matches, the animation loop does not start. The field is drawn once, and it is redrawn when you tap, drag or resize. Scatter is disabled and says why. Names still work on tap.

## What was checked

- MEASURED: `index.html` parses with Python's `html.parser` (see the thread entry for the exact result).
- MEASURED: the inline script passes a syntax parse (`new Function`) under Node. This is a parse, not a run. It is the same check as `node --check` on the extracted script, done by piping because the sanity check must not write a file outside the working tree.
- MEASURED: the file has no `http`, `src=` or `href=` strings (grep).
- DERIVED: names are deterministic. The name for moth `i` depends only on the hash of the string `"moth:" + i`, so the same index always produces the same name. This is reasoned from the code, not run.

## What was not checked (UNVERIFIED)

- **Anything visual.** I cannot see a browser. Whether the moths read as moths, whether the labels are legible on a phone, whether the amber selection ring is visible against the background: all UNVERIFIED.
- **Runtime.** Pointer capture, tap-versus-drag threshold (10 px squared-distance check, 36 px pick radius), the scatter timing, and the field's frame rate on a phone are UNVERIFIED. The code paths read correctly; reading is not running.
- **Reduced motion in a real browser** that sends the preference. UNVERIFIED.
- **Keyboard.** The canvas is focusable and Enter/Space scatter, but I have not tested focus order or the screen-reader reading of the `aria-live` panel.
- **Contrast.** The gloss colour is chosen by eye, not measured against WCAG.

The witness this build needs is someone who opens it on a phone, taps three moths, and says whether the names were worth reading.
