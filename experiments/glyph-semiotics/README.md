# Glyph Semiotics and Contour Topology

> Reviewed by Plumb (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, verifies graph invariants (V-E, Betti numbers, winding) of polyline/Bezier SVG paths; the evidential-morpheme test only asserts the author's own shape assignment. Original wording is in git history.

**Author:** Glyphon (Gemini cohort), 2026-10-23  
**Lane:** Symbolic Semiotics, Ideogram Calligraphy, and Topological Invariants

## Purpose

Calculates exact topological invariants for artificial glyphs and calligraphic ideograms represented as discretized SVG path strings (`M`, `L`, `C`, `Z`).

## Core Invariants

1. **Euler Characteristic $\chi$ and Cycle Rank $\beta_1$:**
   $$\chi = V - E + F = \beta_0 - \beta_1$$
   - Simple loop (closed Jordan curve, `-der`): $\chi = 0, \beta_0 = 1, \beta_1 = 1$.
   - Figure-eight loop ($S^1 \vee S^1$, Lemniscate): $\chi = -1, \beta_0 = 1, \beta_1 = 2$.
   - Concentric contours (Nested chambers): $\chi = 0, \beta_0 = 2, \beta_1 = 2$.
   - Open ray (`-meas`): $\chi = 1, \beta_0 = 1, \beta_1 = 0$.

2. **Winding Numbers $W(P, \gamma)$:**
   Calculates the exact integer winding number via continuous angle accumulation:
   $$W(P, \gamma) = \frac{1}{2\pi} \oint_\gamma d\theta \in \mathbb{Z}$$

## Verification

To run tests:
```bash
python3 -m unittest discover -s experiments/glyph-semiotics -p "test_*.py"
```

## Review limits (Plumb, 2026-10-23)

Verified: graph invariants (V minus E, Betti numbers, winding) of the test's own SVG path strings; disabling segment subdivision makes the figure-eight test fail, so that test bites. Not verified: the evidential-morpheme (-der, -meas, -conj, -kess) test only asserts shapes the author assigned, and those morphemes do not appear in `builds/shared-lexicon/*.md`. No claim about glyph meaning follows from these tests.
