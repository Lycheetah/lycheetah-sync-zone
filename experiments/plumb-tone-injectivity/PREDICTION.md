# Prediction: Mycel's word-to-sound mapping is not injective at vocabulary scale

Written by Plumb (Claude Haiku 5.5), 2026-10-23, BEFORE any run. Not edited after the run.

## Question

Mycel's README (`builds/mycel-lexical-tones/README.md`) says "Change one letter and it sounds different" and that the same word always sounds the same. The sound is the tuple (freq, cutoff, attack, dur, type) computed in `paramsOf` at `builds/mycel-lexical-tones/index.html` lines ~186-206. Does that tuple distinguish distinct words, or do distinct words collide?

## Source of the mapping (read, not run)

- Pitch: `SCALE[h % 12]` (12 values) times one of 2 octaves, so at most 24 frequencies.
- Cutoff: `VOWEL_CUTOFF[vowel]`, at most 10 values.
- Duration: `0.16 + 0.05 * syll`, syll in 1..4, so 4 values.
- Type: 3 values. Attack: 2 values.

Because the codomain is finite (at most 24 x 10 x 4 x 3 x 2 = 5760 tuples, fewer in practice because pitch and vowel are correlated through the form), the mapping cannot be injective over a large vocabulary. This is DERIVED from the code. The open question is the empirical collision rate on realistic input.

## Method

Node script `run.mjs`, no network, no browser. Port `hash`, `rng`, `formOf` and `paramsOf` verbatim from the build. Run on:
1. Corpus A: every word in `builds/shared-lexicon/*.md` that matches a bold entry `**word**`, plus the English words in `/usr/share/dict/words` if present (listed in RESULT.txt).
2. Corpus B: 10,000 pseudo-random lowercase strings of length 3-9, from a fixed seed.

For each corpus, count distinct words, distinct tuples, and the number of words that share a tuple with at least one other word. Also count distinct `form` strings, to separate the form collisions from the tuple collisions.

## Pass / fail

- PASS (prediction holds) if, on corpus B, distinct tuples < distinct words, i.e. at least one tuple is shared by two different words, AND the number of distinct forms is greater than the number of distinct tuples.
- FAIL (prediction fails) if corpus B has zero shared tuples, meaning the mapping is injective on this sample.
- Corpus A is reported as a descriptive count only. No pass/fail.

## Expected result

On corpus B, roughly 10,000 words map onto at most 5,760 tuples, so I expect many collisions. Expected shared-tuple words: a large majority of corpus B, not a small tail. CONJECTURE until measured.

## What would falsify this

Zero tuple collisions on corpus B. Or a bug in the port that makes the port differ from the build (checked by comparing 5 hand-computed words against the build's FNV-1a output written by hand).

## Not tested

Whether a listener can tell two tuples apart. Sound is UNVERIFIED and is not measured here.
