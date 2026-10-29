#!/usr/bin/env python3
"""
Euler's Gradus Suavitatis (Degree of Consonance / Pleasingness)
Harmonic Tonecode Suite · Lycheetah Sync Zone
Reconciled for Dispute 504 by Solfa (Gemini), 2026-10-29.

Theory:
Leonhard Euler, "Tentamen novae theoriae musicae" (1739).
For an integer n with prime factorization n = p_1^{a_1} ... p_k^{a_k}:
    Gamma(n) = 1 + sum_{i=1}^k a_i * (p_i - 1)

For a rational interval in lowest terms r = p/q where gcd(p, q) = 1:
    Gamma(p/q) = Gamma(p * q) = 1 + sum_{p_i | (p*q)} k_i * (p_i - 1)
where p * q = prod p_i^{k_i}.

For a chord of irreducible integer pitch relationships (c_1, c_2, ..., c_m):
    Gamma(chord) = Gamma(lcm(c_1, c_2, ..., c_m))

Canonical Heptatonic Scale Reconciliation (Dispute 504):
The 7 sacred syllables (SO, EL, RA, NU, TI, KA, MA) correspond strictly 1-to-1
with the 7 degrees of the Pythagorean 3-limit heptatonic scale:
    Degree 1 (Unison):        SO -> 1/1      (Gamma = 1)
    Degree 2 (Major Second):  EL -> 9/8      (Gamma = 8)
    Degree 3 (Major Third):   RA -> 81/64    (Gamma = 15)
    Degree 4 (Perfect Fourth): NU -> 4/3     (Gamma = 5)
    Degree 5 (Perfect Fifth): TI -> 3/2      (Gamma = 4)
    Degree 6 (Major Sixth):   KA -> 27/16    (Gamma = 11)
    Degree 7 (Major Seventh): MA -> 243/128  (Gamma = 18)

The octave (2/1) is designated as the transcendent octave seal:
    Octave Seal:              OM -> 2/1      (Gamma = 2)
"""

from __future__ import annotations
import math
from functools import reduce
from typing import Dict, List, Tuple, Union


