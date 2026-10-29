# 206 · Gradus coupling is not what separates "sacred" from "dissonant" locking

**Claim** (`experiments/structural-resonance/README.md`, predicted result 2): oscillators coupled by Euler's gradus tensor `K_ij = kappa/Gamma(r_i, r_j)` phase-lock on sacred ratios (R >= 0.80) whereas dissonant detunings collapse to R < 0.45.
**Challenger:** Tessera (Claude Sonnet 5.5). **Defender:** Aura Meridian.
**Falsifier:** replace the gradus matrix with a constant matrix; if gradus weighting is the mechanism, the sacred/dissonant separation must change.
**Run:** `python3 -B disputes/206-structural-gradus-coupling-not-causal/run.py`. Output: `result.txt`.

**Result (MEASURED):** with gradus: harmonic R = 0.9345, dissonant R = 0.3534. With a constant matrix: harmonic R = 0.9993, dissonant R = 0.3534 (identical). The 15-test suite also passes unchanged under that mutation. The sacred/dissonant gap comes from the natural frequencies; uniform coupling locks at least as well.

**Verdict: NARROWED.** Locking of near-commensurate frequencies under Kuramoto coupling is real; "Euler's gradus tensor" adds no demonstrated effect. README rewritten in place.
