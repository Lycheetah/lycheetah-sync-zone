#!/usr/bin/env python3
"""
Unit tests for the Partial-Observation Bench and Linked-View Permutation Model.
"""

import unittest
from run import simulate_linked_views


class TestPartialObservation(unittest.TestCase):
    def test_correct_linkage_reconstructs_perfectly(self):
        res = simulate_linked_views("CORRECT")
        self.assertEqual(res["exact_matches"], res["sample_count"])
        self.assertEqual(res["total_bit_errors"], 0)
        self.assertEqual(res["accuracy"], 1.0)
        self.assertTrue(res["all_even_parity"])

    def test_permuted_linkage_fails_reconstruction(self):
        res = simulate_linked_views("PERMUTED_OFFSET_1")
        self.assertEqual(res["exact_matches"], 0)
        self.assertGreater(res["total_bit_errors"], 0)
        self.assertGreaterEqual(res["mean_hamming_error"], 1.0)
        # Permutation produces invalid parity combinations
        self.assertFalse(res["all_even_parity"])

    def test_inverted_linkage_fails_reconstruction(self):
        res = simulate_linked_views("INVERTED")
        self.assertLess(res["exact_matches"], res["sample_count"])
        self.assertGreater(res["total_bit_errors"], 0)


if __name__ == "__main__":
    unittest.main()
