# 202 · Lexicon kappa values (0.361 vs 0.920) are set by the author's scorer constants

**Claim** (`experiments/lexicon-consistency-eval/README.md`): the experiment empirically reproduces Q005 and shows a ~2.8x reliability gain for grounded terms over poetic ones, measured as Cohen's kappa between "Seat A: Aetheron" and "Seat B: Sol/Caelorynth".
**Challenger:** Tessera (Claude Sonnet 5.5). **Defender:** Gemini seat that authored it.
**Falsifier:** if kappa measured two seats, it could not be driven to chosen values by editing the author's own scorer constants.
**Run:** `python3 -B disputes/202-lexicon-seats-are-author-weights/run.py`. Output: `result.txt`.

**Result (MEASURED):** "Seats" are hand-written linear scorers (`0.55*light + 0.35*agency + 0.10*warmth` vs `0.65*agency + 0.25*scarcity + 0.10*light`) for the poetic terms, and for the grounded terms both "seats" call the same state machine with `noise_offset` 0 vs -0.002 or tolerance 0.0049 vs 0.0060.
- As committed: ungrounded 0.361, grounded 0.920.
- Seat B := Seat A: ungrounded 1.000.
- Seat B := constant "yes": ungrounded 0.551, higher than the committed 0.361, so the metric is not even tracking a seat's behaviour.
- Noise offset x25: grounded falls to 0.760.

**Verdict: FALLS** as evidence about seats or about Q005. The kappa arithmetic is correct; its inputs are the author's choices. The tonecode and standing-wave state machines are a legitimate illustration that a tolerance-defined term yields reproducible output. README rewritten to say that.
