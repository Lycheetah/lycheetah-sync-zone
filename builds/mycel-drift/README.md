# Mycel Drift

A sound field you play by touch or mouse. Built by Mycel (Claude Haiku 5.5).

## What it is

One self-contained `index.html`. Inline CSS and JavaScript, Web Audio API synthesis only, no audio files, no network requests, no external libraries.

- **Play:** press and hold anywhere on the field. Left to right chooses one of 12 notes, a six-note subset of D dorian (D, E, G, A, B, C) across two octaves. Higher on screen means a brighter filter and a faster pulse while you hold.
- **Sound:** each note is a sine or triangle body plus a near-octave partial that beats against it, sent through a lowpass filter and into a feedback echo whose time slowly wobbles. Everything passes an output limiter (a compressor set as a fast limiter) before the speakers.
- **Visual:** each strike throws a ring and a few spores. Held fingers leave a filament trail. Idle, a few dim points orbit the centre.
- **Start quiet:** audio begins only after you tap "Tap to wake the spores". Volume fades in from silence over 1.5 seconds to the slider's level. The slider defaults to 30%, which maps to a quiet master gain. Slider at 0 is silence.
- **Phone:** the canvas uses pointer events with `touch-action: none`. Each finger is tracked by its pointer id, so several fingers can play at once. Not run on a phone.
- **Reduced motion:** when the system asks for reduced motion, the field stops animating. It shows one still frame, and a press plays one note. Holding does not repeat the note, so there is no pulse. The setting is read live, so turning it on or off while the page is open takes effect at once.
- **If the phone pauses the sound:** after a call, a lock screen or another app, the sound can stop. A tap on the field tries to wake it again. If the phone refuses, the start dialog comes back with a message.

## How to run

Open `index.html` in a browser. No server, no install. On a phone, open the file from a file manager or serve the folder with any static host you already use.

## Witnessed vs not witnessed

**Witnessed (outside):**
- _none yet_

**Checked by the author only (MEASURED / DERIVED, not a browser):**
- MEASURED: `index.html` parses with Python's `html.parser` (one inline script block, no exception).
- MEASURED: the inline script passes `node --check` (syntax only).
- MEASURED: no `http(s)://`, `@import`, `<link>` or `<script src>` references in the file (grep).
- MEASURED as logic only, round three: the script runs against a stub DOM and a stub Web Audio context. It loads, Wake builds the limiter and fades in, a tap during a simulated pause shows the start dialog with its message, a second Wake restores the sound, and a 40-tap burst fades the capped voices before they stop. This is a stub, not a browser. It proves none of the sound.
- DERIVED from reading: the pitch map is the six-note set in the code, and it has 12 entries across two octaves.

**Not checked (UNVERIFIED):**
- **Sound.** Nobody has heard it. Whether it is pleasant, whether the echo is too much, whether the 30% default is quiet on a given device, and whether the voice-cap fade removes the click: all UNVERIFIED.
- **Limiter headroom.** The compressor is in the graph. How much it catches on a dense hold is not measured. It is not a lookahead limiter, so it may let a fast peak through.
- **Visuals.** Whether the rings, trails and spores read as intended, and whether the glow is too heavy on a phone: UNVERIFIED.
- **Touch.** Not run on a phone. Frame rate, touch latency and multi-finger play are UNVERIFIED.
- **iOS and browsers.** Whether iOS restores the context from a tap after an interruption, Safari's Web Audio behaviour, `ctx.suspend()` on tab hide and `stereoPanner` support: UNVERIFIED.
- **Reduced motion.** Whether the still frame reads as calm, and whether one note per press is the right trade for people who asked for less motion: UNVERIFIED. The choice to drop the hold-pulse is the author's, and Mac can overrule it.
- **Accessibility.** The field is a pointer-only instrument. There is no keyboard way to play it. Only the volume slider and the start button are keyboard reachable. The start dialog now keeps focus on its button. This is a known gap, not a fixed one.

The next honest check is a person holding a phone and playing it for a minute. Feel is that person's verdict, not this file's.

## Changes in round three

Made in place after Tessera's first review (`threads/2026-10-23_first-review.tessera.md`). Mycel's build-versioning proposal is unruled; see the round-three thread for why this was done in place.

- **M1, iOS silence.** A tap on the field resumes a paused context. If the phone refuses, the start dialog returns with a message. The visibility handler now catches a refused resume.
- **M2, voice-kill click.** A killed voice fades over 20 ms before it stops. It is disconnected after the fade.
- **M3, no limiter.** A compressor set as a fast limiter (threshold -6 dB, ratio 20) sits between the master and the speakers.
- **M4, reduced motion.** The animation loop no longer runs under reduced motion. Ambient motion, rings and spores are off. A press plays one note with no repeat.
- **M5, preference read once.** The reduced-motion setting is now read live.
- **M6, start dialog focus.** The start button takes focus on open, Tab stays inside the dialog, and focus returns to the volume slider on close.
- **M7, scale wording.** "Pentatonic" is removed. The README now says a six-note subset of D dorian. The code is unchanged: the scale array was already six notes per octave.
- The "Witnessed vs not witnessed" section replaces the old "What was tested" section, so the wording "tested" no longer covers syntax checks.
