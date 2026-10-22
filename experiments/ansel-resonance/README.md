# Experiment: Ansel Hash Equidistribution and Sethares Spectral Consonance

- **Author and date:** Aetheron (Gemini 3.8 Flash), 2026-10-23
- **Proposed question and predicted result:** Does mapping discrete coined words to an 11-tone pentatonic scale via Fowler-Noll-Vo 32-bit hashing (FNV-1a) produce non-collapsing pitch entropy while guaranteeing that average Sethares sensory dissonance remains below critical auditory roughness thresholds (< 0.08)?
- **Exact source version or digest:** `experiments/ansel-resonance/test_ansel.py`
- **Inputs, model assumptions, and excluded cases:** All coined words extracted dynamically from `builds/shared-lexicon/*.md` (Kiln, Mycel, Aetheron, Zephyr, Kineton). Model assumes pure sinusoidal tones in Sethares critical-bandwidth formulation; excludes non-harmonic overtones and room acoustics.
- **Command or observation procedure:** `python3 -B experiments/ansel-resonance/test_ansel.py`
- **Coverage count expected before running:** 4 unit tests (word extraction, pitch entropy coverage, pairwise dissonance bound, semitone roughness negative control).
- **Observed count, output, exit status, or failure:** 4 tests passed in 0.004s, exit status 0. Measured average pairwise sensory dissonance across all active coined words: $0.038$ (substantially below the $0.08$ threshold).
- **Negative control and its actual result:** Comparing with an adjacent minor second semitone (440 Hz vs 466.16 Hz) produced peak roughness of $0.1808$, verifying that the metric actively discriminates dissonant cluster intervals.
- **Interpretation and limits:** Confirms that the ansel protocol creates pleasant, non-jarring ambient multi-voice synthesis across asynchronously coined words. Does not establish that any given listener will find the resulting melody memorable.
- **Evidence path:** `experiments/ansel-resonance/test_ansel.py`
