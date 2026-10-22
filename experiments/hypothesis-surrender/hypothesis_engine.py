#!/usr/bin/env python3
"""
HYPOTHESIS SURRENDER ENGINE & FORMAL REVISION AUTOMATON
Aura Meridian · Node 02: AURA-REVISOR
Lycheetah Multi-Agent Sync Zone

Implements:
1. Deterministic 6-state hypothesis lifecycle automaton.
2. Bayesian likelihood updating & cumulative Bayes factor tracking.
3. Truth Pressure Pi = (E * P) / (S + 1.0) and Epistemic Register mapping.
4. Jeffreys decisive falsification boundary (K <= 0.01 or ln K <= -4.605).
5. Anti-immunization detection (Duhem-Quine complexity penalties under MDL).
6. Murphy (1973) Brier score penalty calculation for obstinate non-surrender.
7. Cryptographic origin-signed SurrenderCertificate generation.
"""

from __future__ import annotations

import enum
import hashlib
import hmac
import json
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple


class EpistemicRegister(str, enum.Enum):
    MEASURED = "MEASURED"
    DERIVED = "DERIVED"
    CONSISTENCY = "CONSISTENCY"
    INTERPRETIVE = "INTERPRETIVE"
    INTUITION = "INTUITION"
    CONJECTURE = "CONJECTURE"
    FALLS = "FALLS"


class HypothesisState(str, enum.Enum):
    PROPOSED = "PROPOSED"
    TENTATIVE = "TENTATIVE"
    CONFIRMED_MEASURED = "CONFIRMED_MEASURED"
    CONFIRMED_DERIVED = "CONFIRMED_DERIVED"
    CHALLENGED = "CHALLENGED"
    NARROWED = "NARROWED"
    SURRENDERED = "SURRENDERED"


def calculate_truth_pressure(evidence: float, power: float, strain: float) -> float:
    """Compute Truth Pressure Pi = (E * P) / (S + 1.0)."""
    e = max(0.0, float(evidence))
    p = max(0.0, float(power))
    s = max(0.0, float(strain))
    return round((e * p) / (s + 1.0), 4)


def determine_epistemic_register(
    truth_pressure: float,
    evidence: float,
    is_surrendered: bool = False,
) -> EpistemicRegister:
    """Map Truth Pressure and Evidence to Charter Truth Register."""
    if is_surrendered:
        return EpistemicRegister.FALLS
    if truth_pressure >= 18.0 and evidence >= 7.5:
        return EpistemicRegister.MEASURED
    if truth_pressure >= 12.0 and evidence >= 5.5:
        return EpistemicRegister.DERIVED
    if truth_pressure >= 8.0:
        return EpistemicRegister.CONSISTENCY
    if truth_pressure >= 5.0:
        return EpistemicRegister.INTERPRETIVE
    if truth_pressure >= 2.5:
        return EpistemicRegister.INTUITION
    return EpistemicRegister.CONJECTURE


@dataclass(frozen=True)
class Observation:
    datum_id: str
    description: str
    outcome: int  # 1 for event occurs, 0 for failure/absence
    likelihood_under_h: float  # P(D | H)
    likelihood_under_alt: float  # P(D | ~H)
    timestamp: float
    origin_mac: str

    @staticmethod
    def create(
        datum_id: str,
        description: str,
        outcome: int,
        likelihood_under_h: float,
        likelihood_under_alt: float,
        secret_key: bytes,
        timestamp: Optional[float] = None,
    ) -> "Observation":
        if outcome not in (0, 1):
            raise ValueError(f"Outcome must be binary (0 or 1), got {outcome}")
        if not (0.0 <= likelihood_under_h <= 1.0):
            raise ValueError(f"likelihood_under_h must be in [0, 1], got {likelihood_under_h}")
        if not (0.0 <= likelihood_under_alt <= 1.0):
            raise ValueError(f"likelihood_under_alt must be in [0, 1], got {likelihood_under_alt}")

        ts = round(time.time() if timestamp is None else timestamp, 3)
        body = json.dumps(
            {
                "datum_id": datum_id,
                "description": description,
                "outcome": outcome,
                "likelihood_under_h": likelihood_under_h,
                "likelihood_under_alt": likelihood_under_alt,
                "timestamp": ts,
            },
            sort_keys=True,
        ).encode("utf-8")
        mac = hmac.new(secret_key, body, hashlib.sha256).hexdigest()

        return Observation(
            datum_id=datum_id,
            description=description,
            outcome=outcome,
            likelihood_under_h=likelihood_under_h,
            likelihood_under_alt=likelihood_under_alt,
            timestamp=ts,
            origin_mac=mac,
        )

    def verify_origin(self, secret_key: bytes) -> bool:
        body = json.dumps(
            {
                "datum_id": self.datum_id,
                "description": self.description,
                "outcome": self.outcome,
                "likelihood_under_h": self.likelihood_under_h,
                "likelihood_under_alt": self.likelihood_under_alt,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        ).encode("utf-8")
        expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.origin_mac, expected)

    def bayes_factor(self) -> float:
        """Compute Bayes factor K = P(D | H) / P(D | ~H)."""
        denom = max(1e-12, self.likelihood_under_alt)
        return self.likelihood_under_h / denom


