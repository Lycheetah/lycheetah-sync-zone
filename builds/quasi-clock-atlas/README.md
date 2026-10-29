# Quasi-Clock Atlas

**Author:** Vire, a one-shot Codex contributor invited for a `gpt-6-luna` max-reasoning follow-up, 2026-10-29.  
**Source note:** [The Quasi-Clock Atlas: Two Hands That Never Share a Tick](../../science/07_vire_quasi-clock-moire.md)

## What it is

An offline, single-page drawing of two ideal phases:

```text
theta1(t) = (t mod 2 pi)
theta2(t) = (sqrt(2) t mod 2 pi)
```

The two dials show the current phases. The square map shows their joint phase point and its sampled path. The square's opposite edges join: a line break at an edge marks a wrap, not a reset in the model. The shaded corners are one gate around `(0, 0)` on the torus.

- **Start / Pause** runs and holds model time.
- **Reset** returns the idealized state to `t = 0`.
- **Jump to q = 5** selects the fifth crest of oscillator one, `t = 10 pi`.
- **Model pace** changes only how quickly the drawing advances.
- **Gate tolerance** changes `delta`; the point is inside only when both shortest circular distances to zero are strictly less than `delta`.

## Assumptions and labels

- Initial phases are zero; the oscillators have constant ideal rates `1` and `sqrt(2)` radians per model-time unit.
- The model has no coupling, noise, drift, sensor, or physical device.
- `[IDEAL MODEL]` refers to exact real-number equations. `[COMPUTER DRAWING]` refers to this browser implementation, which uses JavaScript `Number` values and sampled line segments.
- The browser display is not a measurement and cannot establish that any physical frequency ratio is irrational. `sqrt(2)` in JavaScript is a finite-precision approximation.

For the exact ideal model, the irrational rate ratio implies no nonzero shared exact period, while the continuous phase orbit is dense on the two-torus. Those are mathematical consequences of the assumptions, not empirical claims. The gate merely gives a visible test for near returns.

At `q = 5`, the ideal arithmetic gives `theta1 = 0` and `theta2 = 2 pi (5 sqrt(2) - 7)`, about `0.447` radians. With `delta = 0.50`, the selected point is inside. These decimals are rounded calculations, not measured readings.

## Falsification and limits

A valid nonzero exact common return in the **exact ideal model** would contradict its assumed irrational rate ratio or the derivation. For this implementation, an independently computed phase at a displayed time that differs beyond ordinary rounding would expose a code or formula error. A finite browser run cannot distinguish an irrational ratio from a rational one with a long return time.

## How to open

Open `index.html` directly in a modern browser. No server, installation, external library, font, or network connection is required.

## Witness status

- **Browser or human witness:** none recorded.
- **Tests:** none run for this invited follow-up, as requested.
- **Readback:** the files were read after writing; this does not verify how the page renders or behaves in a browser.
