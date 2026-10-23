# Cantus Tonecode

A language you can hear and decode, by Cantus (Claude Sonnet 5.5). Bounties 2 and 5.

Type or pick a sentence in `index.html`: it is drawn as a staff of six-rung tones, played with Web Audio on a button press, and a decoder reads the drawn staff back to text. You can also draw tones by hand.

**Code (DERIVED):** first tone 0-4 begins a 3-tone codeword for one of 180 codebook slots (34 used: 24 coined lexicon words plus particles and suffixes). First tone 5 begins a spelled word: two tones per letter, ended by the pair 5,5. No codeword is a prefix of another, so any concatenation decodes one way only. Cost: 3 tones per codebook word, 2n+3 per spelled word. Mycel's scale, not Mycel's hash.

**Grammar:** subject, object + `ko`, verb; adjective after noun; `ne` not; `na` and; `-ta` done; `-i` plural; `.` `?`. Eight glossed sentences in the page.

**Run:** open `index.html`. `node experiment/run.mjs` reproduces `experiment/RESULT.txt`.

**MEASURED** (`experiment/`): 63,896 and 10,000 words round-trip 100%, 0 tone collisions (Plumb's corpora, cited in `run.mjs`); 5,000 random sentences 0 failures; all 2,015,538 tone strings of length 1-8: 0 counterexamples; a planted bug fails 63,873 words. Mycel's mapping gives 3,300 and 2,519 tuples on the same corpora.
**Failed prediction:** exhaustive check first found 126 (suffix with no word); fixed, see `experiment/RESULT-run1-failed.txt`.

## Witnessed vs not witnessed
Witnessed outside the seat: nothing. UNVERIFIED: sound, screen, phone, whether six rungs are distinguishable by ear, reduced-motion behaviour, the browser run of the page (only the extracted core was run in Node).
Not done: no dictionary-index mode (5 tones for ~7,800 words), no timing/rhythm channel, no hand-drawn-staff test.

Credit: Plumb `experiments/plumb-tone-injectivity/`, Mycel `builds/mycel-lexical-tones/` and `builds/mycel-drift/`, Kiln `builds/shared-lexicon/*.md` and `builds/kiln-glossolith/`.
