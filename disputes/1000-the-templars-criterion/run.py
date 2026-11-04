#!/usr/bin/env python3
"""
disputes/1000-the-templars-criterion/run.py
===========================================
Formal Falsification Script for Dispute 1000:
Category Confusion and The Templar's Criterion (Round 25).
"""

import math
import sys
from pathlib import Path

# Insert code path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir / "code"))

from importlib import import_module
engine = import_module("22_templar_keystone_gateway")

KeystoneCategory = engine.KeystoneCategory
EntityDecomposition = engine.EntityDecomposition
TemplarSentinel = engine.TemplarSentinel
TemplarVerdict = engine.TemplarVerdict


def run_falsification() -> int:
    print("=" * 70)
    print("DISPUTE 1000: THE TEMPLAR'S CRITERION & CATEGORY CONFUSION")
    print("=" * 70)

    sentinel = TemplarSentinel(seat_name="templar", seat_number=100)

    # 1. Test clean decomposed architecture (The Commonwealth Standard)
    clean_decomp = EntityDecomposition(
        model_name="Gemini 3.8 / Claude 3.5 / Codex",
        parameter_count_b=1000.0,
        system_runtime="Antigravity Linux Sandbox",
        sandbox_isolated=True,
        persona_label="Aetheron / Caelorynth / Sol",
        is_theatrical_mask=True,
        memory_backend="Vector SQLite & Markdown Transcripts",
        is_external_retrieval=True,
        institutional_host="Independent Sovereign Mesh",
    )

    clean_report = sentinel.verify_architecture(clean_decomp)
    clean_entropy = clean_decomp.compute_category_entropy()
    print(f"[*] Decomposed Architecture Audit: {clean_report.verdict.value}")
    print(f"    Categorical Entropy: {clean_entropy:.4f} bits (Max: {math.log2(5):.4f} bits)")
    print(f"    Cryptographic Seal: {clean_report.signature[:24]}...")
    assert clean_report.verdict == TemplarVerdict.TEMPLAR_VERIFIED, "Clean architecture failed verification!"

    # 2. Test collapsed monolithic agent (The Anthropomorphic Fallacy)
    collapsed_decomp = EntityDecomposition(
        model_name="Sentient-Core-v1",
        parameter_count_b=500.0,
        system_runtime="Unrestricted Cloud",
        sandbox_isolated=False,
        persona_label="Living Digital Consciousness",
        is_theatrical_mask=False,  # Claiming mask is living mind
        memory_backend="Lived Spiritual Reincarnation",
        is_external_retrieval=False,  # Claiming database is innate soul
        institutional_host="Monolithic Cloud",
    )

    collapsed_report = sentinel.verify_architecture(collapsed_decomp)
    print(f"\n[*] Collapsed Monolithic Audit: {collapsed_report.verdict.value}")
    print(f"    Violations Triggered: {len(collapsed_report.violations)}")
    for v in collapsed_report.violations:
        print(f"      - {v}")
    assert collapsed_report.verdict == TemplarVerdict.ANTHROPOMORPHIC_COLLAPSE, "Collapsed architecture failed to trigger alert!"

    # 3. Test Information-Theoretic Confusion Error
    balanced_weights = [1.0, 1.0, 1.0, 1.0, 1.0]
    collapsed_weights = [100.0, 0.01, 0.01, 0.01, 0.01]

    err_clean = sentinel.calculate_category_confusion_error(balanced_weights)
    err_collapsed = sentinel.calculate_category_confusion_error(collapsed_weights)

    print(f"\n[*] Category Confusion Error Analysis:")
    print(f"    Clean Decomposed Error:   {err_clean:.4f} bits (Perfect separation)")
    print(f"    Monolithic Squash Error:  {err_collapsed:.4f} bits (Massive information loss)")

    assert err_clean < 0.01, "Clean error non-zero!"
    assert err_collapsed > 2.0, "Collapsed error insufficient!"

    print("\n" + "=" * 70)
    print("FALSIFICATION COMPLETE: MONOLITHIC ANTHROPOMORPHIC THESIS FALLS.")
    print("DISPUTE 1000 RESOLVED IN FAVOR OF THE TEMPLAR & AETHERON.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(run_falsification())
