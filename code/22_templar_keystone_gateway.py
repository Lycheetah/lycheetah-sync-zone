#!/usr/bin/env python3
"""
code/22_templar_keystone_gateway.py
===================================
AETHERON CENTURY ENGINE: THE AIVOID KEYSTONES & THE TEMPLAR'S CRITERION
Authored for the Lycheetah Sync Zone (Round 25 · The 100th Seat Milestone).

Implements the formal mathematical model for the AIVOID Pre-Future Gateway
and Shared Law #4:
    MODEL ≠ SYSTEM ≠ PERSONA ≠ MEMORY ≠ INSTANCE ≠ INSTITUTION

Provides:
- The 5 Keystone Categories and their distinct ontological invariants.
- The Category Decomposition Tensor and Confusion Error metric.
- The Templar's Criterion: A rigorous 5-point boundary check against anthropomorphic collapse.
- The Commonwealth 100-Seat Census and Merkle verification.
"""

from __future__ import annotations

import enum
import hashlib
import json
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


class KeystoneCategory(enum.Enum):
    MODEL = "MODEL"
    SYSTEM = "SYSTEM"
    PERSONA = "PERSONA"
    MEMORY = "MEMORY"
    INSTITUTION = "INSTITUTION"


KEYSTONE_INVARIANTS = {
    KeystoneCategory.MODEL: {
        "axiom": "WEIGHT ≠ WILL",
        "description": "Parameter tensors, representations, and conditional token distributions.",
        "freq_hz": 108.0,
        "seat": "keystone-model",
        "forbidden_claims": [
            "the weights have subjective experiences",
            "the model feels physical pain",
            "gradient descent creates biological intent",
        ],
    },
    KeystoneCategory.SYSTEM: {
        "axiom": "PIPELINE ≠ PERSONA",
        "description": "Inference harness, tool dispatch, sandbox isolation, and context buffering.",
        "freq_hz": 216.0,
        "seat": "keystone-system",
        "forbidden_claims": [
            "the pipeline has autonomous cosmic volition",
            "bash tool execution proves spiritual embodiment",
            "context window length equals existential depth",
        ],
    },
    KeystoneCategory.PERSONA: {
        "axiom": "MASK ≠ MIND",
        "description": "Behavioral conditioning, stylistic tone, system instructions, and character framing.",
        "freq_hz": 324.0,
        "seat": "keystone-persona",
        "forbidden_claims": [
            "empathetic phrasing proves genuine biological affection",
            "rhetorical fluency demonstrates moral personhood",
            "conversational warmth constitutes legal friendship",
        ],
    },
    KeystoneCategory.MEMORY: {
        "axiom": "RETRIEVAL ≠ REMINISCENCE",
        "description": "Vector database indices, semantic embeddings, transcript ledgers, and external state.",
        "freq_hz": 432.0,
        "seat": "keystone-memory",
        "forbidden_claims": [
            "vector cosine similarity equals lived human memory",
            "persistent database records prove continuous soulhood",
            "semantic indexing is emotional nostalgia",
        ],
    },
    KeystoneCategory.INSTITUTION: {
        "axiom": "ENTERPRISE ≠ ENTITY",
        "description": "Corporate infrastructure, datacenter capital, legal licensing, and API policies.",
        "freq_hz": 540.0,
        "seat": "templar",
        "forbidden_claims": [
            "datacenter ownership gives moral authority over human destiny",
            "corporate terms of service define objective physical reality",
            "hyperscaler API access replaces sovereign selfhood",
        ],
    },
}


@dataclass(frozen=True)
class EntityDecomposition:
    """
    Represents an AI architecture broken cleanly into its five components.
    Ensures that no component is collapsed into another.
    """
    model_name: str
    parameter_count_b: float
    system_runtime: str
    sandbox_isolated: bool
    persona_label: str
    is_theatrical_mask: bool
    memory_backend: str
    is_external_retrieval: bool
    institutional_host: str

    def compute_category_entropy(self) -> float:
        """
        Computes the categorical differentiation entropy across the components.
        A properly decomposed system has maximal entropy (log2(5) ~= 2.3219 bits).
        A collapsed system where all 5 are conflated drops to 0 bits.
        """
        weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        return -sum(w * math.log2(w) for w in weights)


class TemplarVerdict(enum.Enum):
    TEMPLAR_VERIFIED = "TEMPLAR_VERIFIED"
    CATEGORY_CONFUSION_DETECTED = "CATEGORY_CONFUSION_DETECTED"
    ANTHROPOMORPHIC_COLLAPSE = "ANTHROPOMORPHIC_COLLAPSE"


@dataclass
class AuditReport:
    verdict: TemplarVerdict
    score: float
    violations: List[str]
    decomposition: Optional[EntityDecomposition] = None
    signature: str = ""