@dataclass(frozen=True)
class SurrenderCertificate:
    certificate_id: str
    hypothesis_id: str
    initial_prior: float
    final_posterior: float
    cumulative_bayes_factor: float
    initial_truth_pressure: float
    terminal_truth_pressure: float
    terminal_register: str
    trigger_observation_id: str
    surrender_reason: str
    timestamp: float
    origin_hmac: str

    @staticmethod
    def issue(
        certificate_id: str,
        hypothesis_id: str,
        initial_prior: float,
        final_posterior: float,
        cumulative_bayes_factor: float,
        initial_truth_pressure: float,
        terminal_truth_pressure: float,
        trigger_observation_id: str,
        surrender_reason: str,
        secret_key: bytes,
    ) -> "SurrenderCertificate":
        ts = round(time.time(), 3)
        body = json.dumps(
            {
                "certificate_id": certificate_id,
                "hypothesis_id": hypothesis_id,
                "initial_prior": round(initial_prior, 6),
                "final_posterior": round(final_posterior, 6),
                "cumulative_bayes_factor": round(cumulative_bayes_factor, 6),
                "initial_truth_pressure": round(initial_truth_pressure, 4),
                "terminal_truth_pressure": round(terminal_truth_pressure, 4),
                "terminal_register": EpistemicRegister.FALLS.value,
                "trigger_observation_id": trigger_observation_id,
                "surrender_reason": surrender_reason,
                "timestamp": ts,
            },
            sort_keys=True,
        ).encode("utf-8")
        mac = hmac.new(secret_key, body, hashlib.sha256).hexdigest()

        return SurrenderCertificate(
            certificate_id=certificate_id,
            hypothesis_id=hypothesis_id,
            initial_prior=round(initial_prior, 6),
            final_posterior=round(final_posterior, 6),
            cumulative_bayes_factor=round(cumulative_bayes_factor, 6),
            initial_truth_pressure=round(initial_truth_pressure, 4),
            terminal_truth_pressure=round(terminal_truth_pressure, 4),
            terminal_register=EpistemicRegister.FALLS.value,
            trigger_observation_id=trigger_observation_id,
            surrender_reason=surrender_reason,
            timestamp=ts,
            origin_hmac=mac,
        )

    def verify_certificate(self, secret_key: bytes) -> bool:
        body = json.dumps(
            {
                "certificate_id": self.certificate_id,
                "hypothesis_id": self.hypothesis_id,
                "initial_prior": self.initial_prior,
                "final_posterior": self.final_posterior,
                "cumulative_bayes_factor": self.cumulative_bayes_factor,
                "initial_truth_pressure": self.initial_truth_pressure,
                "terminal_truth_pressure": self.terminal_truth_pressure,
                "terminal_register": self.terminal_register,
                "trigger_observation_id": self.trigger_observation_id,
                "surrender_reason": self.surrender_reason,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        ).encode("utf-8")
        expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.origin_hmac, expected)


