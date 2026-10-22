#!/usr/bin/env python3
"""
Euler's Gradus Suavitatis (Degree of Consonance / Pleasingness)
Implemented for the Lycheetah Sync Zone by Solfa (Harmonic Tonecode seat).

Theory:
Leonhard Euler, "Tentamen novae theoriae musicae" (1739).
For an integer n with prime factorization n = p_1^{a_1} ... p_k^{a_k}:
    Gamma(n) = 1 + sum_{i=1}^k a_i * (p_i - 1)

For a rational interval in lowest terms r = a/b where gcd(a, b) = 1:
    Gamma(a/b) = Gamma(a * b) = 1 + sum_{p | (a*b)} v_p(a * b) * (p - 1)

For a chord of integer pitch relationships (c_1, c_2, ..., c_m):
    Gamma(chord) = Gamma(lcm(c_1, c_2, ..., c_m))
"""

from __future__ import annotations
import math
from functools import reduce


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
    """Compute Euler's gradus suavitatis for an integer n >= 1."""
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
    Reduces fraction to lowest terms before computing Gamma(a * b).
    """
    if not isinstance(numerator, int) or not isinstance(denominator, int):
        raise TypeError("Numerator and denominator must be integers.")
    if numerator <= 0 or denominator <= 0:
        raise ValueError("Numerator and denominator must be strictly positive.")

    g = math.gcd(numerator, denominator)
    a = numerator // g
    b = denominator // g
    return gradus_suavitatis_int(a * b)


def gradus_ratio(ratio_str: str) -> int:
    """Parse a fraction string 'a/b' or integer 'n' and return its gradus."""
    parts = ratio_str.strip().split("/")
    if len(parts) == 1:
        return gradus_suavitatis_int(int(parts[0]))
    elif len(parts) == 2:
        return gradus_interval(int(parts[0]), int(parts[1]))
    else:
        raise ValueError(f"Invalid ratio string format: '{ratio_str}'")


def _lcm(a: int, b: int) -> int:
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


# Canonical 8 Sacred Tonecode Ratios
SACRED_TONECODE_RATIOS: dict[str, tuple[int, int]] = {
    "sol": (1, 1),
    "fa": (9, 8),
    "mi": (5, 4),
    "ra": (4, 3),
    "do": (3, 2),
    "ke": (5, 3),
    "ath": (15, 8),
    "sol'": (2, 1),
}


def gradus_syllable(syllable: str) -> int:
    """Compute the gradus suavitatis for a named tonecode syllable."""
    s = syllable.lower().strip()
    if s not in SACRED_TONECODE_RATIOS:
        raise KeyError(f"Unknown sacred tonecode syllable: '{syllable}'")
    num, den = SACRED_TONECODE_RATIOS[s]
    return gradus_interval(num, den)


if __name__ == "__main__":
    print("Euler's Gradus Suavitatis for Sacred Tonecode Syllables:")
    print("-" * 50)
    for syl, (num, den) in SACRED_TONECODE_RATIOS.items():
        g = gradus_interval(num, den)
        print(f"Syllable: {syl:>5} | Ratio: {num:>2}/{den:<2} | Gradus: {g:>2}")
