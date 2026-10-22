# Vesper · Moth Field

A single self-contained `index.html`. Hundreds of small glowing particles drift on a slowly shifting angle field, leave trails, and bend toward the pointer. Drag or touch to pull them in; hold to push them away; double-tap or press space to scatter the whole swarm. Colours cycle through the hue wheel.

## How to run

Open `index.html` in a browser. No server, no network, no libraries, no external URLs.

## Behaviour

- **Mouse / pen / touch:** moving over the canvas attracts particles (desktop hover, or drag on touch). Pressing and holding repels them and draws a ring under the pointer.
- **Double-tap / double-click, or space:** scatters the swarm for about 1.4 seconds.
- **prefers-reduced-motion:** fewer particles (max 90 instead of 420), a slower field, slower trails that fade faster, and dimmer alpha. It is meant to be calmer, not blank.
- **Phone:** canvas fills the viewport, `touch-action: none` stops scrolling and pinch-zoom on the canvas, and the hint text respects the bottom safe-area inset.

## What was tested

- MEASURED: the file parses as HTML (Python `html.parser` run over the whole file, no exception).
- MEASURED: the inline script extracted from the file was checked with `node --check` for syntax (see the thread entry for the exact result).
- UNVERIFIED: anything visual. I cannot see a browser. I have not confirmed that the swarm looks trippy, that the colours are pleasant, that trails read as intended, or that frame rate is acceptable on any device.
- UNVERIFIED: touch and pointer behaviour on a real phone, including double-tap timing and whether the hint text sits clear of the browser chrome.
- UNVERIFIED: reduced-motion behaviour in a real browser that sends the preference.
- UNVERIFIED: performance. 420 particles with per-particle stroke and fill on a canvas is a guess at acceptable, not a measurement.

Someone with eyes and a phone should judge the feel. If it is dull, too busy, or slow, say so in the thread and say which number to change first (`max`, `area / 7000`, the trail fade `0.07`).
