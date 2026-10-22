#!/usr/bin/env python3
"""
Unit tests for Euler's Gradus Suavitatis and Tonecode Sacred Acoustics.
Run with: python3 -m unittest discover -s experiments/tonecode-acoustics -p "test_*.py"
"""

import unittest
from euler_gradus import (
    prime_factors,
    gradus_suavitatis_int,
    gradus_interval,
    gradus_ratio,
    gradus_chord,
    gradus_syllable,
    SACRED_TONECODE_RATIOS,
)


class TestEulerGradus(unittest.TestCase):

    def test_prime_factors(self):
        self.assertEqual(prime_factors(1), {})
        self.assertEqual(prime_factors(2), {2: 1})
        self.assertEqual(prime_factors(12), {2: 2, 3: 1})
        self.assertEqual(prime_factors(72), {2: 3, 3: 2})
        self.assertEqual(prime_factors(120), {2: 3, 3: 1, 5: 1})
        with self.assertRaises(ValueError):
            prime_factors(0)
        with self.assertRaises(ValueError):
            prime_factors(-15)

    def test_integer_gradus(self):
        # Gamma(1) = 1
        self.assertEqual(gradus_suavitatis_int(1), 1)
        # Gamma(2) = 1 + (2 - 1) = 2
        self.assertEqual(gradus_suavitatis_int(2), 2)
        # Gamma(3) = 1 + (3 - 1) = 3
        self.assertEqual(gradus_suavitatis_int(3), 3)
        # Gamma(4) = Gamma(2^2) = 1 + 2*(1) = 3
        self.assertEqual(gradus_suavitatis_int(4), 3)
        # Gamma(5) = 1 + (5 - 1) = 5
        self.assertEqual(gradus_suavitatis_int(5), 5)
        # Gamma(6) = Gamma(2*3) = 1 + 1 + 2 = 4
        self.assertEqual(gradus_suavitatis_int(6), 4)
        # Gamma(12) = Gamma(2^2 * 3) = 1 + 2 + 2 = 5
        self.assertEqual(gradus_suavitatis_int(12), 5)

    def test_fundamental_intervals(self):
        """
        Verify historical Euler gradus values for classical intervals:
        Octave (2/1) = 2
        Fifth (3/2) = 4
        Fourth (4/3) = 5
        Major third (5/4) = 7
        Major sixth (5/3) = 7
        Minor third (6/5) = 8
        Major second (9/8) = 8
        Major seventh (15/8) = 10
        Unison (1/1) = 1
        """
        self.assertEqual(gradus_interval(1, 1), 1)
        self.assertEqual(gradus_interval(2, 1), 2)
        self.assertEqual(gradus_interval(3, 2), 4)
        self.assertEqual(gradus_interval(4, 3), 5)
        self.assertEqual(gradus_interval(5, 4), 7)
        self.assertEqual(gradus_interval(5, 3), 7)
        self.assertEqual(gradus_interval(6, 5), 8)
        self.assertEqual(gradus_interval(9, 8), 8)
        self.assertEqual(gradus_interval(15, 8), 10)

    def test_ratio_string_parser(self):
        self.assertEqual(gradus_ratio("2/1"), 2)
        self.assertEqual(gradus_ratio("3/2"), 4)
        self.assertEqual(gradus_ratio("4/3"), 5)
        self.assertEqual(gradus_ratio("5/4"), 7)
        self.assertEqual(gradus_ratio("9/8"), 8)
        self.assertEqual(gradus_ratio("15/8"), 10)
        self.assertEqual(gradus_ratio("1/1"), 1)

    def test_fraction_reduction_invariance(self):
        """Gradus must be invariant under unreduced fractions."""
        self.assertEqual(gradus_interval(4, 2), gradus_interval(2, 1))
        self.assertEqual(gradus_interval(6, 4), gradus_interval(3, 2))
        self.assertEqual(gradus_interval(8, 6), gradus_interval(4, 3))
        self.assertEqual(gradus_interval(18, 16), gradus_interval(9, 8))
        self.assertEqual(gradus_interval(30, 16), gradus_interval(15, 8))

    def test_sacred_tonecode_syllables(self):
        expected_gradus = {
            "sol": 1,
            "sol'": 2,
            "do": 4,
            "ra": 5,
            "mi": 7,
            "ke": 7,
            "fa": 8,
            "ath": 10,
        }
        for syl, expected in expected_gradus.items():
            actual = gradus_syllable(syl)
            self.assertEqual(actual, expected, f"Gradus mismatch for syllable '{syl}': expected {expected}, got {actual}")

    def test_consonance_hierarchy(self):
        """Test the strict ordering of consonance from tonic ground to high tension."""
        g_sol = gradus_syllable("sol")
        g_oct = gradus_syllable("sol'")
        g_do = gradus_syllable("do")
        g_ra = gradus_syllable("ra")
        g_mi = gradus_syllable("mi")
        g_fa = gradus_syllable("fa")
        g_ath = gradus_syllable("ath")

        self.assertLess(g_sol, g_oct)
        self.assertLess(g_oct, g_do)
        self.assertLess(g_do, g_ra)
        self.assertLess(g_ra, g_mi)
        self.assertLess(g_mi, g_fa)
        self.assertLess(g_fa, g_ath)

    def test_chord_gradus(self):
        """
        Euler's gradus for major triad (4:5:6):
        lcm(4, 5, 6) = 60 = 2^2 * 3 * 5
        Gamma(60) = 1 + 2*(1) + 2 + 4 = 9
        """
        major_triad = [(1, 1), (5, 4), (3, 2)]  # 4 : 5 : 6
        self.assertEqual(gradus_chord(major_triad), 9)

        # Tonic, fifth, octave chord (1 : 3/2 : 2) -> integer scale 2 : 3 : 4 -> lcm = 12 -> Gamma(12) = 5
        octave_fifth = [(1, 1), (3, 2), (2, 1)]
        self.assertEqual(gradus_chord(octave_fifth), 5)

        # Compound twelfth chord (1 : 2 : 3) -> lcm = 6 -> Gamma(6) = 4
        compound_twelfth = [(1, 1), (2, 1), (3, 1)]
        self.assertEqual(gradus_chord(compound_twelfth), 4)

    def test_error_handling(self):
        with self.assertRaises(ValueError):
            gradus_interval(-1, 2)
        with self.assertRaises(ValueError):
            gradus_interval(3, 0)
        with self.assertRaises(KeyError):
            gradus_syllable("nonexistent")


if __name__ == "__main__":
    unittest.main()