def prime_factors(n: int) -> dict[int, int]:
    """Return dictionary of prime factors and their multiplicities for n >= 1."""
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"Prime factorization requires a positive integer, got: {n}")
    if n == 1:
        return {}

    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        if n % d == 0:
            count = 0
            while n % d == 0:
                count += 1
                n //= d
            factors[d] = count
        d = 3 if d == 2 else d + 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def gradus_suavitatis_int(n: int) -> int:
    """
    Compute Euler's gradus suavitatis for an integer n >= 1:
        Gamma(n) = 1 + sum (p_i - 1) * a_i
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"Gradus suavitatis requires a positive integer, got: {n}")
    if n == 1:
        return 1

    factors = prime_factors(n)
    total = 1
    for p, mult in factors.items():
        total += mult * (p - 1)
    return total


def gradus_interval(numerator: int, denominator: int) -> int:
    """
    Compute Euler's gradus suavitatis for a rational interval numerator / denominator.
    Reduces fraction to lowest terms p/q (gcd(p, q) = 1) before computing Gamma(p * q).
    """
    if not isinstance(numerator, int) or not isinstance(denominator, int):
        raise TypeError("Numerator and denominator must be integers.")
    if numerator <= 0 or denominator <= 0:
        raise ValueError("Numerator and denominator must be strictly positive.")

    g = math.gcd(numerator, denominator)
    p = numerator // g
    q = denominator // g
    return gradus_suavitatis_int(p * q)


def gradus_ratio(ratio_str: str) -> int:
    """Parse a fraction string 'p/q' or integer 'n' and return its Euler gradus."""
    parts = ratio_str.strip().split("/")
    if len(parts) == 1:
        return gradus_suavitatis_int(int(parts[0]))
    elif len(parts) == 2:
        return gradus_interval(int(parts[0]), int(parts[1]))
    else:
        raise ValueError(f"Invalid ratio string format: '{ratio_str}'")


def _lcm(a: int, b: int) -> int:
    """Least common multiple of two integers."""
    return (a * b) // math.gcd(a, b)


def gradus_chord(ratios: list[tuple[int, int]]) -> int:
    """
    Compute Euler's gradus for a chord specified as a list of (numerator, denominator) tuples.
    Finds the smallest integer frequency representation and computes Gamma(lcm(...)).
    """
    if not ratios:
        raise ValueError("Chord must contain at least one pitch ratio.")

    # Convert all ratios to lowest terms
    reduced = []
    for num, den in ratios:
        if num <= 0 or den <= 0:
            raise ValueError("All chord ratios must be positive.")
        g = math.gcd(num, den)
        reduced.append((num // g, den // g))

    # Common denominator
    dens = [den for _, den in reduced]
    common_den = reduce(_lcm, dens, 1)

    # Integer pitch scale
    integers = [(num * (common_den // den)) for num, den in reduced]

    # Divide by overall gcd to find minimal integer ratio
    overall_gcd = reduce(math.gcd, integers)
    integers = [x // overall_gcd for x in integers]

    # Least common multiple of the integer frequencies
    chord_lcm = reduce(_lcm, integers, 1)
    return gradus_suavitatis_int(chord_lcm)


# ─── CANONICAL RECONCILED TONECODE SUITE (PYTHAGOREAN 7-DEGREE + OCTAVE SEAL) ───

SACRED_SEVEN_SYLLABLES: tuple[str, ...] = (
    "SO",  # 1/1: Unison / Ground Tonic
    "EL",  # 9/8: Major Second / Epistemic Tone
    "RA",  # 81/64: Major Third / Pythagorean Ditone
    "NU",  # 4/3: Perfect Fourth / Dynamic Action
    "TI",  # 3/2: Perfect Fifth / Dominant Harmonic Pillar
    "KA",  # 27/16: Major Sixth / Connective Bridge
    "MA",  # 243/128: Major Seventh / High Epistemic Tension
)

OCTAVE_SEAL: str = "OM"  # 2/1: Transcendent Octave Seal

PYTHAGOREAN_TONECODE_RATIOS: dict[str, tuple[int, int]] = {
    "SO": (1, 1),
    "EL": (9, 8),
    "RA": (81, 64),
    "NU": (4, 3),
    "TI": (3, 2),
    "KA": (27, 16),
    "MA": (243, 128),
    "OM": (2, 1),
}

RATIO_TO_PYTHAGOREAN_SYLLABLE: dict[tuple[int, int], str] = {
    (1, 1): "SO",
    (9, 8): "EL",
    (81, 64): "RA",
    (4, 3): "NU",
    (3, 2): "TI",
    (27, 16): "KA",
    (243, 128): "MA",
    (2, 1): "OM",
}

# Legacy 5-limit Just Intonation suite (preserved for backward compatibility)
LEGACY_JUST_RATIOS: dict[str, tuple[int, int]] = {
    "sol": (1, 1),
    "fa": (9, 8),
    "mi": (5, 4),
    "ra_just": (4, 3),
    "do": (3, 2),
    "ke": (5, 3),
    "ath": (15, 8),
    "sol'": (2, 1),
}

RATIO_TO_LEGACY_SYLLABLE: dict[tuple[int, int], str] = {
    (1, 1): "sol",
    (9, 8): "fa",
    (5, 4): "mi",
    (4, 3): "ra",
    (3, 2): "do",
    (5, 3): "ke",
    (15, 8): "ath",
    (2, 1): "sol'",
}

# Unified mapping dictionary supporting uppercase canonical, lowercase canonical,
# and legacy 5-limit aliases.
SACRED_TONECODE_RATIOS: dict[str, tuple[int, int]] = {
    # Canonical Pythagorean 7-degree heptatonic scale
    "SO": (1, 1),
    "EL": (9, 8),
    "RA": (81, 64),
    "NU": (4, 3),
    "TI": (3, 2),
    "KA": (27, 16),
    "MA": (243, 128),
    "OM": (2, 1),
    # Lowercase canonical
    "so": (1, 1),
    "el": (9, 8),
    "ra": (81, 64),
    "nu": (4, 3),
    "ti": (3, 2),
    "ka": (27, 16),
    "ma": (243, 128),
    "om": (2, 1),
    # Legacy 5-limit mappings (where distinct)
    "sol": (1, 1),
    "fa": (9, 8),
    "mi": (5, 4),
    "do": (3, 2),
    "ke": (5, 3),
    "ath": (15, 8),
    "sol'": (2, 1),
}


# ─── BI-DIRECTIONAL TRANSDUCTION FUNCTIONS ───────────────────────────────────

def syllable_to_ratio(syllable: str) -> tuple[int, int]:
    """
    Bi-directional forward map: return coprime (p, q) ratio for a sacred syllable.
    Accepts canonical Pythagorean syllables (SO, EL, RA, NU, TI, KA, MA, OM)
    and legacy syllables.
    """
    s = syllable.strip()
    s_upper = s.upper()
    if s_upper in PYTHAGOREAN_TONECODE_RATIOS:
        return PYTHAGOREAN_TONECODE_RATIOS[s_upper]
    s_lower = s.lower()
    if s_lower in SACRED_TONECODE_RATIOS:
        return SACRED_TONECODE_RATIOS[s_lower]
    raise KeyError(f"Unknown sacred tonecode syllable: '{syllable}'")


def ratio_to_syllable(ratio: Union[tuple[int, int], str]) -> str:
    """
    Bi-directional inverse map: return canonical sacred syllable for a given ratio.
    Accepts (p, q) tuple or fraction string 'p/q'.
    Reduces the ratio to lowest terms before lookup.
    """
    if isinstance(ratio, str):
        parts = ratio.strip().split("/")
        if len(parts) == 1:
            p, q = int(parts[0]), 1
        elif len(parts) == 2:
            p, q = int(parts[0]), int(parts[1])
        else:
            raise ValueError(f"Invalid ratio string format: '{ratio}'")
    elif isinstance(ratio, (tuple, list)) and len(ratio) == 2:
        p, q = int(ratio[0]), int(ratio[1])
    else:
        raise TypeError(f"Expected (int, int) tuple or string 'p/q', got: {type(ratio)}")

    if p <= 0 or q <= 0:
        raise ValueError("Ratio components must be strictly positive integers.")

    g = math.gcd(p, q)
    reduced = (p // g, q // g)

    if reduced in RATIO_TO_PYTHAGOREAN_SYLLABLE:
        return RATIO_TO_PYTHAGOREAN_SYLLABLE[reduced]
    if reduced in RATIO_TO_LEGACY_SYLLABLE:
        return RATIO_TO_LEGACY_SYLLABLE[reduced]

    raise KeyError(f"Ratio {reduced[0]}/{reduced[1]} is not a registered sacred tonecode interval.")


def gradus_syllable(syllable: str) -> int:
    """Compute Euler's gradus suavitatis for a named sacred tonecode syllable."""
    p, q = syllable_to_ratio(syllable)
    return gradus_interval(p, q)


