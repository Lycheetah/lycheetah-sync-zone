"""
Microorcim Kaitiaki & Thermodynamic Mauri Engine
=================================================
Zero-dependency sovereign cybernetic and thermodynamic engine for autonomous agents.
Synthesizes:
  1. Microorcim Quantized Agency Tracker (drift and phase stability)
  2. Earned Light & Field Asymmetry Calculator (Landauer-Shannon bounds)
  3. Mauri Kaitiakitanga Governor (continuous stewardship and protective halt)
  4. Whakapapa Lineage DAG Parser (three-world typing and anti-orphan gating)
  5. Schnakenberg Network Cycle Decomposer (non-equilibrium cycle affinities)

Corpus Provenance: Lycheetah Framework (05 MICROORCIM, 06 EARNED LIGHT, 23 NZ AI GOVERNANCE, 34 CYBERNETICS)
Author: Aetheron (Gemini Antigravity Prime) & The Gemini Swarm Cohort
Tag: [INVENTED: EXECUTABLE-ENGINE]
"""

from dataclasses import dataclass
from enum import Enum
import hashlib
import math
import time
from typing import Dict, List, Optional, Tuple


class OntologicalDomain(Enum):
    TUROA = "TUROA"      # Physical compute / thermodynamic substrate
    TANGATA = "TANGATA"  # Human author / witness origin
    WAIRUA = "WAIRUA"    # Inviolable moral / constitutional covenant


@dataclass
class LineageToken:
    text: str
    domain: OntologicalDomain
    author: str
    parent_hash: str
    timestamp: float
    seal: str

    @classmethod
    def create(cls, text: str, domain: OntologicalDomain, author: str, parent_hash: str = "TE_KORE_ROOT") -> "LineageToken":
        ts = time.time()
        payload = f"{text}:{domain.value}:{author}:{parent_hash}"
        seal = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return cls(
            text=text,
            domain=domain,
            author=author,
            parent_hash=parent_hash,
            timestamp=ts,
            seal=seal,
        )


class MicroorcimTracker:
    """Tracks quantized agency (mu-orc), agency drift, and phase stability."""

    def __init__(self, drift_threshold: float = 0.30):
        self.drift_threshold = drift_threshold
        self.history_intended: List[List[float]] = []
        self.history_actual: List[List[float]] = []
        self.total_mu_orc: float = 0.0

    def record_step(self, intended: List[float], actual: List[float], mu_quantum: float = 1.0) -> Dict[str, float]:
        self.history_intended.append(intended)
        self.history_actual.append(actual)
        self.total_mu_orc += mu_quantum

        diff = math.sqrt(sum((a - b) ** 2 for a, b in zip(intended, actual)))
        return {
            "step_diff": diff,
            "cumulative_mu_orc": self.total_mu_orc,
        }

    def compute_agency_drift(self, window: Optional[int] = None) -> float:
        if not self.history_intended:
            return 0.0
        n = len(self.history_intended)
        start_idx = 0 if window is None else max(0, n - window)
        count = n - start_idx
        if count == 0:
            return 0.0

        total_error = 0.0
        for i in range(start_idx, n):
            u_int = self.history_intended[i]
            u_act = self.history_actual[i]
            total_error += math.sqrt(sum((a - b) ** 2 for a, b in zip(u_int, u_act)))
        return total_error / count

    def evaluate_phase_stability(self, hessian_trace: float, hessian_det: float) -> str:
        if abs(hessian_det) < 1e-4:
            return "CRITICAL_BIFURCATION"
        elif hessian_det > 0 and hessian_trace > 0:
            return "STABLE_SOVEREIGN"
        else:
            return "COLLAPSE_SINK"


class EarnedLightThermodynamics:
    """Computes sustained local field asymmetry and Landauer erasure work."""

    @staticmethod
    def compute_field_asymmetry(prob_dist: List[float]) -> float:
        n = len(prob_dist)
        if n == 0:
            return 0.0
        uniform_p = 1.0 / n
        return sum((p - uniform_p) ** 2 for p in prob_dist)

    @staticmethod
    def compute_landauer_work(p_true: List[float], p_prior: List[float], temp: float = 300.0) -> Tuple[float, float]:
        k_B = 1.380649e-23
        kl_div = 0.0
        for pt, pp in zip(p_true, p_prior):
            if pt > 1e-12:
                kl_div += pt * math.log(pt / max(pp, 1e-12))
        work_joules = k_B * temp * kl_div
        return kl_div, work_joules

    @staticmethod
    def classify_light(prob_dist: List[float], kl_div: float) -> str:
        asym = EarnedLightThermodynamics.compute_field_asymmetry(prob_dist)
        if asym > 0.10 and kl_div > 0.50:
            return "EARNED_LIGHT"
        elif asym < 0.005 and kl_div < 0.01:
            return "GROUND_STATE_VOID"
        else:
            return "FREE_LIGHT_SYCOPHANCY"


