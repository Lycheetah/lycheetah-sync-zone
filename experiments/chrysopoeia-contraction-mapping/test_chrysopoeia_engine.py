"""
Unit Tests for Chrysopoeia Contraction Mapping & Cascade Demotion Engine
========================================================================
Verifies Banach fixed-point contraction, non-commutative operator commutators,
monotonic 4-tier alchemical progression, Cascade 3-tier pyramid demotion,
AGM belief revision postulates, fixed-point idempotence, and non-equilibrium
entropy balance under Prigogine dissipative thermodynamics.
"""

import math
import unittest

from chrysopoeia_engine import Belief, ChrysopoeiaEngine


class TestChrysopoeiaEngine(unittest.TestCase):
    """
    Test suite for ChrysopoeiaEngine mathematical and epistemological invariants.
    """

    def setUp(self):
        self.engine = ChrysopoeiaEngine(psi_star=0.95, target_contraction=0.65)

    def test_banach_contraction_convergence(self):
        """
        1. Banach Contraction Convergence:
        Proves successive applications of Xi converge geometrically to fixed point psi*
        with d(psi_n, psi*) <= q^n * d(psi_0, psi*) and error < 1e-7 within 40 iterations.
        """
        psi = 0.15  # Starting deep in Nigredo
        psi_0 = psi
        initial_distance = self.engine.distance_to_fixed_point(psi_0)

        for step in range(40):
            prev_dist = self.engine.distance_to_fixed_point(psi)
            psi = self.engine.transform(psi)
            curr_dist = self.engine.distance_to_fixed_point(psi)

            # Contraction ratio check
            contraction_ratio = curr_dist / prev_dist
            self.assertLess(
                contraction_ratio,
                0.75,
                f"Contraction ratio {contraction_ratio} exceeds bound at step {step}"
            )

        final_distance = self.engine.distance_to_fixed_point(psi)
        self.assertLess(
            final_distance,
            1e-7,
            f"Final distance {final_distance} exceeds 1e-7 threshold"
        )
        # Expected geometric upper bound
        expected_upper_bound = (0.75 ** 40) * initial_distance
        self.assertLessEqual(final_distance, expected_upper_bound)

    def test_non_commutative_operator_order(self):
        """
        2. Non-Commutative Operator Order:
        Demonstrates that operators do not commute ([Calc, Diss] != 0, [Sep, Conj] != 0)
        and that reversing operator order changes the trajectory.
        """
        test_psi = 0.30

        # Commutator [Calc, Diss](psi)
        comm_calc_diss = self.engine.commutator("calc", "diss", test_psi)
        self.assertNotEqual(
            comm_calc_diss,
            0.0,
            "Commutator [Calc, Diss] must be non-zero"
        )
        self.assertGreater(
            abs(comm_calc_diss),
            1e-4,
            "Commutator [Calc, Diss] magnitude must be significant"
        )

        # Commutator [Sep, Conj](psi)
        comm_sep_conj = self.engine.commutator("sep", "conj", test_psi)
        self.assertNotEqual(
            comm_sep_conj,
            0.0,
            "Commutator [Sep, Conj] must be non-zero"
        )
        self.assertGreater(
            abs(comm_sep_conj),
            1e-4,
            "Commutator [Sep, Conj] magnitude must be significant"
        )

        # Composition disparity under reversal
        canonical_state = self.engine.transform(test_psi)
        reversed_state = self.engine.transform_reversed(test_psi)
        self.assertNotEqual(
            canonical_state,
            reversed_state,
            "Reversed operator composition must diverge from canonical order"
        )
        self.assertGreater(
            abs(canonical_state - reversed_state),
            1e-4,
            "Reversed sequence must produce non-trivial state divergence"
        )

    def test_four_tiers_monotonic_progression(self):
        """
        3. Four Tiers Monotonic Progression:
        Coherence and consonance increase monotonically across the 4 stages:
        Nigredo [0.0, 0.25) -> Albedo [0.25, 0.55) -> Citrinitas [0.55, 0.85) -> Rubedo [0.85, 1.0].
        """
        # Step through trajectory starting from Nigredo
        psi = 0.12
        tiers_visited = [ChrysopoeiaEngine.get_tier(psi)]
        coherences = [psi]
        consonances = [ChrysopoeiaEngine.consonance_metric(psi)]

        while ChrysopoeiaEngine.get_tier(psi) != "Rubedo":
            psi = self.engine.transform(psi)
            coherences.append(psi)
            consonances.append(ChrysopoeiaEngine.consonance_metric(psi))
            current_tier = ChrysopoeiaEngine.get_tier(psi)
            if current_tier != tiers_visited[-1]:
                tiers_visited.append(current_tier)

        # Verify all 4 tiers visited in exact order
        self.assertEqual(
            tiers_visited,
            ["Nigredo", "Albedo", "Citrinitas", "Rubedo"],
            f"Expected 4-stage tier progression, got {tiers_visited}"
        )

        # Verify strict monotonic increase in coherence and consonance
        for i in range(len(coherences) - 1):
            self.assertGreater(
                coherences[i + 1],
                coherences[i],
                f"Coherence must increase monotonically at step {i}"
            )
            self.assertGreater(
                consonances[i + 1],
                consonances[i],
                f"Consonance must increase monotonically at step {i}"
            )

    def test_cascade_pyramid_demotion(self):
        """
        4. Cascade Pyramid Demotion:
        Verifies that when truth pressure Pi > 1.2, contradictions are demoted
        (Theory -> Edge, Edge -> Quarantined) while Foundation invariants remain strictly untouched.
        """
        beliefs = [
            Belief(id="F1", tier="foundation", claim="Noether SO(2) Invariant", is_conflicted=True),
            Belief(id="F2", tier="foundation", claim="Zero-Dependency Rule", is_conflicted=False),
            Belief(id="T1", tier="theory", claim="Euler Gradus Tuning", is_conflicted=True),
            Belief(id="T2", tier="theory", claim="Biot-Savart Vorticity", is_conflicted=False),
            Belief(id="E1", tier="edge", claim="Ad-hoc 0.985 Damping Window", is_conflicted=True),
            Belief(id="E2", tier="edge", claim="Mobile WebGL Speculative Shader", is_conflicted=False),
        ]

        # Case A: Subcritical truth pressure (Pi = 1.0 <= 1.2) -> No demotions
        sub_beliefs = self.engine.demote_under_truth_pressure(beliefs, truth_pressure=1.0, threshold=1.2)
        for orig, sub in zip(beliefs, sub_beliefs):
            self.assertEqual(orig.tier, sub.tier)
            self.assertEqual(orig.status, sub.status)

        # Case B: Supercritical truth pressure (Pi = 1.6 > 1.2) -> Demotions execute
        dem_beliefs = self.engine.demote_under_truth_pressure(beliefs, truth_pressure=1.6, threshold=1.2)
        dem_dict = {b.id: b for b in dem_beliefs}

        # Foundation invariants MUST remain active and in foundation
        self.assertEqual(dem_dict["F1"].tier, "foundation")
        self.assertEqual(dem_dict["F1"].status, "active")
        self.assertEqual(dem_dict["F2"].tier, "foundation")
        self.assertEqual(dem_dict["F2"].status, "active")

        # Conflicted theory must be demoted to edge
        self.assertEqual(dem_dict["T1"].tier, "edge")
        self.assertEqual(dem_dict["T1"].status, "demoted")
        self.assertEqual(dem_dict["T1"].confidence, 0.5)

        # Unconflicted theory remains in theory
        self.assertEqual(dem_dict["T2"].tier, "theory")
        self.assertEqual(dem_dict["T2"].status, "active")

        # Conflicted edge must be quarantined
        self.assertEqual(dem_dict["E1"].tier, "edge")
        self.assertEqual(dem_dict["E1"].status, "quarantined")
        self.assertEqual(dem_dict["E1"].confidence, 0.0)

        # Unconflicted edge remains active
        self.assertEqual(dem_dict["E2"].tier, "edge")
        self.assertEqual(dem_dict["E2"].status, "active")

    def test_agm_postulates_satisfied(self):
        """
        5. AGM Postulates Satisfied:
        Validates AGM belief revision postulates (Closure, Inclusion, Vacuity, Consistency, Success).
        """
        beliefs = [
            Belief(id="F1", tier="foundation", claim="CHARTER §1 Sovereign Fire", is_conflicted=False),
            Belief(id="T1", tier="theory", claim="Linear Damping Model", is_conflicted=True),
            Belief(id="E1", tier="edge", claim="Heuristic Constant Guess", is_conflicted=True),
        ]

        # Subcritical validation (Vacuity check)
        dem_sub = self.engine.demote_under_truth_pressure(beliefs, truth_pressure=0.9, threshold=1.2)
        agm_sub = ChrysopoeiaEngine.validate_agm_postulates(beliefs, dem_sub, truth_pressure=0.9, threshold=1.2)
        self.assertTrue(agm_sub["all_satisfied"], f"AGM subcritical postulates failed: {agm_sub}")
        self.assertTrue(agm_sub["vacuity"])

        # Supercritical validation (Success & Inclusion check)
        dem_super = self.engine.demote_under_truth_pressure(beliefs, truth_pressure=1.5, threshold=1.2)
        agm_super = ChrysopoeiaEngine.validate_agm_postulates(beliefs, dem_super, truth_pressure=1.5, threshold=1.2)
        self.assertTrue(agm_super["all_satisfied"], f"AGM supercritical postulates failed: {agm_super}")
        self.assertTrue(agm_super["closure"])
        self.assertTrue(agm_super["inclusion"])
        self.assertTrue(agm_super["consistency"])
        self.assertTrue(agm_super["success"])

    def test_fixed_point_idempotence(self):
        """
        6. Fixed Point Idempotence:
        Xi(psi*) = psi* to machine precision (< 1e-14), and Xi(Xi(psi*)) = psi*.
        """
        psi_star = self.engine.psi_star
        transformed = self.engine.transform(psi_star)
        error = abs(transformed - psi_star)
        self.assertLess(
            error,
            1e-14,
            f"Fixed point mapping error {error} exceeds machine precision 1e-14"
        )

        double_transformed = self.engine.transform(transformed)
        self.assertLess(
            abs(double_transformed - psi_star),
            1e-14,
            "Double transformed fixed point must be idempotent within 1e-14"
        )

    def test_entropy_balance_dissipation(self):
        """
        7. Entropy Balance & Dissipation:
        Internal entropy drop d_i S < 0 is offset by positive environmental dissipation
        d_e S > 0 such that dS_total = d_i S + d_e S >= 0 (Prigogine 2nd Law).
        """
        psi_initial = 0.20
        psi_final = self.engine.transform(psi_initial)  # ascends to ~0.50

        self.assertGreater(psi_final, psi_initial, "Coherence must increase under transformation")

        balance = ChrysopoeiaEngine.entropy_balance(psi_initial, psi_final)
        d_i_s = balance["d_i_s"]
        d_e_s = balance["d_e_s"]
        d_total = balance["d_total_s"]

        # 1. Internal entropy decreases as coherence increases
        self.assertLess(
            d_i_s,
            0.0,
            f"Internal entropy change must be negative (negentropy), got {d_i_s}"
        )

        # 2. Environmental dissipation is strictly positive
        self.assertGreater(
            d_e_s,
            0.0,
            f"Environmental dissipation must be positive, got {d_e_s}"
        )

        # 3. Total universe entropy is non-decreasing (Second Law)
        self.assertGreaterEqual(
            d_total,
            0.0,
            f"Total entropy change must be non-negative, got {d_total}"
        )
        self.assertEqual(balance["second_law_satisfied"], 1.0)


if __name__ == "__main__":
    unittest.main()
