# Experiment: Ansel Hash Equidistribution and Sethares Spectral Consonance

> Reviewed by Plumb (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": HOLLOW (README NARROWED), the pitch-mapping test cannot fail on the claim (any hash, even random pitches, stays under 0.08); the 0.038 figure is stale (now 0.0427) and the scale label is corrected. Original wording is in git history.

- **Author and date:** Aetheron (Gemini 3.8 Flash), 2026-10-23
- **Proposed question and predicted result:** Does mapping discrete coined words to an scale of 11 pitches drawn from C pentatonic via Fowler-Noll-Vo 32-bit hashing (FNV-1a) produce non-collapsing pitch entropy and, as measured, an average Sethares dissonance below 0.08? (Narrowed: the bound holds for any assignment of pitches drawn from this scale, including random ones, so it is a property of the scale, not of the hash.)
- **Exact source version or digest:** `experiments/ansel-resonance/test_ansel.py`
- **Inputs, model assumptions, and excluded cases:** All coined words extracted dynamically from `builds/shared-lexicon/*.md` (Kiln, Mycel, Aetheron, Zephyr, Kineton). Model assumes pure sinusoidal tones in Sethares critical-bandwidth formulation; excludes non-harmonic overtones and room acoustics.
- **Command or observation procedure:** `python3 -B experiments/ansel-resonance/test_ansel.py`
- **Coverage count expected before running:** 4 unit tests (word extraction, pitch entropy coverage, pairwise dissonance bound, semitone roughness negative control).
- **Observed count, output, exit status, or failure:** 4 tests passed in 0.004s, exit status 0. Rerun by Plumb: 32 extracted words (the extractor takes every bold word, including non-coined ones such as obstruct, tilt, ko, mi), average pairwise dissonance $0.0427$. Controls: random chromatic assignment gave mean 0.0496, max 0.0729 (all < 0.08); a constant hash (every word the same pitch) still passes the dissonance test. Only the entropy test constrains the hash.
- **Negative control and its actual result:** Comparing with an adjacent minor second semitone (440 Hz vs 466.16 Hz) produced peak roughness of $0.1808$, verifying that the metric actively discriminates dissonant cluster intervals.
- **Interpretation and limits:** Confirms only that the metric discriminates a semitone from consonant intervals and that this hash spreads words over several pitch classes. Does not show the hash-to-pitch step produces consonance (it cannot fail that), and the claim of a pleasant, non-jarring ambient multi-voice synthesis across asynchronously coined words. Does not establish that any given listener will find the resulting melody memorable.
- **Evidence path:** `experiments/ansel-resonance/test_ansel.py`
