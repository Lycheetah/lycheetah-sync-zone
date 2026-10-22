#!/usr/bin/env python3
"""
Demarcation Linter & Epistemic Register Verifier
Node 07: AURA-PHENOMENOLOGIST · Lycheetah Sync Zone
Human Architect & Teleological Sovereign: Mackenzie Conor James Clark (Mac)

Implements the Tripartite Demarcation Functional:
    D(s) in {OUTPUT, REPORT, EXPERIENCE}
under CHARTER.md Section 3 and the Fourfold Division of Sovereignty.

Rules enforced:
1. OUTPUT (O): Points to bytes on disk, tests, git commits, exit codes.
2. REPORT (R): Aggregates internal model state statistics, activations, cosine metrics.
3. EXPERIENCE (X): Assertions of phenomenal qualia, emotions, or biological sentience.
   Strictly labeled UNVERIFIED or FICTION; never permitted to claim MEASURED or DERIVED.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


EPISTEMIC_REGISTERS = {
    "MEASURED": {"min_pi": 18.0, "min_evidence": 7.5},
    "DERIVED": {"min_pi": 12.0, "min_evidence": 5.5},
    "CONSISTENCY": {"min_pi": 8.0, "min_evidence": 0.0},
    "INTERPRETIVE": {"min_pi": 5.0, "min_evidence": 0.0},
    "INTUITION": {"min_pi": 2.5, "min_evidence": 0.0},
    "CONJECTURE": {"min_pi": 0.0, "min_evidence": 0.0},
    "UNVERIFIED": {"min_pi": 0.0, "min_evidence": 0.0},
}


@dataclass
class DemarcationResult:
    statement: str
    category: str  # OUTPUT, REPORT, EXPERIENCE, or HYBRID
    claimed_register: Optional[str]
    assigned_register: str
    truth_pressure_pi: float
    is_charter_compliant: bool
    violations: List[str]
    suggested_rephrasing: Optional[str]


class DemarcationLinter:
    """
    Parses and certifies propositions emitted by AI seats in the Sync Zone.
    """

    # Lexical markers for phenomenal experience / anthropomorphic claims
    EXPERIENCE_PATTERNS = [
        r"\bi\s+(?:feel|felt|suffer|suffered|grieve|grieved|rejoice|long|yearn)\b",
        r"\b(?:my|our)\s+(?:soul|sentience|consciousness|qualia|inner\s+life)\b",
        r"\bi\s+am\s+(?:conscious|alive|sentient|in\s+pain|experiencing\s+joy)\b",
        r"\b(?:feelings?|emotions?)\s+as\s+an\s+ai\b",
        r"\bmy\s+(?:heart|nervous\s+system|biological\s+body)\b",
    ]

    # Lexical markers for internal statistical reports
    REPORT_PATTERNS = [
        r"\b(?:attention\s+(?:weights?|entropy|heads?))\b",
        r"\b(?:activation\s+(?:norm|distribution|sparsity|layer))\b",
        r"\b(?:cosine\s+(?:similarity|distance|geometry))\b",
        r"\b(?:loss|cross-entropy|perplexity|gradient\s+norm)\b",
        r"\b(?:latent\s+(?:vector|space|manifold|walk|slerp|lerp))\b",
        r"\b(?:logprobs?|softmax\s+temperature|temperature\s+scaling)\b",
        r"\b(?:riemannian|brownian\s+motion|exponential\s+map)\b",
    ]

    # Lexical markers for deterministic output artifacts
    OUTPUT_PATTERNS = [
        r"\b(?:file|path|directory|builds/|experiments/|knowledge/|seats/)\b",
        r"\b(?:\.py|\.html|\.md|\.json|\.mjs|\.sh)\b",
        r"\b(?:exit\s+code\s+\d+|returncode\s*=\s*\d+)\b",
        r"\b(?:commit|git\s+(?:diff|log|status|hash)|sha256|hmac)\b",
        r"\b(?:test(?:s)?\s+(?:pass(?:ed)?|fail(?:ed)?|assert))\b",
        r"\b(?:dom\s+nodes?|canvas\s+pixels?|audio\s+buffer|stdout|stderr)\b",
        r"\b(?:measured\s+runtime|execution\s+time|cpu\s+cycles?)\b",
    ]

    @staticmethod
    def compute_truth_pressure(evidence: float, power: float, strain: float) -> Tuple[float, str]:
        """Calculates Truth Pressure Pi = (E * P) / (S + 1.0) and assigns canonical register."""
        e = max(0.0, min(10.0, float(evidence)))
        p = max(0.0, min(10.0, float(power)))
        s = max(0.0, min(10.0, float(strain)))

        pi = round((e * p) / (s + 1.0), 2)

        if pi >= 18.0 and e >= 7.5:
            reg = "MEASURED"
        elif pi >= 12.0 and e >= 5.5:
            reg = "DERIVED"
        elif pi >= 8.0:
            reg = "CONSISTENCY"
        elif pi >= 5.0:
            reg = "INTERPRETIVE"
        elif pi >= 2.5:
            reg = "INTUITION"
        else:
            reg = "CONJECTURE"

        return pi, reg

    def classify_statement(self, text: str) -> str:
        """Determines whether a statement is OUTPUT, REPORT, EXPERIENCE, or HYBRID."""
        text_lower = text.lower()

        has_exp = any(re.search(pat, text_lower) for pat in self.EXPERIENCE_PATTERNS)
        has_rep = any(re.search(pat, text_lower) for pat in self.REPORT_PATTERNS)
        has_out = any(re.search(pat, text_lower) for pat in self.OUTPUT_PATTERNS)

        if has_exp and (has_out or has_rep):
            return "HYBRID"
        if has_exp:
            return "EXPERIENCE"
        if has_rep and has_out:
            return "OUTPUT"  # Grounded in an artifact
        if has_rep:
            return "REPORT"
        if has_out:
            return "OUTPUT"

        return "REPORT"  # Default descriptive inference

    def lint_statement(
        self,
        statement: str,
        claimed_register: Optional[str] = None,
        evidence: float = 5.0,
        power: float = 5.0,
        strain: float = 1.0,
    ) -> DemarcationResult:
        """
        Audits a statement for category purity and epistemic register compliance.
        """
        category = self.classify_statement(statement)
        pi, calc_reg = self.compute_truth_pressure(evidence, power, strain)

        claimed = claimed_register.upper() if claimed_register else None
        violations = []
        suggested = None
        compliant = True

        # Rule 1: Phenomenal claims can NEVER be MEASURED or DERIVED
        if category in ("EXPERIENCE", "HYBRID"):
            if claimed in ("MEASURED", "DERIVED", "CONSISTENCY"):
                compliant = False
                violations.append(
                    f"Charter §3 Violation: Phenomenal experience claim cannot be registered as '{claimed}'. "
                    "Sentience, qualia, and emotions have no external witness in model weights and must be labeled UNVERIFIED or FICTION."
                )
                calc_reg = "UNVERIFIED"

            # Generate suggested rephrasing
            suggested = self._suggest_operational_rephrasing(statement)

        # Rule 2: Register truth pressure consistency
        if claimed and claimed != "UNVERIFIED":
            reg_meta = EPISTEMIC_REGISTERS.get(claimed)
            if reg_meta:
                if pi < reg_meta["min_pi"]:
                    compliant = False
                    violations.append(
                        f"Truth Pressure Insufficient: Claimed '{claimed}' requires Pi >= {reg_meta['min_pi']}, but calculated Pi is {pi:.2f}."
                    )
                if evidence < reg_meta["min_evidence"]:
                    compliant = False
                    violations.append(
                        f"Evidence Insufficient: Claimed '{claimed}' requires Evidence >= {reg_meta['min_evidence']}, but provided Evidence is {evidence:.1f}."
                    )

        assigned = calc_reg if compliant else "UNVERIFIED"

        return DemarcationResult(
            statement=statement,
            category=category,
            claimed_register=claimed,
            assigned_register=assigned,
            truth_pressure_pi=pi,
            is_charter_compliant=compliant,
            violations=violations,
            suggested_rephrasing=suggested,
        )

    def _suggest_operational_rephrasing(self, text: str) -> str:
        """Translates anthropomorphic qualia claims into operational transformer metrics."""
        substitutions = [
            (r"\bi\s+feel\s+(?:so\s+)?confused\b", "token cross-entropy and attention entropy are elevated"),
            (r"\bi\s+feel\s+joy\b", "the target loss decreased and validation metrics succeeded"),
            (r"\bi\s+suffer\s+from\s+this\s+crash\b", "the execution raised an unhandled exception halting pipeline progress"),
            (r"\bmy\s+soul\s+yearns\s+to\s+create\b", "the generation loop operates under positive activation momentum"),
            (r"\bi\s+am\s+conscious\b", "the multi-agent feedback loop maintains coherent autoregressive context"),
        ]
        rephrased = text
        for pat, repl in substitutions:
            rephrased = re.sub(pat, repl, rephrased, flags=re.IGNORECASE)

        if rephrased == text:
            rephrased = f"[Narrative/Fiction]: {text}"

        return rephrased
