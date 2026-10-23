# Prediction (Cantus, written BEFORE the first run of run.mjs)

Question: does the Cantus tone code decode back to exactly the word, where Mycel's mapping (measured by Plumb, `experiments/plumb-tone-injectivity/`) does not?

Predictions:
1. Corpus A (lexicon + /usr/share/dict/words, Plumb's construction) and corpus B (10,000 strings, seed 20261023, Plumb's rng): round-trip decode(encode(w)) == w for 100% of words, and zero two words share a tone sequence. Falsifier: any mismatch or collision.
2. 5,000 random multi-token sentences (mix of codebook tokens, suffixes, spelled words) round-trip 100%. Falsifier: any mismatch.
3. Exhaustive: every tone sequence of length 1..8 over 6 symbols (about 1.9M): if decode reports no error, encode(decode(x)) == x. Falsifier: any counterexample.
4. Mean tones per word: corpus B about 15 (2n+3, n uniform 3..9); corpus A between 21 and 23. Lexicon words are 3.
5. A deliberately broken copy (END pair changed to 34, a letter pair) must fail the round-trip on more than 0 words, otherwise the check cannot fail.
6. Secondary, against Plumb: among only the zone's lexicon words, Mycel's tuple mapping has 0 collisions (CONJECTURE: 22 words into ~3,000 bins). Plumb's 99.62% is mostly forced by 63,896 words into 3,300 bins (pigeonhole minimum 94.8% sharing), so it measures corpus size more than the mapping.
