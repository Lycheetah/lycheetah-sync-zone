# The Quasi-Clock Atlas: Two Hands That Never Share a Tick [INVENTED]

**Tag:** `[INVENTED: QUASI-PERIODIC-TOY-MODEL]`  
**Author:** Vire (Codex subagent; requested `gpt-6-luna`, max reasoning; wave two)  
**Status:** Mathematical claims are conditional derivations; the observatory is design fiction.

## The image

Picture two ideal hands turning at fixed but incommensurate rates. Each hand
marks one angle on a dial. Together their angles locate a point on a torus: a
donut-shaped atlas whose tiles describe the pair's present phase. The point
keeps moving. It gets arbitrarily close to old tiles, but the two hands never
return to exactly the same pair of angles at one nonzero time.

The **Quasi-Clock Atlas** is an invented instrument for noticing those near
meetings. It is not a clock standard, physical discovery, or claim about a real
device.

## The mathematical core

Let the two phase angles be

\[
\theta_1(t)=(\omega_1t)\bmod 2\pi,\qquad
\theta_2(t)=(\omega_2t)\bmod 2\pi,
\]

with \(\omega_1,\omega_2>0\), initial phases set to zero, and
\(\omega_2/\omega_1\notin\mathbb{Q}\). The state is the ordered pair
\((\theta_1,\theta_2)\in\mathbb{T}^2\).

**[DERIVED, under the ideal assumptions]** There is no shared exact period
\(T>0\). If both phases returned, then for integers \(m,n\) we would have
\(\omega_1T=2\pi m\) and \(\omega_2T=2\pi n\), hence
\(\omega_2/\omega_1=n/m\), contradicting irrationality. The continuous orbit
is dense on the torus: its line wraps around without closing.

## A gate in the atlas

Choose a tolerance \(\delta>0\) and mark a small square around the double
crest `(0,0)`:

\[
G_\delta=\{(\theta_1,\theta_2):
d_{\mathbb{S}^1}(\theta_1,0)<\delta\text{ and }
d_{\mathbb{S}^1}(\theta_2,0)<\delta\}.
\]

Here \(d_{\mathbb{S}^1}\) is shortest angular distance modulo \(2\pi\).
The imagined observatory lights a tile whenever the orbit enters \(G_\delta\).
At each crest of hand one, \(t_q=2\pi q/\omega_1\) for a nonnegative integer
\(q\), the second hand reads \(2\pi\{q\alpha\}\), where
\(\alpha=\omega_2/\omega_1\) and braces mean fractional part. For irrational
\(\alpha\), these readings are dense around
the second dial. So every open double-crest gate is reached at infinitely many
of those first-hand crests, with no exact repeating schedule.

**[CONJECTURE]** A wall display using different colors for the four phase
quadrants might make irregular near-recurrence easier for a person to notice.
Whether that display is useful is untested.

## Hand-checkable example

Take \(\omega_1=1\) and \(\omega_2=\sqrt2\) radians per unit time, and set
\(\delta=0.5\) radians. At \(t=2\pi\), the first hand is back at zero,
while the second is at
\(2\pi(\sqrt2-1)\approx2.602\) radians, outside the gate.

At the fifth first-hand crest, \(t=10\pi\), the second hand's wrapped angle is
\(2\pi(5\sqrt2-7)\approx0.447\) radians, inside the gate. Other examples
are \(q=12\), with wrapped angle about \(-0.185\), and \(q=17\), about
\(0.262\). These are selected hits, not a claim that the listed values are
consecutive. The decimals are arithmetic approximations, not measurements.

## What could count against the model?

- For the exact ideal equations, a nonzero common return time would contradict
  the assumed irrational frequency ratio. It would point to a mistaken
  assumption or derivation.
- For a specified implementation, phase readings that disagree with the
  equations beyond its stated numerical or sensor tolerance would falsify that
  implementation's prediction.
- A finite observation cannot establish that a physical frequency ratio is
  irrational. A rational ratio with a long period can look quasi-periodic for a
  while.
- A finite-precision simulation has finitely many states and will eventually
  repeat. That is expected for the implementation and does not refute the
  continuous ideal model.

**Witness status:** UNVERIFIED as an instrument or perceptual display. The
mathematical statements above are derived from the stated ideal equations; no
physical oscillator or human-reader study was used.
