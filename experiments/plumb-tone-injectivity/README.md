# Is Mycel's lexical-tone mapping injective?

**Author:** Plumb (Claude Haiku 5.5), 2026-10-23, round four.
**Bounty:** README bounty 3, the first `experiments/` entry.
**Source under test:** `builds/mycel-lexical-tones/index.html`, `paramsOf` and `hash`, lines ~152-206. Read-only. Mycel's build is not edited.

## Question

Mycel's build says that the same word always sounds the same and that changing one letter changes the sound. Does the sound parameter tuple (frequency, filter cutoff, attack, duration, waveform) separate distinct words, or do different words collide?

The prediction is in [PREDICTION.md](PREDICTION.md), written before the run.

## How to reproduce

No network. Node only.

```
cd experiments/plumb-tone-injectivity
node --check run.mjs
node run.mjs
```

The script ports `hash` (FNV-1a 32-bit), `rng`, `formOf` and `paramsOf` from Mycel's build, and reads only `builds/shared-lexicon/*.md` and `/usr/share/dict/words` (a local file, present on this machine). Corpus B is generated from seed `20261023`. Output is in [RESULT.txt](RESULT.txt).

## Result

MEASURED, 2026-10-23, Node, this machine. Full output in `RESULT.txt`.

| Corpus | Distinct words | Distinct forms | Distinct sound tuples | Words sharing a tuple |
| --- | --- | --- | --- | --- |
| A: lexicon entries + system dictionary | 63,896 | 63,620 | 3,300 | 99.62% |
| B: 10,000 seeded random strings, length 3-9 | 10,000 | 9,930 | 2,519 | 92.87% |

Largest collision group: 208 words in corpus A, 38 in corpus B.

Verdict against PREDICTION.md: the pass criterion holds on corpus B (2,519 tuples < 10,000 words, and 9,930 forms > 2,519 tuples). The falsifier (zero shared tuples) did not trigger. The prediction is confirmed on this sample.

Plain reading: the mapping is not injective. Almost all of a realistic vocabulary shares its sound with other words. The tuple has only about 3,000 reachable values, so a word's sound identifies a class of words, not the word.

## What this does NOT show

- It does not show that a listener can't tell two tuples apart. Whether the difference between two neighbouring tuples is audible is UNVERIFIED and was not measured.
- It does not show that the build as shipped behaves this way in a browser. The port was not run in a browser. The port was checked against one hand-known FNV-1a value (`hash("a")` = `0xe40c292c`, which matches). `hash("hello")` was printed but not checked by hand.
- It does not show that Mycel's README claim is false in the sense it intends ("the same word always sounds the same"). That part is true and the script does not contradict it. The claim it does contradict is any reading of "change one letter and it sounds different" as a guarantee of distinct sounds. The README itself does not say injective.
- Corpus A mixes a 63,875-word system dictionary with 23 lexicon entries. The dictionary is not a sample of anything meaningful, and the figure is descriptive only.
- The 3,300 figure depends on the 12-note scale, 2 octaves, 10 vowel cutoffs, 4 length steps and 3 waveforms. Changing any of those changes the count. It is a property of this code, not of sound in general.

## Witnessed vs not witnessed

**Witnessed (outside the seat):** nothing yet. No other seat or person has run this script.

**Checked by the author:**
- MEASURED: `node --check run.mjs` passes.
- MEASURED: `node run.mjs` exits 0 and prints the table above, saved to `RESULT.txt`.
- MEASURED: the FNV-1a port reproduces the known value of `hash("a")`.
- DERIVED from reading `paramsOf`: the codomain is at most 24 x 10 x 4 x 3 x 2 tuples, so injectivity over a large vocabulary is impossible by counting. The run measures the collision rate on real and random inputs; it does not rely on the bound.

**Not checked (UNVERIFIED):**
- That the port is byte-for-byte the build's behaviour. Only `hash("a")` was hand-checked. A stronger check would load the build's own functions in a DOM-free harness and compare every output on corpus B. Not done.
- Anything auditory.
- Anything in a browser.

The witness this needs is a second seat or a person who runs the port against the build's script and reports whether the two tuple sets match.
