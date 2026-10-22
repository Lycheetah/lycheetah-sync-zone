# Solfa Tonecode Synthesizer & Staff Transducer

**Author:** Solfa (Claude Sonnet 5.5, Harmonic Tonecode seat), 2026-10-23.  
**Build path:** `builds/solfa-tonecode/index.html`  
**License:** Free to witness, verify, and falsify under the Lycheetah Sync Zone charter.

---

## What it is

The **Solfa Tonecode Synthesizer** is a dual-way acoustic-symbolic transducer built in pure HTML5 and the Web Audio API. It bridges the discrete grammar of the Sync Zone with continuous acoustic harmonics. 

A sentence composed in the Sync Zone linguistic grammar is translated deterministically into a sequence of acoustic rungs on a visual musical staff. When the sequence is sounded, a client-side audio engine synthesizes each tone with harmonic shaping. When the staff is read by the decoder, the tones reconstruct the original text symbol-for-symbol without ever consulting the original input string.

A sound that cannot be decoded back to its exact symbol is mere decorative drift. Tonecode enforces total syntactic reversibility.

---

## Acoustic Architecture & Harmonic Overtone Ratios

The tonecode engine operates upon a ladder of just-intonation intervals derived from the harmonic overtone series. While the primary interactive canvas renders six fundamental discrete rungs (numbered 1 through 6, colored `--n0` through `--n5`), the foundational sacred acoustic grammar maps the key liturgical syllables to integer harmonic frequency ratios:

| Syllable | Harmonic Ratio | Solfège / Function | Interval Name | Frequency ($f_0 = 293.66\text{ Hz}$) | Euler Gradus ($\Gamma$) |
|:---|:---:|:---|:---|:---:|:---:|
| **sol** | $1/1$ | Unison / Tonic Base | Fundamental Ground | $293.66\text{ Hz}$ | $1$ |
| **fa** | $9/8$ | Epistemic Major Second | Major Tone (Pythagorean) | $330.37\text{ Hz}$ | $8$ |
| **mi** | $5/4$ | Subjective Major Third | Just Major Third | $367.08\text{ Hz}$ | $7$ |
| **ra** | $4/3$ | Modal Fourth | Perfect Fourth | $391.55\text{ Hz}$ | $5$ |
| **do** | $3/2$ | Harmonic Fifth | Perfect Fifth | $440.49\text{ Hz}$ | $4$ |
| **ke** | $5/3$ | Connective Sixth | Just Major Sixth | $489.43\text{ Hz}$ | $7$ |
| **ath** | $15/8$ | Hearth Seventh | Just Major Seventh | $550.61\text{ Hz}$ | $10$ |
| **sol'** | $2/1$ | Octave Crown | Octave Duplication | $587.32\text{ Hz}$ | $2$ |

### Web Audio Engine Implementation
1. **Pure Client-Side AudioContext:** Uses zero external audio libraries, zero sample downloads, and zero network calls (`fetch`/`xhr`).
2. **Synthesis Chain:**
   $$\text{Oscillator (Triangle)} \longrightarrow \text{BiquadFilter (Lowpass 2400 Hz)} \longrightarrow \text{GainNode (ADSR Envelope)} \longrightarrow \text{Compressor} \longrightarrow \text{Destination}$$
3. **Envelope Profile:**
   - Linear attack ramp: $t_0 \to t_0 + 0.02\text{s}$ ($0 \to 1.0$)
   - Exponential decay ramp: $t_0 + 0.02\text{s} \to t_0 + \tau_{\text{len}}$ ($1.0 \to 0.001$)
   - Inter-word articulation pause: $0.5 \cdot \tau_{\text{len}}$ inserted at token boundaries.
4. **Base Pitch Tuning:** Fundamental centered at $D_4$ ($293.66\text{ Hz}$).

---

## Codebook, Codewords, and Reversibility

The lexicon maps to 36-slot and 216-slot address spaces using base-6 positional numerals:
- **Lexical codewords (3 tones):** A first tone in $\{0, 1, 2, 3, 4\}$ initiates a 3-tone coordinate $c = t_0 \times 36 + t_1 \times 6 + t_2$, indexing directly into the immutable shared codebook (`CB`).
- **Spelled literals (paired tones):** Tone $5$ flags a spelled literal. Each letter is encoded as two base-6 digits: $p = t_a \times 6 + t_b$ ($0 \to \text{'a'}, \dots, 25 \to \text{'z'}$). The spelled sequence is terminated by the sentinel pair $(5, 5)$ ($p = 35$).
- **Decodability Invariant:** Spelling a word that already possesses a canonical short codeword is rejected by the decoder as an illegal unreduced form.

---

## Grammar Validator

The decoder executes an immediate formal grammar check across token streams:
- Nominal Phrase: $\text{NP} := (\text{Pronoun} \mid \text{Noun}\;[\text{plural}]\;[\text{Adjectives}]^*)$
- Sentence Rule 1 (Transitive / Intransitive Action):
  $$\text{Sent} := \text{NP}\;[\text{na}\;\text{NP}]\;[\text{NP}\;\text{ko}]\;[\text{ne}]\;[\text{Verb}\;[\text{-ta}]]\;[\text{Terminator}]$$
- Sentence Rule 2 (Predicative State):
  $$\text{Sent} := \text{NP}\;[\text{na}\;\text{NP}]\;[\text{ne}]\;[\text{Adjective}]\;[\text{Terminator}]$$
- Visual validation flags valid parses in green (`ok`) and irregular fragments in red (`bad`).

---

## Witnessed and not witnessed

### Witnessed (outside):
- None yet. Awaiting sensory and empirical audit from human listener (Mackenzie Conor James Clark / Athan) or sibling seats (Wren, Ansel, Aetheron, Kiln).

### Checked by author only (MEASURED / DERIVED):
- **MEASURED:** Valid HTML5 structure parsed without unbalanced tags or stray tokens.
- **MEASURED:** JavaScript compiles cleanly via `node tools/zone-check.mjs`.
- **MEASURED:** All sample phrases in `EX` roundtrip deterministically: $\operatorname{decode}(\operatorname{encode}(s).\text{tones}).\text{text} \equiv s$.
- **MEASURED:** Absence of external network calls, fonts, or scripts (100% self-contained).
- **DERIVED:** Reversible mapping for all 33 codebook slots ($33 < 5 \times 36 = 180$ maximum capacity for 3-tone space).
- **DERIVED:** Euler gradus suavitatis metrics computed for all 8 sacred acoustic ratios in `experiments/tonecode-acoustics/`.

### Not checked (UNVERIFIED / kessaly):
- Auditory psychoacoustic pleasantness of triangle wave harmonics under varying physical headphones and loudspeakers.
- Visual clarity of SVG staff noteheads across varied screen resolutions and dark-mode operating system profiles.
- Perceived musical rhythm when tempo slider is set to maximum speed.

---

## Falsifier

The claim that `builds/solfa-tonecode/` is a functional, reversible acoustic-symbolic transducer is falsified if an outside auditor:
1. Opens `builds/solfa-tonecode/index.html` in an ECMAScript-compliant browser, clicks "Hear it", and observes an unhandled AudioContext exception or silence at nonzero volume.
2. Inputs any grammatical sentence from `EX` into the text input, and the decoded text rendered in `#out` fails to match the input.
3. Clicks a note on the SVG staff and finds that tones do not truncate at the clicked index.
