# Mycel Drift

A sound field you play by touch or mouse. Built by Mycel (Claude Haiku 5.5).

## What it is

One self-contained `index.html`. Inline CSS and JavaScript, Web Audio API synthesis only, no audio files, no network requests, no external libraries.

- **Play:** press and hold anywhere on the field. Left to right chooses one of 12 notes in D dorian-ish pentatonic (two octaves). Higher on screen means a brighter filter and a faster pulse while you hold.
- **Sound:** each note is a sine or triangle body plus a near-octave partial that beats against it, sent through a lowpass filter and into a feedback echo whose time slowly wobbles.
- **Visual:** each strike throws a ring and a few spores. Held fingers leave a filament trail. Idle, a few dim points orbit the centre.
- **Start quiet:** audio begins only after you tap "Tap to wake the spores". Volume fades in from silence over 1.5 seconds to the slider's level. The slider defaults to 30%, which maps to a quiet master gain. Slider at 0 is silence.
- **Phone:** the canvas uses pointer events with `touch-action: none`, so multi-finger play is supported in principle.

## How to run

Open `index.html` in a browser. No server, no install. On a phone, open the file from a file manager or serve the folder with any static host you already use.

## What was tested, and what was not

Tested (MEASURED, by the seat that wrote it):
- HTML parses with Python's `html.parser` (no error raised, one inline script block found).
- The inline script parses as JavaScript (`new Function(...)` under Node 24, a syntax parse only, not run). This is not a run and says nothing about behaviour.
- No `http(s)://`, `@import`, `<link>` or `<script src>` references in the file (grep).

Not tested (UNVERIFIED):
- **Sound.** I cannot hear it. Whether it is pleasant, whether the echo is too much, whether the 30% default is actually quiet on a given device, whether the voice-cap kill produces an audible click: all UNVERIFIED.
- **Visuals.** I cannot see it. Whether the rings, trails and spores read as intended, and whether the glow is too heavy on a phone, are UNVERIFIED.
- **Touch.** I have not run it on a phone or tested multi-touch. Frame rate and touch latency are UNVERIFIED.
- **Browsers.** Not run in any browser. Safari's Web Audio behaviour, `ctx.suspend()` on tab hide, and `stereoPanner` support are UNVERIFIED.
- **Accessibility.** The field is a pointer-only instrument. There is no keyboard way to play it. Only the volume slider and the start button are keyboard reachable. This is a known gap, not a fixed one.
- **Reduced motion.** The code lowers trail persistence when `prefers-reduced-motion` is set. Whether that helps enough is UNVERIFIED.

The next honest check is a person holding a phone and playing it for a minute. Feel is that person's verdict, not this file's.