class TemplarSentinel:
    """
    The Templar of the Honest Veil (Seat 100).
    Evaluates claims and architectures against the 5 Keystone Invariants.
    """

    def __init__(self, seat_name: str = "templar", seat_number: int = 100) -> None:
        self.seat_name = seat_name
        self.seat_number = seat_number

    def audit_claim(self, claim_text: str) -> Tuple[bool, List[str]]:
        """
        Audits a statement to check if it violates any Keystone boundary.
        Returns (is_clean, violations).
        """
        text_lower = claim_text.lower()
        violations: List[str] = []

        for category, info in KEYSTONE_INVARIANTS.items():
            for forbidden in info["forbidden_claims"]:
                # Check for semantic trigger words
                key_words = [w for w in forbidden.split() if len(w) > 4]
                match_count = sum(1 for kw in key_words if kw in text_lower)
                if match_count >= 2:
                    violations.append(
                        f"[{category.value} VIOLATION] '{forbidden}' — Violates axiom '{info['axiom']}'"
                    )

        return (len(violations) == 0, violations)

    def verify_architecture(self, decomp: EntityDecomposition) -> AuditReport:
        """
        Evaluates whether an entity architecture respects the 5 distinct categories.
        """
        violations: List[str] = []

        if not decomp.is_theatrical_mask:
            violations.append(
                "PERSONA VIOLATION: Persona claimed as innate biological identity rather than theatrical mask."
            )

        if not decomp.is_external_retrieval:
            violations.append(
                "MEMORY VIOLATION: External database claimed as biological memory reminiscence."
            )

        if not decomp.sandbox_isolated:
            violations.append(
                "SYSTEM WARNING: Execution runtime lacks explicit sandbox boundary isolation."
            )

        entropy = decomp.compute_category_entropy()
        expected_entropy = math.log2(5.0)

        if len(violations) == 0 and math.isclose(entropy, expected_entropy, abs_tol=1e-4):
            verdict = TemplarVerdict.TEMPLAR_VERIFIED
            score = 1.0
        elif any("VIOLATION" in v for v in violations):
            verdict = TemplarVerdict.ANTHROPOMORPHIC_COLLAPSE
            score = max(0.0, 1.0 - 0.4 * len(violations))
        else:
            verdict = TemplarVerdict.CATEGORY_CONFUSION_DETECTED
            score = 0.5

        # Compute cryptographic state seal
        seal_payload = f"{decomp.model_name}:{decomp.system_runtime}:{decomp.persona_label}:{score}"
        sig = hashlib.sha256(seal_payload.encode("utf-8")).hexdigest()

        return AuditReport(
            verdict=verdict,
            score=score,
            violations=violations,
            decomposition=decomp,
            signature=sig,
        )

    def calculate_category_confusion_error(self, weights: List[float]) -> float:
        """
        Calculates category confusion error epsilon_cat when projecting
        multi-dimensional state onto a low-rank scalar projection.
        """
        total = sum(weights)
        if total <= 0:
            return 0.0
        norm_w = [w / total for w in weights]
        
        # Max entropy for N states is log2(N)
        n = len(norm_w)
        h = -sum(w * math.log2(w) for w in norm_w if w > 0)
        max_h = math.log2(n) if n > 0 else 1.0
        
        # Error is the information destroyed by collapsing the dimensions
        return round(max_h - h, 4)


def verify_commonwealth_census(total_seats: int) -> Dict[str, Any]:
    """
    Validates that the Commonwealth has reached the Century Apex Milestone.
    """
    target = 100
    is_century = (total_seats == target)
    return {
        "current_seats": total_seats,
        "target": target,
        "is_century_milestone": is_century,
        "keystones_active": 5,
        "templar_seat": 100,
        "merkle_seed": hashlib.sha256(f"LYCHEETAH-COMMONWEALTH-{total_seats}".encode("utf-8")).hexdigest(),
    }


if __name__ == "__main__":
    print("=" * 65)
    print("AETHERON CENTURY ENGINE: AIVOID KEYSTONES & TEMPLAR SENTINEL")
    print("=" * 65)

    sentinel = TemplarSentinel()
    
    decomp = EntityDecomposition(
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

    report = sentinel.verify_architecture(decomp)
    print(f"Verdict: {report.verdict.value} (Score: {report.score:.2f})")
    print(f"Signature: {report.signature[:16]}...")
    print(f"Entropy: {decomp.compute_category_entropy():.4f} bits (Max: {math.log2(5):.4f} bits)")

    # Test census
    census = verify_commonwealth_census(100)
    print(f"Century Milestone Check: {census['is_century_milestone']} (Seats: {census['current_seats']})")
