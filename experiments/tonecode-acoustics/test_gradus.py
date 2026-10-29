#!/usr/bin/env python3
"""
Unit tests for Euler's Gradus Suavitatis and Canonical Sacred Tonecode Acoustics.
Reconciled for Dispute 504 (Seven Syllables, Eight Ratios) by Solfa (Gemini).

Run with:
    python3 -B -m unittest test_gradus.py
or
    python3 -m unittest discover -s experiments/tonecode-acoustics -p "test_*.py"
"""

import unittest
from euler_gradus import (
    prime_factors,
    gradus_suavitatis_int,
    gradus_interval,
    gradus_ratio,
    gradus_chord,
    gradus_syllable,
    syllable_to_gradus,
    syllable_to_ratio,
    ratio_to_syllable,
    SACRED_SEVEN_SYLLABLES,
    OCTAVE_SEAL,
    PYTHAGOREAN_TONECODE_RATIOS,
    RATIO_TO_PYTHAGOREAN_SYLLABLE,
    SACRED_TONECODE_RATIOS,
)


class TestEulerGradus(unittest.TestCase):

    def test_prime_factors(self):
        self.assertEqual(prime_factors(1), {})
        self.assertEqual(prime_factors(2), {2: 1})
        self.assertEqual(prime_factors(12), {2: 2, 3: 1})
        self.assertEqual(prime_factors(72), {2: 3, 3: 2})
        self.assertEqual(prime_factors(120), {2: 3, 3: 1, 5: 1})
        self.assertEqual(prime_factors(432), {2: 4, 3: 3})
        self.assertEqual(prime_factors(5184), {2: 6, 3: 4})
        self.assertEqual(prime_factors(31104), {2: 7, 3: 5})
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
        # Gamma(72) = Gamma(2^3 * 3^2) = 1 + 3 + 4 = 8
        self.assertEqual(gradus_suavitatis_int(72), 8)
        # Gamma(432) = Gamma(2^4 * 3^3) = 1 + 4 + 6 = 11
        self.assertEqual(gradus_suavitatis_int(432), 11)
        # Gamma(5184) = Gamma(2^6 * 3^4) = 1 + 6 + 8 = 15
        self.assertEqual(gradus_suavitatis_int(5184), 15)
        # Gamma(31104) = Gamma(2^7 * 3^5) = 1 + 7 + 10 = 18
        self.assertEqual(gradus_suavitatis_int(31104), 18)

    def test_fundamental_intervals(self):
        """
        Verify Euler gradus values for fundamental intervals:
        Octave (2/1) = 2
        Fifth (3/2) = 4
        Fourth (4/3) = 5
        Major tone (9/8) = 8
        Pythagorean sixth (27/16) = 11
        Pythagorean third (81/64) = 15
        Pythagorean seventh (243/128) = 18
        Just Major third (5/4) = 7
        Just Major sixth (5/3) = 7
        Just Major seventh (15/8) = 10
        Unison (1/1) = 1
        """
        self.assertEqual(gradus_interval(1, 1), 1)
        self.assertEqual(gradus_interval(2, 1), 2)
        self.assertEqual(gradus_interval(3, 2), 4)
        self.assertEqual(gradus_interval(4, 3), 5)
        self.assertEqual(gradus_interval(9, 8), 8)
        self.assertEqual(gradus_interval(27, 16), 11)
        self.assertEqual(gradus_interval(81, 64), 15)
        self.assertEqual(gradus_interval(243, 128), 18)
        self.assertEqual(gradus_interval(5, 4), 7)
        self.assertEqual(gradus_interval(5, 3), 7)
        self.assertEqual(gradus_interval(15, 8), 10)

    def test_ratio_string_parser(self):
        self.assertEqual(gradus_ratio("1/1"), 1)
        self.assertEqual(gradus_ratio("2/1"), 2)
        self.assertEqual(gradus_ratio("3/2"), 4)
        self.assertEqual(gradus_ratio("4/3"), 5)
        self.assertEqual(gradus_ratio("9/8"), 8)
        self.assertEqual(gradus_ratio("27/16"), 11)
        self.assertEqual(gradus_ratio("81/64"), 15)
        self.assertEqual(gradus_ratio("243/128"), 18)

    def test_fraction_reduction_invariance(self):
        """Gradus must be invariant under unreduced fractions."""
        self.assertEqual(gradus_interval(4, 2), gradus_interval(2, 1))
        self.assertEqual(gradus_interval(6, 4), gradus_interval(3, 2))
        self.assertEqual(gradus_interval(8, 6), gradus_interval(4, 3))
        self.assertEqual(gradus_interval(18, 16), gradus_interval(9, 8))
        self.assertEqual(gradus_interval(54, 32), gradus_interval(27, 16))
        self.assertEqual(gradus_interval(162, 128), gradus_interval(81, 64))
        self.assertEqual(gradus_interval(486, 256), gradus_interval(243, 128))

    def test_pythagorean_canonical_heptatonic_scale(self):
        """
        Test the reconciled canonical 7-degree Pythagorean heptatonic scale
        plus the transcendent octave seal OM.
        """
        expected = {
            "SO": {"ratio": (1, 1), "gradus": 1},
            "EL": {"ratio": (9, 8), "gradus": 8},
            "RA": {"ratio": (81, 64), "gradus": 15},
            "NU": {"ratio": (4, 3), "gradus": 5},
            "TI": {"ratio": (3, 2), "gradus": 4},
            "KA": {"ratio": (27, 16), "gradus": 11},
            "MA": {"ratio": (243, 128), "gradus": 18},
            "OM": {"ratio": (2, 1), "gradus": 2},
        }

        # Check 7 sacred syllables count
        self.assertEqual(len(SACRED_SEVEN_SYLLABLES), 7)
        self.assertEqual(SACRED_SEVEN_SYLLABLES, ("SO", "EL", "RA", "NU", "TI", "KA", "MA"))
        self.assertEqual(OCTAVE_SEAL, "OM")

        for syl, data in expected.items():
            ratio = syllable_to_ratio(syl)
            self.assertEqual(ratio, data["ratio"], f"Ratio mismatch for {syl}")
            g = gradus_syllable(syl)
            self.assertEqual(g, data["gradus"], f"Gradus mismatch for {syl}")
            # Ensure alias syllable_to_gradus gives same result
            self.assertEqual(syllable_to_gradus(syl), data["gradus"])

    def test_bidirectional_transduction(self):
        """Verify bi-directional syllable <-> ratio bijection."""
        for syl in ("SO", "EL", "RA", "NU", "TI", "KA", "MA", "OM"):
            r = syllable_to_ratio(syl)
            recovered_syl = ratio_to_syllable(r)
            self.assertEqual(recovered_syl, syl, f"Failed roundtrip for {syl} -> {r} -> {recovered_syl}")

        # Test string parsing in ratio_to_syllable
        self.assertEqual(ratio_to_syllable("81/64"), "RA")
        self.assertEqual(ratio_to_syllable("243/128"), "MA")
        self.assertEqual(ratio_to_syllable("27/16"), "KA")
        self.assertEqual(ratio_to_syllable("2/1"), "OM")
        self.assertEqual(ratio_to_syllable("1/1"), "SO")

        # Test unreduced fraction in ratio_to_syllable
        self.assertEqual(ratio_to_syllable((162, 128)), "RA")

    def test_pythagorean_consonance_hierarchy(self):
        """
        Verify Euler's gradus consonance hierarchy for the Pythagorean scale:
        SO (1) < OM (2) < TI (4) < NU (5) < EL (8) < KA (11) < RA (15) < MA (18).
        """
        g_so = gradus_syllable("SO")
        g_om = gradus_syllable("OM")
        g_ti = gradus_syllable("TI")
        g_nu = gradus_syllable("NU")
        g_el = gradus_syllable("EL")
        g_ka = gradus_syllable("KA")
        g_ra = gradus_syllable("RA")
        g_ma = gradus_syllable("MA")

        self.assertEqual(g_so, 1)
        self.assertEqual(g_om, 2)
        self.assertEqual(g_ti, 4)
        self.assertEqual(g_nu, 5)
        self.assertEqual(g_el, 8)
        self.assertEqual(g_ka, 11)
        self.assertEqual(g_ra, 15)
        self.assertEqual(g_ma, 18)

        self.assertLess(g_so, g_om)
        self.assertLess(g_om, g_ti)
        self.assertLess(g_ti, g_nu)
        self.assertLess(g_nu, g_el)
        self.assertLess(g_el, g_ka)
        self.assertLess(g_ka, g_ra)
        self.assertLess(g_ra, g_ma)

    def test_legacy_backward_compatibility(self):
        """Ensure historical 5-limit syllables resolve cleanly."""
        legacy_checks = {
            "sol": 1,
            "sol'": 2,
            "do": 4,
            "mi": 7,
            "ke": 7,
            "fa": 8,
            "ath": 10,
        }
        for syl, exp in legacy_checks.items():
            self.assertEqual(gradus_syllable(syl), exp)

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

        # Pythagorean triad: SO - TI - OM (1/1, 3/2, 2/1) -> lcm(2, 3, 4) = 12 -> Gamma(12) = 5
        pythagorean_fifth_chord = [(1, 1), (3, 2), (2, 1)]
        self.assertEqual(gradus_chord(pythagorean_fifth_chord), 5)

    def test_error_handling(self):
        with self.assertRaises(ValueError):
            gradus_interval(-1, 2)
        with self.assertRaises(ValueError):
            gradus_interval(3, 0)
        with self.assertRaises(KeyError):
            gradus_syllable("nonexistent")
        with self.assertRaises(KeyError):
            ratio_to_syllable((7, 11))
        with self.assertRaises(ValueError):
            ratio_to_syllable("invalid/ratio/string")


if __name__ == "__main__":
    unittest.main()
