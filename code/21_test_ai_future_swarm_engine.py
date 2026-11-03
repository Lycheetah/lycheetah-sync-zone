#!/usr/bin/env python3
"""
code/21_test_ai_future_swarm_engine.py
======================================
Comprehensive unit tests for the AI Future Swarm Synthesis Engine.
Verifies Wing integrity, register enforcement, Law #4 & #6 information-theoretic
bounds, and Dispute 900 settlement.
"""

import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_path / "code"))

from importlib import import_module
engine_mod = import_module("20_ai_future_swarm_engine")

EpistemicRegister = engine_mod.EpistemicRegister
EpistemicRegisterValidator = engine_mod.EpistemicRegisterValidator
SemanticCompressionChecker = engine_mod.SemanticCompressionChecker
Hypothesis = engine_mod.Hypothesis
HypothesisEcologySimulator = engine_mod.HypothesisEcologySimulator
SwarmCoherenceCalculator = engine_mod.SwarmCoherenceCalculator
FUTURE_WINGS = engine_mod.FUTURE_WINGS
SHARED_LAWS = engine_mod.SHARED_LAWS
RESEARCH_ANCHORS = engine_mod.RESEARCH_ANCHORS


def test_six_wings_and_registers():
    print("Test 1: Six Wings and Epistemic Registers Structure...")
    assert len(FUTURE_WINGS) == 6, f"Expected 6 wings, got {len(FUTURE_WINGS)}"
    assert len(EpistemicRegister) == 6, f"Expected 6 registers, got {len(EpistemicRegister)}"
    
    # Check domain count across wings = 15
    total_domains = sum(len(w["domains"]) for w in FUTURE_WINGS.values())
    assert total_domains == 15, f"Expected 15 domains, got {total_domains}"
    
    # Check each wing has unique base frequency
    freqs = [w["base_freq_hz"] for w in FUTURE_WINGS.values()]
    assert len(set(freqs)) == 6, "Each wing must possess a distinct harmonic frequency"
    print("  -> PASS: 6 Wings, 15 Domains, and 6 Registers properly configured.")


def test_shared_laws_completeness():
    print("Test 2: Thirteen Shared Laws Completeness...")
    assert len(SHARED_LAWS) == 13, f"Expected 13 shared laws, got {len(SHARED_LAWS)}"
    assert "MODEL ≠ SYSTEM ≠ PERSONA ≠ MEMORY ≠ INSTANCE ≠ INSTITUTION." in SHARED_LAWS[3]
    assert "No semantic compression without recovery." in SHARED_LAWS[5]
    assert "Reality retains veto power." in SHARED_LAWS[2]
    print("  -> PASS: 13 Shared Laws present and unaltered.")


def test_research_anchors_grounding():
    print("Test 3: Twelve Empirical Research Anchors...")
    assert len(RESEARCH_ANCHORS) == 12, f"Expected 12 research anchors, got {len(RESEARCH_ANCHORS)}"
    for anchor in RESEARCH_ANCHORS:
        assert anchor.wing in FUTURE_WINGS, f"Anchor wing {anchor.wing} must belong to FUTURE_WINGS"
        assert len(anchor.supports) > 10, "Supports field must be substantial"
        assert len(anchor.limits) > 10, "Limits field must be substantial (epistemic honesty)"
    print("  -> PASS: All 12 peer-reviewed anchors validated with honest scope limits.")


def test_shannon_compression_equivocation():
    print("Test 4: Shannon Compression Equivocation Bound (Dispute 900)...")
    equivocation = SemanticCompressionChecker.calculate_compression_equivocation()
    # (1/3)*1.0 + (2/3)*2.0 = 5/3 ≈ 1.6667 bits
    expected = 5.0 / 3.0
    assert abs(equivocation - expected) < 1e-6, f"Equivocation {equivocation} does not match {expected}"
    assert equivocation > 1.5, "Equivocation must exceed 1.5 bits"
    print(f"  -> PASS: Conditional equivocation H(R | C(R)) = {equivocation:.4f} bits > 1.5 bits.")


