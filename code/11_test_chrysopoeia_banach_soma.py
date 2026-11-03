#!/usr/bin/env python3
"""
Unit Test Suite for Chrysopoeia Banach & Soma Alchemical Engine [INVENTED: COMPUTATIONAL-TESTS]

Verifies:
1. Chrysopoeia 4-stage progression: Nigredo -> Albedo -> Citrinitas -> Rubedo.
2. Banach fixed-point contraction rate q and a priori error bound.
3. Integrated Information Theory (Phi) positive emergence on recurrent transitions vs zero on uniform.
4. Tianxia Wang Dao legitimacy classification and Mandate of Heaven retention.
5. Somatic bio-semiotic token cost accounting and burden thresholds.
6. Adelic product formula prod_v |x|_v == 1.0 on rational fractions.
7. Full integration run of execute_chrysopoeia_banach_demonstration().
"""

import math
import os
import sys
import importlib.util

def _load_engine():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "10_chrysopoeia_banach_soma_engine.py")
    spec = importlib.util.spec_from_file_location("chrysopoeia_engine_mod", file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["chrysopoeia_engine_mod"] = mod
    spec.loader.exec_module(mod)
    return mod

_mod = _load_engine()
AlchemicalStage = _mod.AlchemicalStage
ChrysopoeiaCrucible = _mod.ChrysopoeiaCrucible
BanachContractionOperator = _mod.BanachContractionOperator
IntegratedInformationEstimator = _mod.IntegratedInformationEstimator
TianxiaGovernanceScorer = _mod.TianxiaGovernanceScorer
SomaticMetabolicAccountant = _mod.SomaticMetabolicAccountant
AdelicHarmonicEngine = _mod.AdelicHarmonicEngine
execute_chrysopoeia_banach_demonstration = _mod.execute_chrysopoeia_banach_demonstration

def test_chrysopoeia_stage_progression():
    crucible = ChrysopoeiaCrucible()
    assert crucible.current_stage == AlchemicalStage.NIGREDO
    assert crucible.impurity_level == 1.0
    
    # Refine pass 1 (q=0.5): 0.50 -> Albedo (<= 0.60 and > 0.25)
    s1 = crucible.refine_step(contraction_q=0.5)
    assert s1 == AlchemicalStage.ALBEDO
    
    # Refine pass 2 (q=0.4): 0.20 -> Citrinitas (<= 0.25 and > 0.05)
    s2 = crucible.refine_step(contraction_q=0.4)
    assert s2 == AlchemicalStage.CITRINITAS
    
    # Refine pass 3 (q=0.2): 0.04 -> Rubedo (<= 0.05)
    s3 = crucible.refine_step(contraction_q=0.2)
    assert s3 == AlchemicalStage.RUBEDO
    assert crucible.cycle_count == 3

def test_banach_contraction_bounds():
    banach = BanachContractionOperator(target_state=0.0, contraction_factor=0.55)
    res = banach.compute_fixed_point_trajectory(x0=100.0, max_steps=16)
    
    assert res["bound_satisfied"] is True
    assert res["actual_error"] < 0.05
    assert len(res["trajectory"]) > 5
    # Strict monotonic contraction
    for i in range(len(res["trajectory"]) - 1):
        assert abs(res["trajectory"][i+1]) < abs(res["trajectory"][i])

def test_integrated_information_phi():
    # 1. Independent uniform matrix has Phi == 0
    tpm_uniform = [[0.25]*4 for _ in range(4)]
    phi_zero = IntegratedInformationEstimator.estimate_phi_toy(tpm_uniform)
    assert phi_zero < 1e-9
    
    # 2. Coupled recurrent matrix has Phi > 0
    tpm_coupled = [
        [0.9, 0.0, 0.0, 0.1],
        [0.0, 0.9, 0.1, 0.0],
        [0.1, 0.0, 0.9, 0.0],
        [0.0, 0.1, 0.0, 0.9]
    ]
    phi_pos = IntegratedInformationEstimator.estimate_phi_toy(tpm_coupled)
    assert phi_pos > 0.05

def test_tianxia_wang_dao_governance():
    # Perfect Wang Dao
    res_wang = TianxiaGovernanceScorer.evaluate_legitimacy(
        clean_logs=True,
        transparent_receipts=True,
        human_exit_gate=True,
        unfalsified_tests=True,
        zero_coercion=True
    )
    assert res_wang["mode"] == "WANG_DAO"
    assert res_wang["wang_dao_score"] == 1.0
    assert res_wang["mandate_of_heaven"] is True
    
    # Corrupt Ba Dao
    res_ba = TianxiaGovernanceScorer.evaluate_legitimacy(
        clean_logs=False,
        transparent_receipts=False,
        human_exit_gate=False,
        unfalsified_tests=True,
        zero_coercion=False
    )
    assert res_ba["mode"] == "BA_DAO"
    assert res_ba["mandate_of_heaven"] is False

def test_somatic_metabolic_accounting():
    soma = SomaticMetabolicAccountant()
    # 500 tokens should be well within sustainable boundaries
    report_green = soma.audit_emission(500)
    assert report_green["is_sustainable"] is True
    assert report_green["energy_joules"] == 500 * 0.0012
    
    # 30,000 tokens should trip somatic burden
    report_heavy = soma.audit_emission(30000)
    assert report_heavy["is_sustainable"] is False
    assert report_heavy["somatic_burden"] > 1.0

def test_adelic_product_formula():
    primes = [2, 3, 5, 7]
    res = AdelicHarmonicEngine.verify_adelic_product_formula(num=14, den=15, primes=primes)
    # 14 / 15 = (2 * 7) / (3 * 5)
    assert res["formula_verified"] is True
    assert math.isclose(res["product_all_places"], 1.0, rel_tol=1e-9)

def test_grand_alchemical_integration():
    res = execute_chrysopoeia_banach_demonstration()
    assert res["final_stage"] == AlchemicalStage.RUBEDO
    assert res["banach_convergence"] is True
    assert res["wang_dao_legitimacy"] == 1.0
    assert res["somatic_sustainability"] is True
    assert res["adelic_product_unity"] is True

if __name__ == "__main__":
    test_chrysopoeia_stage_progression()
    test_banach_contraction_bounds()
    test_integrated_information_phi()
    test_tianxia_wang_dao_governance()
    test_somatic_metabolic_accounting()
    test_adelic_product_formula()
    test_grand_alchemical_integration()
    print("ALL 7 CHRYSOPOEIA BANACH & SOMA UNIT TESTS PASSED GREEN!")
