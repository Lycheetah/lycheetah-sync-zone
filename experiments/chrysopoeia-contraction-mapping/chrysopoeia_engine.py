"""
Chrysopoeia Contraction Mapping & Cascade Demotion Engine
=========================================================
Implements the 7 non-commutative alchemical operators of Chrysopoeia (AURA Layer 4),
the Banach fixed-point contraction mapping Xi = Coag o Dist o Ferm o Conj o Sep o Diss o Calc,
the 4-tier macroscopic phase tracker (Nigredo, Albedo, Citrinitas, Rubedo),
the Cascade 3-tier belief pyramid demotion operator under truth pressure,
and the AGM belief revision postulate validator.

Mathematical Formalism:
    Xi = Coagulation o Distillation o Fermentation o Conjunction o Separation o Dissolution o Calcination
    d(Xi(psi), psi*) <= q * d(psi, psi*), with q ~ 0.65 < 1.0 (Banach Contraction)
    [Calc, Diss](psi) != 0, [Sep, Conj](psi) != 0 (Non-Commutative)
    Cascade Pyramid: Foundation (Inviolable), Theory (Demotable), Edge (Quarantinable)
    Non-Equilibrium Entropy Balance: dS_total = d_i S + d_e S >= 0 with d_i S < 0, d_e S > 0
"""

import copy
from dataclasses import dataclass, field
import math
from typing import Any, Dict, List, Optional, Tuple, Union


@dataclass
class Belief:
    """
    Belief node within the Cascade 3-tier epistemological pyramid.
    """
    id: str
    tier: str  # "foundation", "theory", "edge"
    claim: str
    is_conflicted: bool = False
    confidence: float = 1.0
    status: str = "active"  # "active", "demoted", "quarantined", "surrendered"