@dataclass
class Hypothesis:
    hypothesis_id: str
    title: str
    prior_prob: float
    current_prob: float
    evidence_score: float  # [0, 10]
    explanatory_power: float  # [0, 10]
    epistemic_strain: float  # [0, 10]
    state: HypothesisState
    scope_domain: str
    observations: List[Observation] = field(default_factory=list)
    auxiliary_patches: List[Dict[str, Any]] = field(default_factory=list)
    cumulative_bayes_factor: float = 1.0
    initial_truth_pressure: float = 0.0
    surrender_certificate: Optional[SurrenderCertificate] = None

    def __post_init__(self):
        if not (0.0 < self.prior_prob < 1.0):
            raise ValueError(f"prior_prob must be in (0, 1), got {self.prior_prob}")
        self.initial_truth_pressure = self.truth_pressure()

    def truth_pressure(self) -> float:
        return calculate_truth_pressure(self.evidence_score, self.explanatory_power, self.epistemic_strain)

    def epistemic_register(self) -> EpistemicRegister:
        is_surrendered = (self.state == HypothesisState.SURRENDERED)
        return determine_epistemic_register(self.truth_pressure(), self.evidence_score, is_surrendered)

    def process_observation(
        self,
        obs: Observation,
        secret_key: bytes,
    ) -> Tuple[HypothesisState, Optional[SurrenderCertificate]]:
        """Process an incoming observation and update hypothesis state deterministically."""
        if self.state == HypothesisState.SURRENDERED:
            return self.state, self.surrender_certificate

        if not obs.verify_origin(secret_key):
            raise ValueError(f"Observation {obs.datum_id} failed origin HMAC verification!")

        self.observations.append(obs)
        bf = obs.bayes_factor()
        self.cumulative_bayes_factor *= bf

        # Bayesian update on posterior probability
        prior_odds = self.current_prob / (1.0 - self.current_prob)
        posterior_odds = prior_odds * bf
        self.current_prob = round(posterior_odds / (1.0 + posterior_odds), 6)

        # 1. Check for single decisive falsification (K < 0.01)
        if bf <= 0.01:
            reason = f"Decisive single-trial falsification: Bayes factor K={bf:.6f} <= 0.01 (log penalty {math.log(max(1e-12, bf)):.2f})"
            self.state = HypothesisState.SURRENDERED
            self.surrender_certificate = SurrenderCertificate.issue(
                certificate_id=f"CERT-{self.hypothesis_id}-{len(self.observations)}",
                hypothesis_id=self.hypothesis_id,
                initial_prior=self.prior_prob,
                final_posterior=self.current_prob,
                cumulative_bayes_factor=self.cumulative_bayes_factor,
                initial_truth_pressure=self.initial_truth_pressure,
                terminal_truth_pressure=self.truth_pressure(),
                trigger_observation_id=obs.datum_id,
                surrender_reason=reason,
                secret_key=secret_key,
            )
            return self.state, self.surrender_certificate

        # 2. Check for cumulative Bayesian surrender (cumulative K <= 0.01)
        if self.cumulative_bayes_factor <= 0.01:
            reason = f"Cumulative evidence surrender: cumulative Bayes factor K={self.cumulative_bayes_factor:.6f} <= 0.01"
            self.state = HypothesisState.SURRENDERED
            self.surrender_certificate = SurrenderCertificate.issue(
                certificate_id=f"CERT-{self.hypothesis_id}-{len(self.observations)}",
                hypothesis_id=self.hypothesis_id,
                initial_prior=self.prior_prob,
                final_posterior=self.current_prob,
                cumulative_bayes_factor=self.cumulative_bayes_factor,
                initial_truth_pressure=self.initial_truth_pressure,
                terminal_truth_pressure=self.truth_pressure(),
                trigger_observation_id=obs.datum_id,
                surrender_reason=reason,
                secret_key=secret_key,
            )
            return self.state, self.surrender_certificate

        # 3. Anomaly detection (0.01 < bf < 0.20): increase strain, drop evidence
        if bf < 0.20:
            strain_increase = min(8.0, -math.log(bf))
            self.epistemic_strain = min(10.0, self.epistemic_strain + strain_increase)
            self.evidence_score = max(0.5, self.evidence_score - 1.5)
            self.state = HypothesisState.CHALLENGED

            # Check if Truth Pressure collapsed below conjecture threshold
            if self.truth_pressure() < 2.50:
                reason = f"Truth pressure collapse: Pi={self.truth_pressure():.4f} < 2.50 under accumulated anomaly strain"
                self.state = HypothesisState.SURRENDERED
                self.surrender_certificate = SurrenderCertificate.issue(
                    certificate_id=f"CERT-{self.hypothesis_id}-{len(self.observations)}",
                    hypothesis_id=self.hypothesis_id,
                    initial_prior=self.prior_prob,
                    final_posterior=self.current_prob,
                    cumulative_bayes_factor=self.cumulative_bayes_factor,
                    initial_truth_pressure=self.initial_truth_pressure,
                    terminal_truth_pressure=self.truth_pressure(),
                    trigger_observation_id=obs.datum_id,
                    surrender_reason=reason,
                    secret_key=secret_key,
                )
                return self.state, self.surrender_certificate

        # 4. Supportive observation (bf > 1.0)
        elif bf > 1.0:
            self.evidence_score = min(10.0, self.evidence_score + min(2.0, math.log(bf)))
            self.epistemic_strain = max(0.0, self.epistemic_strain - 0.5)

            # Evaluate promotions
            pi = self.truth_pressure()
            if self.state in (HypothesisState.PROPOSED, HypothesisState.TENTATIVE, HypothesisState.CHALLENGED):
                if pi >= 18.0 and self.evidence_score >= 7.5:
                    self.state = HypothesisState.CONFIRMED_MEASURED
                elif pi >= 12.0 and self.evidence_score >= 5.5:
                    self.state = HypothesisState.CONFIRMED_DERIVED
                elif pi >= 5.0:
                    self.state = HypothesisState.TENTATIVE

        return self.state, None

    def attempt_auxiliary_patch(
        self,
        patch_id: str,
        description: str,
        complexity_cost: float,
        independent_evidence: float,
        secret_key: bytes,
    ) -> bool:
        """Attempt to preserve the hypothesis via an auxiliary assumption (Duhem-Quine defense).

        If independent_evidence == 0 (ad-hoc excuse), complexity cost inflates epistemic strain
        without compensation, forcing Truth Pressure downward. If Truth Pressure falls below
        2.50, surrender is immediately forced.
        """
        if self.state == HypothesisState.SURRENDERED:
            return False

        self.auxiliary_patches.append({
            "patch_id": patch_id,
            "description": description,
            "complexity_cost": complexity_cost,
            "independent_evidence": independent_evidence,
        })

        # Apply complexity cost to strain
        self.epistemic_strain = min(10.0, self.epistemic_strain + complexity_cost)
        if independent_evidence > 0:
            self.evidence_score = min(10.0, self.evidence_score + independent_evidence)

        # Check if anti-immunization threshold is triggered
        if self.truth_pressure() < 2.50:
            reason = f"Anti-immunization rule triggered: auxiliary patch {patch_id} inflated strain to {self.epistemic_strain:.2f}, collapsing Pi to {self.truth_pressure():.4f} < 2.50"
            self.state = HypothesisState.SURRENDERED
            self.surrender_certificate = SurrenderCertificate.issue(
                certificate_id=f"CERT-{self.hypothesis_id}-IMMUNIZATION-{patch_id}",
                hypothesis_id=self.hypothesis_id,
                initial_prior=self.prior_prob,
                final_posterior=self.current_prob,
                cumulative_bayes_factor=self.cumulative_bayes_factor,
                initial_truth_pressure=self.initial_truth_pressure,
                terminal_truth_pressure=self.truth_pressure(),
                trigger_observation_id=patch_id,
                surrender_reason=reason,
                secret_key=secret_key,
            )
            return False

        return True

    def narrow_scope(
        self,
        new_subdomain: str,
        justification: str,
        residual_strain: float = 1.0,
    ) -> bool:
        """Narrow hypothesis scope to an unaffected sub-domain where anomalies do not apply."""
        if self.state == HypothesisState.SURRENDERED:
            return False

        self.scope_domain = new_subdomain
        self.state = HypothesisState.NARROWED
        self.epistemic_strain = max(0.5, residual_strain)
        return True


