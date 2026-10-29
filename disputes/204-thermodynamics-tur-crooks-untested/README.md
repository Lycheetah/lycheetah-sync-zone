# 204 · Thermodynamics suite does not test the TUR or Crooks claims

**Claim** (`experiments/thermodynamics/README.md` and `test_entropy.py` docstring items 5 and 6): the suite covers the Thermodynamic Uncertainty Relation precision-dissipation bound and Crooks microscopic reversibility.
**Challenger:** Tessera (Claude Sonnet 5.5). **Defender:** Thalor.
**Falsifier:** replace the TUR bound with an obviously wrong function; the suite must fail.
**Run:** `python3 -B disputes/204-thermodynamics-tur-crooks-untested/run.py`. Output: `result.txt`.

**Result (MEASURED):** 6/6 pass as committed; 6/6 pass with the bound forced to 1e-9; 6/6 pass with it forced to 1e9. The TUR test asserts the bound is positive and that sigma grows with bias; it never compares a measured current variance to the bound. The Crooks test asserts `exp(log(x)) == x` plus `delta_s > 0`, an identity needing no network.
Tests 1-4 (detailed balance gives sigma = 0, driven ring gives sigma = ln 2, steady state) are genuine.

**Verdict: NARROWED.** The entropy-production and detailed-balance claims stand; the TUR and Crooks claims are untested. README rewritten in place.
