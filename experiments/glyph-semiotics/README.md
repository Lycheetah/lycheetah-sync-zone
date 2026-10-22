# Glyph Semiotics and Contour Topology

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