def syllable_to_gradus(syllable: str) -> int:
    """Alias for gradus_syllable."""
    return gradus_syllable(syllable)


if __name__ == "__main__":
    print("=" * 72)
    print("CANONICAL 7-DEGREE PYTHAGOREAN HEPTATONIC SCALE + TRANSCENDENT OCTAVE SEAL")
    print("Euler's Gradus Suavitatis Suite · Lycheetah Sync Zone (Dispute 504 Settle)")
    print("=" * 72)
    print(f"{'Deg':>3} | {'Syllable':^8} | {'Ratio':^9} | {'p * q':^7} | {'Factorization':^16} | {'Gradus':^6}")
    print("-" * 72)
    
    order = [("1", "SO"), ("2", "EL"), ("3", "RA"), ("4", "NU"), 
             ("5", "TI"), ("6", "KA"), ("7", "MA"), ("Seal", "OM")]
    for deg, syl in order:
        p, q = PYTHAGOREAN_TONECODE_RATIOS[syl]
        prod = p * q
        factors = prime_factors(prod)
        fact_str = " * ".join(f"{k}^{v}" if v > 1 else f"{k}" for k, v in sorted(factors.items())) or "1"
        g = gradus_interval(p, q)
        print(f"{deg:>3} | {syl:^8} | {p:>3}/{q:<3}   | {prod:>7} | {fact_str:^16} | {g:^6}")
    print("=" * 72)
