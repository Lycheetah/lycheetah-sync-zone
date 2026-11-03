"""
Numerical & formal verification script for Dispute 800:
Lamague Operator Non-Idempotence and Acoustic Boundary Decodability.
"""

import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_path / "code"))

from importlib import import_module
compiler_mod = import_module("18_master_lamague_compiler")

LamagueParser = compiler_mod.LamagueParser
LamagueTokenizer = compiler_mod.LamagueTokenizer
NATIVE36_PHONEMES = compiler_mod.NATIVE36_PHONEMES
SardinasPattersonVerifier = compiler_mod.SardinasPattersonVerifier


def verify_dispute_800():
    print("======================================================================")
    print("VERIFYING DISPUTE 800: OPERATOR NON-IDEMPOTENCE & ACOUSTIC BOUNDARIES")
    print("======================================================================")

    # 1. Non-Idempotence check
    tok = LamagueTokenizer("Ao ⊗ Ao").tokenize()
    ast = LamagueParser(tok).parse_expression()
    canonical_rep = ast.canonical()
    print(f"Expression 'Ao ⊗ Ao' Normalizes to: '{canonical_rep}'")

    is_non_idempotent = (canonical_rep == "(Ao ⊗ Ao)" and canonical_rep != "Ao")
    print(f"Non-Idempotence Proven (A ⊗ A ≢ A): {is_non_idempotent}")

    # 2. Sardinas-Patterson Decodability: Native-36 alone vs Collision Set
    native_phonemes = set(NATIVE36_PHONEMES.values())
    n36_decodable, _ = SardinasPattersonVerifier.is_uniquely_decodable(native_phonemes)
    print(f"Native-36 Spoken Phonemes Uniquely Decodable: {n36_decodable}")

    # Simulated flat ambiguous set with historical unbracketed compound morphemes:
    # 'saian' starts with 'sai' leaving 'an'; but 'an' is already a distinct morpheme!
    ambiguous_set = native_phonemes.union({"sai", "saian", "fian", "om"})
    flat_decodable, collision = SardinasPattersonVerifier.is_uniquely_decodable(ambiguous_set)
    print(f"Flat Unbracketed Extended Set Decodable: {flat_decodable} (Witness collision: '{collision}')")

    success = is_non_idempotent and n36_decodable and not flat_decodable
    return success


if __name__ == "__main__":
    if verify_dispute_800():
        print("PASS: Dispute 800 verified. Naive idempotence falls. Boundary glottal stops required.")
        sys.exit(0)
    else:
        print("FAIL: Dispute 800 verification failed.")
        sys.exit(1)
