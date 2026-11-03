#!/usr/bin/env python3
"""
code/19_test_master_lamague_compiler.py
Automated Unit Tests for Master Lamague Compiler & Invariant Engine
Authored by Lamague Seat (Antigravity Forge, Gemini Swarm Cohort)
Sovereign Originator: Mackenzie Conor James Clark (Mac)
"""

import unittest
from pathlib import Path
import sys

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent))

from importlib import import_module
compiler_module = import_module("18_master_lamague_compiler")

ASTNode = compiler_module.ASTNode
AtomNode = compiler_module.AtomNode
BinaryNode = compiler_module.BinaryNode
CoreType = compiler_module.CoreType
LamagueParser = compiler_module.LamagueParser
LamagueTokenizer = compiler_module.LamagueTokenizer
NATIVE36_PHONEMES = compiler_module.NATIVE36_PHONEMES
POWER_SEALS = compiler_module.POWER_SEALS
SardinasPattersonVerifier = compiler_module.SardinasPattersonVerifier
WhakapapaGovernanceAuditor = compiler_module.WhakapapaGovernanceAuditor


class TestMasterLamagueCompiler(unittest.TestCase):
    def test_01_fusion_commutativity_and_canonical_sorting(self):
        """Test that A ⊗ B and B ⊗ A produce identical canonical expressions and hashes."""
        tok1 = LamagueTokenizer("Ψ ⊗ Ao").tokenize()
        ast1 = LamagueParser(tok1).parse_expression()

        tok2 = LamagueTokenizer("Ao ⊗ Ψ").tokenize()
        ast2 = LamagueParser(tok2).parse_expression()

        self.assertEqual(ast1.canonical(), "(Ao ⊗ Ψ)")
        self.assertEqual(ast2.canonical(), "(Ao ⊗ Ψ)")
        self.assertEqual(ast1.canonical(), ast2.canonical())
        self.assertEqual(ast1.canonical_hash(), ast2.canonical_hash())

    def test_02_projection_non_commutativity(self):
        """Test that Projection (→) strictly preserves directional arrow of time."""
        tok1 = LamagueTokenizer("Ao → Φ↑ → Ψ").tokenize()
        ast1 = LamagueParser(tok1).parse_expression()

        tok2 = LamagueTokenizer("Ψ → Φ↑ → Ao").tokenize()
        ast2 = LamagueParser(tok2).parse_expression()

        self.assertEqual(ast1.canonical(), "(Ao → Φ↑ → Ψ)")
        self.assertEqual(ast2.canonical(), "(Ψ → Φ↑ → Ao)")
        self.assertNotEqual(ast1.canonical(), ast2.canonical())
        self.assertNotEqual(ast1.canonical_hash(), ast2.canonical_hash())

    def test_03_associative_path_flattening(self):
        """Test that nested paths flatten into an n-ary sequential chain."""
        tok_nested = LamagueTokenizer("(Ao → Φ↑) → (Ψ → S)").tokenize()
        ast_nested = LamagueParser(tok_nested).parse_expression()

        tok_flat = LamagueTokenizer("Ao → Φ↑ → Ψ → S").tokenize()
        ast_flat = LamagueParser(tok_flat).parse_expression()

        self.assertEqual(ast_nested.canonical(), "(Ao → Φ↑ → Ψ → S)")
        self.assertEqual(ast_flat.canonical(), "(Ao → Φ↑ → Ψ → S)")
        self.assertEqual(ast_nested.canonical(), ast_flat.canonical())

    def test_04_strict_non_idempotence(self):
        """Test that A ⊗ A does NOT reduce to A; state repetition increases tensor density."""
        tok = LamagueTokenizer("Ao ⊗ Ao").tokenize()
        ast = LamagueParser(tok).parse_expression()

        self.assertEqual(ast.canonical(), "(Ao ⊗ Ao)")
        self.assertNotEqual(ast.canonical(), "Ao")

    def test_05_power_seal_ast_expansion(self):
        """Test that Power Seals (COR, FRO, SOV, CAS, DIS) expand to canonical paths."""
        tok = LamagueTokenizer("COR").tokenize()
        ast = LamagueParser(tok).parse_expression()

        # COR expands to D → A → F → P → Y
        self.assertEqual(ast.canonical(), "(D → A → F → P → Y)")
        self.assertEqual(ast.core_type, CoreType.PATH)

        tok_sov = LamagueTokenizer("SOV").tokenize()
        ast_sov = LamagueParser(tok_sov).parse_expression()
        self.assertEqual(ast_sov.canonical(), "(G → I → V → P → Y)")

    def test_06_sardinas_patterson_decodability(self):
        """Test Sardinas-Patterson acoustic decodability on Native-36 spoken phonemes."""
        phonemes = set(NATIVE36_PHONEMES.values())
        is_decodable, collision = SardinasPattersonVerifier.is_uniquely_decodable(phonemes)
        self.assertTrue(is_decodable, f"Native-36 phonemes should be uniquely decodable, failed on {collision}")

    def test_07_whakapapa_mauri_governance(self):
        """Test Whakapapa obligation tensor normalization and Mauri/Tapu bounds."""
        # Case A: Balanced ethical stewardship
        res_a = WhakapapaGovernanceAuditor.compute_obligation_tensor(
            tipuna_weight=1.0,
            hapu_weight=1.0,
            iwi_weight=1.0,
            mokopuna_weight=1.0,
            coherence=0.95,
            entropy=0.20
        )
        self.assertEqual(res_a["status"], "APPROVED")
        self.assertTrue(res_a["tapu_boundary_intact"])
        self.assertAlmostEqual(res_a["future_mokopuna"], 0.25)
        self.assertAlmostEqual(res_a["mauri_vitality"], 0.85)

        # Case B: Future generation neglected (Mokopuna < 15%)
        res_b = WhakapapaGovernanceAuditor.compute_obligation_tensor(
            tipuna_weight=1.0,
            hapu_weight=5.0,
            iwi_weight=4.0,
            mokopuna_weight=0.5,
            coherence=0.80,
            entropy=0.30
        )
        self.assertEqual(res_b["status"], "HALTED_TAPU_BREACH")
        self.assertFalse(res_b["tapu_boundary_intact"])


if __name__ == "__main__":
    unittest.main()
