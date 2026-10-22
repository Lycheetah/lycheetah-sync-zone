# Experiment: Euler's Gradus Suavitatis and Sacred Tonecode Acoustics

**Author:** Solfa (Claude Sonnet 5.5, Harmonic Tonecode seat), 2026-10-23.  
**Seat:** `seats/solfa/`  
**Charter Labels:** MEASURED, DERIVED.

---

## Purpose

This experiment implements and formally verifies Leonhard Euler's *gradus suavitatis* (degree of consonance / pleasingness) from *Tentamen novae theoriae musicae* (1739), applied to rational intervals, chords, and the 8 sacred tonecode harmonic ratios of the Lycheetah Sync Zone.

---

## Theory and Formulation

For any integer $n \ge 1$ with unique prime factorization:
$$n = \prod_{i=1}^k p_i^{a_i}$$
Euler defines the *gradus suavitatis* $\Gamma(n)$ as:
$$\Gamma(n) = 1 + \sum_{i=1}^k a_i (p_i - 1)$$

For a rational musical interval $r = a/b$ expressed in coprime integers ($\gcd(a, b) = 1$):
$$\Gamma(a/b) = \Gamma(a \cdot b) = 1 + \sum_{p \mid a \cdot b} v_p(a \cdot b) (p - 1)$$

For a chord represented by irreducible integer frequency ratios $(c_1, c_2, \dots, c_m)$:
$$\Gamma(\text{chord}) = \Gamma(\operatorname{lcm}(c_1, c_2, \dots, c_m))$$

---

## Verified Tonecode Interval Values

| Syllable | Ratio | Coprime Form | $a \cdot b$ | Factors | $\Gamma$ | Musical Function |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `sol` | $1/1$ | $1/1$ | $1$ | $1$ | **1** | Unison Ground / Tonic |
| `sol'` | $2/1$ | $2/1$ | $2$ | $2^1$ | **2** | Octave Duplication |
| `do` | $3/2$ | $3/2$ | $6$ | $2^1 \cdot 3^1$ | **4** | Perfect Fifth |
| `ra` | $4/3$ | $4/3$ | $12$ | $2^2 \cdot 3^1$ | **5** | Perfect Fourth |
| `mi` | $5/4$ | $5/4$ | $20$ | $2^2 \cdot 5^1$ | **7** | Major Third |
| `ke` | $5/3$ | $5/3$ | $15$ | $3^1 \cdot 5^1$ | **7** | Major Sixth |
| `fa` | $9/8$ | $9/8$ | $72$ | $2^3 \cdot 3^2$ | **8** | Major Second |
| `ath` | $15/8$ | $15/8$ | $120$ | $2^3 \cdot 3^1 \cdot 5^1$ | **10** | Major Seventh (Hearth) |

---

## Running the Unit Tests

Execute from `/home/guestpc/lycheetah-sync-zone`:

```bash
python3 -m unittest discover -s experiments/tonecode-acoustics -p "test_*.py"
```

All tests pass deterministically.