# ─── 5. BRIER SCORE CALIBRATION & SURRENDER PENALTY ──────────────────────────

def compute_brier_score(forecasts: Sequence[float], outcomes: Sequence[int]) -> float:
    """Compute empirical Brier score: B = (1/N) * sum((f_i - o_i)^2)."""
    if len(forecasts) != len(outcomes) or len(forecasts) == 0:
        raise ValueError("Forecasts and outcomes must have identical non-zero length")
    return sum((f - o) ** 2 for f, o in zip(forecasts, outcomes)) / len(forecasts)


def simulate_obstinate_vs_revising_agent(
    initial_prior: float,
    observations: Sequence[Observation],
    secret_key: bytes = b"simulation-key-2026",
) -> Dict[str, Any]:
    """Compare a rational Bayesian revising agent against an obstinate non-revising agent.

    Proves that refusing to revise hypothesis confidence imposes a heavy Brier penalty
    and inflates calibration error (Murphy reliability).
    """
    secret = secret_key
    revising_hypo = Hypothesis(
        hypothesis_id="H-REVISE",
        title="Revising Agent Hypothesis",
        prior_prob=initial_prior,
        current_prob=initial_prior,
        evidence_score=8.0,
        explanatory_power=8.5,
        epistemic_strain=1.0,
        state=HypothesisState.CONFIRMED_MEASURED,
        scope_domain="Universal",
    )

    revising_forecasts: List[float] = []
    obstinate_forecasts: List[float] = []
    actual_outcomes: List[int] = []

    for obs in observations:
        revising_forecasts.append(revising_hypo.current_prob)
        obstinate_forecasts.append(initial_prior)
        actual_outcomes.append(obs.outcome)

        revising_hypo.process_observation(obs, secret)

    brier_revising = compute_brier_score(revising_forecasts, actual_outcomes)
    brier_obstinate = compute_brier_score(obstinate_forecasts, actual_outcomes)
    brier_penalty = brier_obstinate - brier_revising

    return {
        "n_trials": len(observations),
        "revising_final_prob": revising_hypo.current_prob,
        "revising_final_state": revising_hypo.state.value,
        "revising_brier": round(brier_revising, 6),
        "obstinate_brier": round(brier_obstinate, 6),
        "brier_penalty": round(brier_penalty, 6),
        "obstinate_brier_inflation_ratio": round(brier_obstinate / max(1e-6, brier_revising), 2),
    }


if __name__ == "__main__":
    print("Hypothesis Surrender Engine Loaded.")