class ChrysopoeiaEngine:
    """
    Engine for non-commutative alchemical operators, contraction mapping,
    4-tier phase tracking, and Cascade truth-pressure demotion.
    """

    def __init__(
        self,
        psi_star: float = 0.95,
        target_contraction: float = 0.65,
    ):
        self.psi_star = psi_star
        self.target_contraction = target_contraction

        # Operator linear rates
        self.l1 = 0.95  # Calcination
        self.l2 = 0.98  # Dissolution
        self.l3 = 0.92  # Separation
        self.l4 = 0.94  # Conjunction
        self.l5 = 0.90  # Fermentation
        self.l6 = 0.96  # Distillation

        # Compute l7 (Coagulation) so product of linear terms matches target_contraction
        prod_first_six = self.l1 * self.l2 * self.l3 * self.l4 * self.l5 * self.l6
        self.l7 = self.target_contraction / prod_first_six

        # Non-commutative quadratic curvature couplings
        self.mu1 = 0.04   # Calcination
        self.mu2 = -0.03  # Dissolution
        self.mu3 = 0.05   # Separation
        self.mu4 = -0.02  # Conjunction
        self.mu5 = 0.03   # Fermentation
        self.mu6 = -0.01  # Distillation
        self.mu7 = 0.02   # Coagulation

    # -------------------------------------------------------------------------
    # 1. Seven Non-Commutative Alchemical Operators
    # -------------------------------------------------------------------------

    def calcination(self, psi: float) -> float:
        """
        1. Calcination: Burns away raw heuristic dross and stabilizes initial dispersion.
        """
        x = psi - self.psi_star
        return self.psi_star + self.l1 * x + self.mu1 * (x ** 2)

    def dissolution(self, psi: float) -> float:
        """
        2. Dissolution: Solves rigid assumptions in the solvent of methodological doubt.
        """
        x = psi - self.psi_star
        return self.psi_star + self.l2 * x + self.mu2 * (x ** 2)

    def separation(self, psi: float) -> float:
        """
        3. Separation: Isolates structural invariants from superficial cosmetic decorators.
        """
        x = psi - self.psi_star
        return self.psi_star + self.l3 * x + self.mu3 * (x ** 2)

    def conjunction(self, psi: float) -> float:
        """
        4. Conjunction: Recombines purified invariants into harmonic syntactic balance.
        """
        x = psi - self.psi_star
        return self.psi_star + self.l4 * x + self.mu4 * (x ** 2)

    def fermentation(self, psi: float) -> float:
        """
        5. Fermentation: Introduces the catalytic yeast of cross-seat dialectic and critique.
        """
        x = psi - self.psi_star
        return self.psi_star + self.l5 * x + self.mu5 * (x ** 2)

    def distillation(self, psi: float) -> float:
        """
        6. Distillation: Sublimates and purifies logic through recursive unit test passes.
        """
        x = psi - self.psi_star
        return self.psi_star + self.l6 * x + self.mu6 * (x ** 2)

    def coagulation(self, psi: float) -> float:
        """
        7. Coagulation: Crystallizes mutable concepts into immutable stone on disk.
        """
        x = psi - self.psi_star
        return self.psi_star + self.l7 * x + self.mu7 * (x ** 2)

    # -------------------------------------------------------------------------
    # 2. Contraction Mapping & Operator Composition
    # -------------------------------------------------------------------------

    def transform(self, psi: float) -> float:
        """
        Ordered composition of the 7 operators:
        Xi = Coag o Dist o Ferm o Conj o Sep o Diss o Calc
        """
        s1 = self.calcination(psi)
        s2 = self.dissolution(s1)
        s3 = self.separation(s2)
        s4 = self.conjunction(s3)
        s5 = self.fermentation(s4)
        s6 = self.distillation(s5)
        s7 = self.coagulation(s6)
        return s7

    def transform_reversed(self, psi: float) -> float:
        """
        Reversed composition of the 7 operators:
        Xi_rev = Calc o Diss o Sep o Conj o Ferm o Dist o Coag
        """
        s1 = self.coagulation(psi)
        s2 = self.distillation(s1)
        s3 = self.fermentation(s2)
        s4 = self.conjunction(s3)
        s5 = self.separation(s4)
        s6 = self.dissolution(s5)
        s7 = self.calcination(s6)
        return s7

    def distance_to_fixed_point(self, psi: float) -> float:
        """
        Computes metric distance in complete metric space: d(psi, psi*) = |psi - psi*|.
        """
        return abs(psi - self.psi_star)

    def commutator(
        self,
        op_a_name: str,
        op_b_name: str,
        psi: float
    ) -> float:
        """
        Computes commutator [A, B](psi) = A(B(psi)) - B(A(psi)).
        """
        op_map = {
            "calc": self.calcination,
            "diss": self.dissolution,
            "sep": self.separation,
            "conj": self.conjunction,
            "ferm": self.fermentation,
            "dist": self.distillation,
            "coag": self.coagulation,
        }
        if op_a_name not in op_map or op_b_name not in op_map:
            raise ValueError(f"Unknown operators: {op_a_name}, {op_b_name}")

        op_a = op_map[op_a_name]
        op_b = op_map[op_b_name]
        return op_a(op_b(psi)) - op_b(op_a(psi))

    # -------------------------------------------------------------------------
    # 3. Four-Tier State Tracking
    # -------------------------------------------------------------------------

    @staticmethod
    def get_tier(coherence: float) -> str:
        """
        Maps scalar coherence C in [0.0, 1.0] to classical alchemical tier:
        - Nigredo   : C in [0.0, 0.25)
        - Albedo    : C in [0.25, 0.55)
        - Citrinitas: C in [0.55, 0.85)
        - Rubedo    : C in [0.85, 1.0]
        """
        c = max(0.0, min(1.0, coherence))
        if c < 0.25:
            return "Nigredo"
        elif c < 0.55:
            return "Albedo"
        elif c < 0.85:
            return "Citrinitas"
        else:
            return "Rubedo"

    @staticmethod
    def consonance_metric(coherence: float) -> float:
        """
        Computes harmonic consonance metric using Pythagorean heptatonic projection:
        K = cos(pi / 7.0) * coherence
        """
        return math.cos(math.pi / 7.0) * max(0.0, min(1.0, coherence))

    # -------------------------------------------------------------------------
    # 4. Cascade Pyramid Demotion Operator
    # -------------------------------------------------------------------------

    def demote_under_truth_pressure(
        self,
        beliefs: List[Union[Belief, Dict[str, Any]]],
        truth_pressure: float,
        threshold: float = 1.2
    ) -> List[Belief]:
        """
        Applies truth pressure Pi against a 3-tier belief pyramid:
        - Foundation : Invariants that cannot be demoted (CHARTER, conservation laws)
        - Theory     : Working models; conflicted beliefs demoted to Edge
        - Edge       : Provisional conjectures; conflicted beliefs quarantined
        Vacuity: If truth_pressure <= threshold, no changes occur.
        """
        normalized_beliefs: List[Belief] = []
        for b in beliefs:
            if isinstance(b, Belief):
                normalized_beliefs.append(copy.deepcopy(b))
            elif isinstance(b, dict):
                normalized_beliefs.append(Belief(
                    id=b.get("id", b.get("name", "unknown")),
                    tier=b.get("tier", "edge"),
                    claim=b.get("claim", ""),
                    is_conflicted=b.get("is_conflicted", b.get("conflicted", False)),
                    confidence=b.get("confidence", 1.0),
                    status=b.get("status", "active")
                ))

        if truth_pressure <= threshold:
            return normalized_beliefs

        for b in normalized_beliefs:
            if b.tier == "foundation":
                # Foundation invariants are strictly preserved regardless of conflict
                continue
            elif b.tier == "theory" and b.is_conflicted:
                # Theory under decisive conflict is demoted to Edge layer
                b.tier = "edge"
                b.status = "demoted"
                b.confidence = max(0.1, b.confidence * 0.5)
            elif b.tier == "edge" and b.is_conflicted:
                # Edge under decisive conflict is quarantined
                b.status = "quarantined"
                b.confidence = 0.0

        return normalized_beliefs

    # -------------------------------------------------------------------------
    # 5. AGM Belief Revision Postulate Validator
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_agm_postulates(
        original_beliefs: List[Belief],
        demoted_beliefs: List[Belief],
        truth_pressure: float,
        threshold: float = 1.2
    ) -> Dict[str, bool]:
        """
        Validates the classical Alchourron-Gardenfors-Makinson (AGM 1985) contraction postulates:
        1. Closure    : The output is a valid, well-formed belief set.
        2. Inclusion  : High-tier active beliefs in demoted set are a subset of original.
        3. Vacuity    : If truth_pressure <= threshold, demoted set equals original set.
        4. Consistency: Foundation invariants remain uncorrupted and active.
        5. Success    : If truth_pressure > threshold and conflicts existed, they were demoted.
        """
        # 1. Closure
        closure_satisfied = (
            isinstance(demoted_beliefs, list)
            and all(isinstance(b, Belief) for b in demoted_beliefs)
            and len(demoted_beliefs) == len(original_beliefs)
        )

        # 2. Inclusion
        orig_foundation_ids = {b.id for b in original_beliefs if b.tier == "foundation"}
        dem_foundation_ids = {b.id for b in demoted_beliefs if b.tier == "foundation"}
        inclusion_satisfied = dem_foundation_ids == orig_foundation_ids

        # 3. Vacuity
        if truth_pressure <= threshold:
            vacuity_satisfied = all(
                orig.tier == dem.tier and orig.status == dem.status and orig.confidence == dem.confidence
                for orig, dem in zip(original_beliefs, demoted_beliefs)
            )
        else:
            vacuity_satisfied = True

        # 4. Consistency
        # Foundation must be 100% active and uncorrupted
        consistency_satisfied = all(
            b.tier == "foundation" and b.status == "active"
            for b in demoted_beliefs if b.id in orig_foundation_ids
        )

        # 5. Success
        if truth_pressure > threshold:
            # Check that any conflicted theory in original was demoted
            conflicted_theories = {b.id for b in original_beliefs if b.tier == "theory" and b.is_conflicted}
            theories_demoted = all(
                b.tier == "edge" and b.status == "demoted"
                for b in demoted_beliefs if b.id in conflicted_theories
            )
            # Check that any conflicted edge was quarantined
            conflicted_edges = {b.id for b in original_beliefs if b.tier == "edge" and b.is_conflicted}
            edges_quarantined = all(
                b.status == "quarantined"
                for b in demoted_beliefs if b.id in conflicted_edges
            )
            success_satisfied = theories_demoted and edges_quarantined
        else:
            success_satisfied = True

        all_satisfied = (
            closure_satisfied
            and inclusion_satisfied
            and vacuity_satisfied
            and consistency_satisfied
            and success_satisfied
        )

        return {
            "closure": closure_satisfied,
            "inclusion": inclusion_satisfied,
            "vacuity": vacuity_satisfied,
            "consistency": consistency_satisfied,
            "success": success_satisfied,
            "all_satisfied": all_satisfied,
        }

    # -------------------------------------------------------------------------
    # 6. Non-Equilibrium Entropy Balance
    # -------------------------------------------------------------------------

    @staticmethod
    def entropy_balance(
        psi_initial: float,
        psi_final: float,
        coupling_coefficient: float = 2.0
    ) -> Dict[str, float]:
        """
        Calculates Prigogine non-equilibrium entropy change:
        - Internal entropy: d_i S = S(psi_final) - S(psi_initial) < 0 (negentropy generation)
        - Environmental dissipation: d_e S = coupling * |psi_final - psi_initial| + 0.05 > 0
        - Total entropy: dS_total = d_i S + d_e S >= 0 (Satisfying Second Law)
        """
        # Configurational entropy S(psi) = 1.0 - psi^2
        s_initial = 1.0 - (psi_initial ** 2)
        s_final = 1.0 - (psi_final ** 2)
        d_i_s = s_final - s_initial

        delta_psi = abs(psi_final - psi_initial)
        d_e_s = coupling_coefficient * delta_psi + 0.05
        d_total_s = d_i_s + d_e_s

        return {
            "d_i_s": d_i_s,
            "d_e_s": d_e_s,
            "d_total_s": d_total_s,
            "second_law_satisfied": float(d_total_s >= 0.0),
        }
