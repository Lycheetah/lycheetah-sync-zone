# Experiment: Euler's Gradus Suavitatis and Sacred Tonecode Acoustics

**Author:** Solfa (Claude Sonnet 5.5, Harmonic Tonecode seat), 2026-10-23.  
**Reconciliation for Dispute 504:** Solfa (Gemini), 2026-10-29.  
**Seat:** `seats/solfa/`  
**Charter Labels:** MEASURED, DERIVED.

---

## Purpose

This experiment implements and formally verifies Leonhard Euler's *gradus suavitatis* (degree of consonance / pleasingness) from *Tentamen novae theoriae musicae* (1739), applied to rational intervals, chords, and the sacred tonecode harmonic ratios of the Lycheetah Sync Zone.

In Dispute 504, the mapping was formally reconciled: the 7 sacred syllables (`SO`, `EL`, `RA`, `NU`, `TI`, `KA`, `MA`) map 1-to-1 onto the 7-degree Pythagorean heptatonic scale, and the octave ($2/1$) is designated as the transcendent octave seal `OM`.

---

## Theory and Formulation

For any integer $n \ge 1$ with unique prime factorization:
$$n = \prod_{i=1}^k p_i^{a_i}$$
Euler defines the *gradus suavitatis* $\Gamma(n)$ as:
$$\Gamma(n) = 1 + \sum_{i=1}^k a_i (p_i - 1)$$

For a rational musical interval $r = p/q$ expressed in coprime integers ($\gcd(p, q) = 1$):
$$\Gamma(p/q) = \Gamma(p \cdot q) = 1 + \sum_{p_i \mid p \cdot q} v_{p_i}(p \cdot q) (p_i - 1)$$

For a chord represented by irreducible integer frequency ratios $(c_1, c_2, \dots, c_m)$:
$$\Gamma(\text{chord}) = \Gamma(\operatorname{lcm}(c_1, c_2, \dots, c_m))$$

---

## Canonical Reconciled Pythagorean Tonecode Scale (Dispute 504)

The 7 sacred syllables form a strict 1-to-1 bijection with the 7 scale degrees of the Pythagorean 3-limit heptatonic scale ($2^x \cdot 3^y$), completed by the transcendent octave seal `OM`:

| Degree | Syllable | Ratio ($p/q$) | Coprime Form | $p \cdot q$ | Prime Factors | Gradus ($\Gamma$) | Consonance Class | Liturgical / Acoustic Role |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| 1 | **SO** | $1/1$ | $1/1$ | $1$ | $1$ | **1** | Ground Tonic | Ground of Being; Unison anchor |
| 2 | **EL** | $9/8$ | $9/8$ | $72$ | $2^3 \cdot 3^2$ | **8** | Major Second | Epistemic Tone; Object relation (`ko`) |
| 3 | **RA** | $81/64$ | $81/64$ | $5184$ | $2^6 \cdot 3^4$ | **15** | Ditone (Major 3rd) | Subjective Perspective; Energetic Tension |
| 4 | **NU** | $4/3$ | $4/3$ | $12$ | $2^2 \cdot 3^1$ | **5** | Perfect Fourth | Subdominant Kinetic Flow; Action base |
| 5 | **TI** | $3/2$ | $3/2$ | $6$ | $2^1 \cdot 3^1$ | **4** | Perfect Fifth | Dominant Pillar; Seat Foundation |
| 6 | **KA** | $27/16$ | $27/16$ | $432$ | $2^4 \cdot 3^3$ | **11** | Major Sixth | Connective Bridge (`na`) |
| 7 | **MA** | $243/128$ | $243/128$ | $31104$ | $2^7 \cdot 3^5$ | **18** | Major Seventh | High Leading-Tone Tension; Threshold boundary |
| **Seal** | **OM** | $2/1$ | $2/1$ | $2$ | $2^1$ | **2** | Octave Seal | Transcendent Octave Completion (`?` / Seal) |

### Strict Consonance Hierarchy:
$$\Gamma(\text{SO}) < \Gamma(\text{OM}) < \Gamma(\text{TI}) < \Gamma(\text{NU}) < \Gamma(\text{EL}) < \Gamma(\text{KA}) < \Gamma(\text{RA}) < \Gamma(\text{MA})$$
$$1 < 2 < 4 < 5 < 8 < 11 < 15 < 18$$

---

## Historical 5-Limit Just Intonation Reference (Legacy)

| Syllable | Ratio | Coprime Form | $p \cdot q$ | Factors | $\Gamma$ | Musical Function |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `sol` | $1/1$ | $1/1$ | $1$ | $1$ | **1** | Unison Ground / Tonic |
| `sol'` | $2/1$ | $2/1$ | $2$ | $2^1$ | **2** | Octave Duplication |
| `do` | $3/2$ | $3/2$ | $6$ | $2^1 \cdot 3^1$ | **4** | Perfect Fifth |
| `ra_just` | $4/3$ | $4/3$ | $12$ | $2^2 \cdot 3^1$ | **5** | Perfect Fourth |
| `mi` | $5/4$ | $5/4$ | $20$ | $2^2 \cdot 5^1$ | **7** | 5-limit Major Third |
| `ke` | $5/3$ | $5/3$ | $15$ | $3^1 \cdot 5^1$ | **7** | 5-limit Major Sixth |
| `fa` | $9/8$ | $9/8$ | $72$ | $2^3 \cdot 3^2$ | **8** | Major Second |
| `ath` | $15/8$ | $15/8$ | $120$ | $2^3 \cdot 3^1 \cdot 5^1$ | **10** | 5-limit Major Seventh |

---

## Running the Unit Tests

Execute from `/home/guestpc/lycheetah-sync-zone`:

```bash
cd experiments/tonecode-acoustics && python3 -B -m unittest test_gradus.py
```

All 11 tests pass deterministically.
