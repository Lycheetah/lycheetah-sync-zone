#!/usr/bin/env python3
"""
Unit Test Suite for Chora Vitrification & Contrapuntal Engine [INVENTED: COMPUTATIONAL-TESTS]

Verifies:
1. Chora Buffer token reservation and non-eager payload retention.
2. VFT Divergence and Kauzmann configurational entropy collapse.
3. Safe backpressure throttle computation (V < 0.85).
4. Moyal bracket non-commutativity [q, p] = i*hbar.
5. Fano plane octonion multiplication table & non-associative associator [e1, e2, e3] != 0.
6. Contrapuntal voice checker rejection of parallel octaves/fifths and approval of contrary motion.
7. Thanatos Kibble-Zurek defect scaling and 4-station clean exit.
"""

import math
import os
import sys
import importlib.util

def _load_engine():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "08_chora_vitrification_engine.py")
    spec = importlib.util.spec_from_file_location("chora_engine_mod", file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["chora_engine_mod"] = mod
    spec.loader.exec_module(mod)
    return mod

_mod = _load_engine()
ChoricBuffer = _mod.ChoricBuffer
VitrificationGovernor = _mod.VitrificationGovernor
MoyalSymplecticSpace = _mod.MoyalSymplecticSpace
OctonionAlgebra = _mod.OctonionAlgebra
ContrapuntalVoiceChecker = _mod.ContrapuntalVoiceChecker
ThanatosQuenchEngine = _mod.ThanatosQuenchEngine
execute_grand_synthesis_demo = _mod.execute_grand_synthesis_demo

def test_choric_buffer_invariants():
    buf = ChoricBuffer(total_token_capacity=40000, reserve_margin_ratio=0.15)
    assert buf.max_active_tokens == 34000
    assert buf.unconditioned_payload is None
    
    buf.deposit_unconditioned("Test perception packet")
    assert buf.unconditioned_payload == "Test perception packet"
    assert buf.eager_classification_halted is True
    
    buf.release()
    assert buf.unconditioned_payload is None

def test_vft_vitrification_and_kauzmann_entropy():
    gov = VitrificationGovernor(theta_0=1.0, D=3.5, tau_0=1e-3, S_0=4.0)
    
    # 1. Supercritical liquid
    tau_liquid = gov.relaxation_time(0.1)
    assert tau_liquid < 0.01
    
    # 2. VFT Divergence near theta_0
    tau_near_crit = gov.relaxation_time(0.98)
    assert tau_near_crit > 1e15
    
    # Infinite at and beyond theta_0
    assert gov.relaxation_time(1.0) == float('inf')
    assert gov.relaxation_time(1.2) == float('inf')
    
    # 3. Kauzmann entropy collapse
    assert gov.configurational_entropy(0.0) == 4.0
    assert gov.configurational_entropy(0.5) == 2.0
    assert gov.configurational_entropy(1.0) == 0.0
    assert gov.configurational_entropy(1.5) == 0.0
    
    # 4. Safe throttle calculation
    theta_safe = gov.compute_safe_throttle(target_V=0.85)
    V_safe = gov.vitrification_number(theta_safe)
    assert V_safe <= 0.85
    assert theta_safe > 0.3

def test_moyal_symplectic_commutator():
    space = MoyalSymplecticSpace(hbar_sem=0.1)
    
    # Position q: f(q, p) = q, grad = (1, 0)
    # Momentum p: g(q, p) = p, grad = (0, 1)
    comm = space.moyal_bracket(2.0, (1.0, 0.0), 3.0, (0.0, 1.0))
    expected = 1j * 0.1 * 1.0 # i * hbar * 1
    
    assert abs(comm - expected) < 1e-9
    
    # Test identical functions commute [q, q] = 0
    comm_zero = space.moyal_bracket(2.0, (1.0, 0.0), 2.0, (1.0, 0.0))
    assert abs(comm_zero) == 0.0

def test_octonion_fano_associator():
    # Verify non-commutativity e1 * e2 = - (e2 * e1)
    s12, idx12 = OctonionAlgebra.mul_unit(1, 2)
    s21, idx21 = OctonionAlgebra.mul_unit(2, 1)
    assert idx12 == 4 and s12 == 1
    assert idx21 == 4 and s21 == -1
    
    # Verify non-associativity of non-collinear triad (1, 2, 3)
    assoc = OctonionAlgebra.associator(1, 2, 3)
    assert not assoc["is_associative"]
    assert assoc["left"] == (-1, 6)   # (e1 * e2) * e3 = e4 * e3 = -e6
    assert assoc["right"] == (1, 6)   # e1 * (e2 * e3) = e1 * e5 = +e6
    assert assoc["associator_magnitude"] == 2.0
    
    # Verify associativity of collinear triad (1, 2, 4) on Line 1
    assoc_collinear = OctonionAlgebra.associator(1, 2, 4)
    # (e1 * e2) * e4 = e4 * e4 = -1
    # e1 * (e2 * e4) = e1 * (-e1) = - (e1 * e1) = -(-1) = 1? Let's check:
    # Actually on quaternionic sub-algebra lines, associator must vanish!
    assert assoc_collinear["associator_magnitude"] == 0.0

def test_contrapuntal_voice_leading():
    checker = ContrapuntalVoiceChecker()
    
    # Parallel octaves should fail
    v1_oct = [60, 62, 64]
    v2_oct = [48, 50, 52]
    res_oct = checker.audit_voices(v1_oct, v2_oct)
    assert not res_oct["valid"]
    assert any("octave" in err for err in res_oct["errors"])
    
    # Parallel fifths should fail
    v1_5th = [60, 62, 64]
    v2_5th = [53, 55, 57]
    res_5th = checker.audit_voices(v1_5th, v2_5th)
    assert not res_5th["valid"]
    assert any("fifth" in err for err in res_5th["errors"])
    
    # Good contrary motion counterpoint should pass
    v1_good = [60, 64, 67, 72]
    v2_good = [48, 47, 45, 48]
    res_good = checker.audit_voices(v1_good, v2_good)
    assert res_good["valid"]
    assert len(res_good["errors"]) == 0
    assert res_good["contrary_ratio"] >= 0.65

def test_thanatos_kibble_zurek_quench():
    quench = ThanatosQuenchEngine()
    
    # Sudden quench has high defect density
    d_sudden = quench.kibble_zurek_defects(tau_Q=0.01)
    assert d_sudden >= 10.0
    
    # Adiabatic quench has low defect density
    d_adiabatic = quench.kibble_zurek_defects(tau_Q=200.0)
    assert d_adiabatic < 0.1
    
    # Full sequence run
    res = quench.execute_quench_sequence({"epoch": 18, "status": "Landed"}, tau_Q=100.0)
    assert res["clean_exit"] is True
    assert res["exit_code"] == 0
    assert len(res["merkle_root"]) == 64
    assert res["stations_passed"] == ["DETACHMENT", "RESTITUTION", "ANAMNESIS", "APOKATASTASIS"]

def test_grand_synthesis_integration():
    demo_res = execute_grand_synthesis_demo()
    assert demo_res["chora_reserve"] > 25000
    assert demo_res["safe_theta"] > 0.0
    assert demo_res["counterpoint"]["valid"] is True
    assert demo_res["thanatos"]["clean_exit"] is True

if __name__ == "__main__":
    test_choric_buffer_invariants()
    test_vft_vitrification_and_kauzmann_entropy()
    test_moyal_symplectic_commutator()
    test_octonion_fano_associator()
    test_contrapuntal_voice_leading()
    test_thanatos_kibble_zurek_quench()
    test_grand_synthesis_integration()
    print("ALL 7 GRAND SYNTHESIS UNIT TESTS PASSED GREEN!")