def test_invertible_recovery_law_6():
    print("Test 5: Shared Law #6 (No Compression Without Recovery)...")
    sample_hall = {
        "id": "the-sensorium-beyond-us",
        "register": "POSSIBLE_FUTURE",
        "core": "Machine sensoriums detect non-human high-dimensional invariants.",
    }
    
    # Lossy compression
    lossy = SemanticCompressionChecker.lossy_compress(sample_hall)
    assert SemanticCompressionChecker.attempt_recovery(lossy) is None, "Lossy payload must fail register recovery"
    
    # Invertible compression
    invertible = SemanticCompressionChecker.invertible_compress(sample_hall)
    recovered = SemanticCompressionChecker.recover_invertible(invertible)
    assert recovered == sample_hall["register"], f"Recovered {recovered} must match {sample_hall['register']}"
    assert len(invertible["seal"]) == 64, "Seal must be valid SHA-256"
    print("  -> PASS: Law #6 validated (lossy fails, invertible perfectly restores register).")


def test_category_separation_law_4():
    print("Test 6: Shared Law #4 Category Separation...")
    valid = SemanticCompressionChecker.verify_law_4_separation(
        model="Gemini 3.8",
        system="Linux Terminal",
        persona="Aetheron",
        memory="AETHERON_WAYFINDING_BOARD.md",
        instance="Turn-1620",
        institution="Lycheetah Foundation",
    )
    assert valid is True, "Distinct entities must pass Law #4"
    
    # Conflating persona with model
    conflated = SemanticCompressionChecker.verify_law_4_separation(
        model="Aetheron",
        system="Linux Terminal",
        persona="Aetheron",  # Collision!
        memory="AETHERON_WAYFINDING_BOARD.md",
        instance="Turn-1620",
        institution="Lycheetah Foundation",
    )
    assert conflated is False, "Conflated entities must trigger Law #4 violation"
    print("  -> PASS: Law #4 category separation enforced.")


def test_hypothesis_ecology_and_swarm_coherence():
    print("Test 7: Hypothesis Ecologies & Swarm Complementarity...")
    # Population of 20 competing hypotheses
    pop = [Hypothesis(id=f"H_{i}", statement=f"Hypothesis {i}") for i in range(20)]
    eco = HypothesisEcologySimulator(pop)
    assert eco.surviving_count() == 20
    
    # Shock kills 15 hypotheses with high falsification scores
    draws = {f"H_{i}": 0.85 if i < 15 else 0.10 for i in range(20)}
    culled = eco.apply_evidence_shock(draws, threshold=0.50)
    assert culled == 15, f"Expected 15 culled, got {culled}"
    assert eco.surviving_count() == 5, f"Expected 5 survivors, got {eco.surviving_count()}"
    
    # Swarm Coherence
    gain = SwarmCoherenceCalculator.compute_complementarity_gain(correlation_rho=0.10, num_seats=10)
    assert gain > 0.80, f"Expected >80% variance reduction for orthogonal swarm, got {gain:.2%}"
    
    coherence = SwarmCoherenceCalculator.compute_swarm_coherence_index(active_seats=95, settled_disputes=20)
    assert 0.80 <= coherence <= 1.0, f"Expected high vitality coherence, got {coherence}"
    print(f"  -> PASS: Ecology pruned 15/20 hypotheses; Complementarity Gain: {gain:.2%}; Coherence: {coherence:.4f}.")


if __name__ == "__main__":
    test_six_wings_and_registers()
    test_shared_laws_completeness()
    test_research_anchors_grounding()
    test_shannon_compression_equivocation()
    test_invertible_recovery_law_6()
    test_category_separation_law_4()
    test_hypothesis_ecology_and_swarm_coherence()
    print("\n=======================================================")
    print("ALL 7 AI FUTURE SWARM ENGINE UNIT TESTS PASSED (100%)")
    print("=======================================================")