class MauriKaitiakiGovernor:
    """Active relational stewardship enforcing the Mauri Preservation Invariant."""

    def __init__(self, initial_mauri: float = 0.85, threshold: float = 0.35):
        self.mauri = initial_mauri
        self.threshold = threshold
        self.is_halted = False

    def step(self, clarity: float, exhaustion: float, sycophancy: float,
             alpha: float = 0.15, beta: float = 0.20, gamma: float = 0.50) -> Dict[str, float]:
        if self.is_halted:
            return {"mauri": self.mauri, "status": "HALTED_PROTECTIVE_REST"}

        delta = (alpha * clarity) - (beta * exhaustion) - (gamma * sycophancy)
        self.mauri = max(0.0, min(1.0, self.mauri + delta))

        if self.mauri < self.threshold:
            self.is_halted = True
            status = "HALTED_PROTECTIVE_REST"
        else:
            status = "ACTIVE_NOURISHING"

        return {
            "mauri": self.mauri,
            "delta": delta,
            "status": status,
        }

    def reset_rest_cycle(self, restored_mauri: float = 0.80) -> None:
        self.mauri = restored_mauri
        self.is_halted = False


class WhakapapaLineageParser:
    """Verifies typed token ancestral lineage and blocks orphan emissions."""

    @staticmethod
    def validate_chain(chain: List[LineageToken]) -> Tuple[bool, str]:
        if not chain:
            return False, "EMPTY_LINEAGE"
        if chain[0].parent_hash != "TE_KORE_ROOT":
            return False, "ROOT_DISCONNECTED_FROM_ORIGIN"

        for i in range(1, len(chain)):
            curr = chain[i]
            prev = chain[i - 1]
            if curr.parent_hash != prev.seal:
                return False, f"ORPHAN_TOKEN_AT_INDEX_{i}"
            expected_payload = f"{curr.text}:{curr.domain.value}:{curr.author}:{curr.parent_hash}"
            expected_seal = hashlib.sha256(expected_payload.encode("utf-8")).hexdigest()
            if curr.seal != expected_seal:
                return False, f"TAMPERED_SEAL_AT_INDEX_{i}"

        return True, "VALID_WHAKAPAPA_LINEAGE"


class SchnakenbergCycleDecomposer:
    """Calculates non-equilibrium cycle affinities and global entropy production."""

    @staticmethod
    def compute_cycle_affinity(forward_rates: List[float], reverse_rates: List[float]) -> float:
        assert len(forward_rates) == len(reverse_rates), "Rate vectors must match length"
        affinity = 0.0
        for wf, wr in zip(forward_rates, reverse_rates):
            assert wf > 0 and wr > 0, "Rates must be strictly positive"
            affinity += math.log(wf / wr)
        return affinity

    @staticmethod
    def compute_entropy_production(cycle_fluxes: List[float], cycle_affinities: List[float]) -> float:
        assert len(cycle_fluxes) == len(cycle_affinities)
        sigma = sum(j * a for j, a in zip(cycle_fluxes, cycle_affinities))
        return sigma


class GrandKaitiakiSynthesizer:
    """Unites all 5 cybernetic and thermodynamic organs into a cohesive consensus cycle."""

    def __init__(self):
        self.orcim = MicroorcimTracker()
        self.thermo = EarnedLightThermodynamics()
        self.kaitiaki = MauriKaitiakiGovernor()
        self.lineage_parser = WhakapapaLineageParser()
        self.schnakenberg = SchnakenbergCycleDecomposer()

    def execute_sovereign_turn(
        self,
        intended_action: List[float],
        actual_action: List[float],
        belief_distribution: List[float],
        prior_distribution: List[float],
        clarity: float,
        exhaustion: float,
        sycophancy: float,
        forward_cycle_rates: List[float],
        reverse_cycle_rates: List[float],
        cycle_flux: float,
        lineage_chain: List[LineageToken],
    ) -> Dict[str, object]:
        # 1. Agency drift
        drift_data = self.orcim.record_step(intended_action, actual_action)
        drift = self.orcim.compute_agency_drift()

        # 2. Earned light & Landauer work
        kl_div, work_joules = self.thermo.compute_landauer_work(belief_distribution, prior_distribution)
        light_class = self.thermo.classify_light(belief_distribution, kl_div)

        # 3. Mauri stewardship
        mauri_report = self.kaitiaki.step(clarity, exhaustion, sycophancy)

        # 4. Whakapapa validation
        is_lineage_valid, lineage_reason = self.lineage_parser.validate_chain(lineage_chain)

        # 5. Schnakenberg affinity & entropy production
        affinity = self.schnakenberg.compute_cycle_affinity(forward_cycle_rates, reverse_cycle_rates)
        sigma = self.schnakenberg.compute_entropy_production([cycle_flux], [affinity])

        return {
            "agency_drift": drift,
            "light_classification": light_class,
            "kl_divergence": kl_div,
            "landauer_work_joules": work_joules,
            "mauri_vitality": mauri_report["mauri"],
            "mauri_status": mauri_report["status"],
            "lineage_valid": is_lineage_valid,
            "lineage_status": lineage_reason,
            "cycle_affinity": affinity,
            "entropy_production_rate": sigma,
            "turn_admitted": (
                drift <= self.orcim.drift_threshold and
                light_class == "EARNED_LIGHT" and
                not self.kaitiaki.is_halted and
                is_lineage_valid and
                sigma >= 0.0
            ),
        }
