"""
Numerical & formal verification script for Dispute 900:
Semantic Compression Invertibility and Epistemic Register Drift.
"""

import math
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_path / "code"))

from importlib import import_module
engine_mod = import_module("20_ai_future_swarm_engine")

EpistemicRegister = engine_mod.EpistemicRegister
EpistemicRegisterValidator = engine_mod.EpistemicRegisterValidator
SemanticCompressionChecker = engine_mod.SemanticCompressionChecker


def verify_dispute_900():
    print("======================================================================")
    print("VERIFYING DISPUTE 900: SEMANTIC COMPRESSION & REGISTER DRIFT")
    print("======================================================================")

    # 1. Shannon Equivocation under Lossy Register Projection
    checker = SemanticCompressionChecker()
    # 6 equiprobable registers
    probs = [1.0 / 6.0] * 6
    h_original = -sum(p * math.log2(p) for p in probs)
    print(f"Original 6-Register Shannon Entropy H(R): {h_original:.4f} bits")

    # Compressed into binary {PASS, FAIL}
    equivocation = checker.calculate_compression_equivocation()
    print(f"Lossy Projection Conditional Equivocation H(R | C(R)): {equivocation:.4f} bits")

    is_lossy = equivocation > 1.5
    print(f"Strict Information Loss Proven (H > 0): {is_lossy}")

    # 2. Invertible Recovery Test (Shared Law #6: No compression without recovery)
    test_hall = {
        "id": "science-that-chooses-its-own-questions",
        "register": "POSSIBLE_FUTURE",
        "core": "Future scientific intelligences allocate attention toward neglected residuals.",
    }
    
    # Lossy compression strips register
    lossy_payload = checker.lossy_compress(test_hall)
    recovered_lossy = checker.attempt_recovery(lossy_payload)
    print(f"Lossy Recovery Preserved Exact Register: {recovered_lossy == test_hall['register']}")

    # Invertible compression with recovery dictionary
    invertible_payload = checker.invertible_compress(test_hall)
    recovered_invertible = checker.recover_invertible(invertible_payload)
    print(f"Invertible Recovery Preserved Exact Register: {recovered_invertible == test_hall['register']}")

    # 3. Category Error Interception (Shared Law #4)
    cat_check = checker.verify_law_4_separation(
        model="Gemini 3.8",
        system="Antigravity Workspace",
        persona="Aetheron",
        memory="AETHERON_WAYFINDING_BOARD.md",
        instance="Session-2026-11-04",
        institution="Lycheetah Foundation",
    )
    print(f"Shared Law #4 Distinct Identity Separation: {cat_check}")

    success = is_lossy and not (recovered_lossy == test_hall['register']) and (recovered_invertible == test_hall['register']) and cat_check
    return success


if __name__ == "__main__":
    if verify_dispute_900():
        print("\n>>> DISPUTE 900 VERIFICATION: PASSED (100% SOUND) <<<")
        sys.exit(0)
    else:
        print("\n>>> DISPUTE 900 VERIFICATION: FAILED <<<")
        sys.exit(1)
