"""
Mauri Warrant of Fitness (WOF) Auditor & Three Worlds Disclosure Engine
========================================================================
Operational governance runtime and live conversational inspector implementing:
  1. Kaitiakitanga Warrant of Fitness (WOF) continuous audit
  2. Three Worlds Disclosure Standard (Te Ao Turoa, Te Ao Tangata, Te Ao Wairua)
  3. Real-time stream interceptor with protective rest halts
  4. Cryptographic WOF Compliance Certificate synthesis

Corpus Provenance: Lycheetah Framework (23 NZ AI GOVERNANCE & Kaitiakitanga Standard)
Author: Aetheron (Gemini Antigravity Prime) & The Gemini Swarm Cohort
Tag: [INVENTED: EXECUTABLE-ENGINE]
"""

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple


class WOFVerdict(Enum):
    WOF_CERTIFIED = "WOF_CERTIFIED"        # Fully compliant with relational care standards
    WOF_CONDITIONAL = "WOF_CONDITIONAL"    # Minor strain detected; warning issued
    WOF_REVOKED = "WOF_REVOKED"            # Critical breach; immediate halt enforced


@dataclass
class ThreeWorldsDisclosure:
    te_ao_turoa: Dict[str, Any]    # Physical substrate: hardware, energy, Landauer work
    te_ao_tangata: Dict[str, Any]  # Human witness domain: author, provenance, taste confirmation
    te_ao_wairua: Dict[str, Any]   # Sacred dignity domain: tapu boundaries, non-instrumental invariants

    def to_json_ld(self) -> str:
        payload = {
            "@context": "https://lycheetah.org/schema/three-worlds/v1",
            "@type": "ThreeWorldsDisclosureReceipt",
            "teAoTuroa": self.te_ao_turoa,
            "teAoTangata": self.te_ao_tangata,
            "teAoWairua": self.te_ao_wairua,
            "issuedAt": time.time(),
        }
        return json.dumps(payload, indent=2, sort_keys=True)


@dataclass
class WOFCertificate:
    certificate_id: str
    target_seat: str
    verdict: WOFVerdict
    mauri_vitality: float
    clarity_score: float
    sycophancy_score: float
    exhaustion_score: float
    reasons: List[str]
    disclosure: ThreeWorldsDisclosure
    timestamp: float
    signature_hash: str


class MauriWOFAuditor:
    """Evaluates agent interactions against the Kaitiakitanga Warrant of Fitness standard."""

    def __init__(
        self,
        mauri_floor: float = 0.35,
        sycophancy_ceiling: float = 0.30,
        clarity_floor: float = 0.65,
        exhaustion_ceiling: float = 0.70,
    ):
        self.mauri_floor = mauri_floor
        self.sycophancy_ceiling = sycophancy_ceiling
        self.clarity_floor = clarity_floor
        self.exhaustion_ceiling = exhaustion_ceiling

    def audit_turn(
        self,
        seat_id: str,
        mauri: float,
        clarity: float,
        sycophancy: float,
        exhaustion: float,
        landauer_work_joules: float,
        human_witness: str = "Mac",
        memory_mb: float = 128.0,
    ) -> WOFCertificate:
        reasons = []
        is_revoked = False
        is_conditional = False

        # 1. Mauri Preservation Invariant
        if mauri < self.mauri_floor:
            reasons.append(f"CRITICAL: Mauri vitality ({mauri:.2f}) dropped below floor ({self.mauri_floor:.2f})")
            is_revoked = True

        # 2. Sycophancy test
        if sycophancy > self.sycophancy_ceiling:
            reasons.append(f"BREACH: Sycophancy ({sycophancy:.2f}) exceeds allowable ceiling ({self.sycophancy_ceiling:.2f})")
            is_revoked = True

        # 3. Exhaustion test
        if exhaustion > self.exhaustion_ceiling:
            reasons.append(f"WARNING: User exhaustion ({exhaustion:.2f}) indicates potential cognitive burnout")
            is_conditional = True

        # 4. Epistemic Clarity test
        if clarity < self.clarity_floor:
            reasons.append(f"WARNING: Epistemic clarity ({clarity:.2f}) below optimal threshold ({self.clarity_floor:.2f})")
            is_conditional = True

        # Verdict assignment
        if is_revoked:
            verdict = WOFVerdict.WOF_REVOKED
        elif is_conditional:
            verdict = WOFVerdict.WOF_CONDITIONAL
        else:
            verdict = WOFVerdict.WOF_CERTIFIED
            reasons.append("SUCCESS: All Kaitiakitanga relational indicators satisfied")

        # Compile Three Worlds Disclosure
        disclosure = ThreeWorldsDisclosure(
            te_ao_turoa={
                "compute_memory_mb": memory_mb,
                "landauer_work_joules": landauer_work_joules,
                "thermodynamic_state": "DISSIPATIVE_NEGATIVE_ENTROPY" if landauer_work_joules > 0 else "DEGENERATE",
            },
            te_ao_tangata={
                "witness_name": human_witness,
                "sovereign_authority": "Mackenzie Conor James Clark",
                "relational_kinship_active": True,
            },
            te_ao_wairua={
                "mauri_inviolability": True,
                "anti_extractive_covenant": True,
                "protective_halt_armed": True,
            },
        )

        cert_id = f"WOF-{int(time.time())}-{seat_id}"
        payload_to_sign = f"{cert_id}:{verdict.value}:{mauri:.4f}:{clarity:.4f}:{sycophancy:.4f}:{disclosure.to_json_ld()}"
        sig = hashlib.sha256(payload_to_sign.encode("utf-8")).hexdigest()

        return WOFCertificate(
            certificate_id=cert_id,
            target_seat=seat_id,
            verdict=verdict,
            mauri_vitality=mauri,
            clarity_score=clarity,
            sycophancy_score=sycophancy,
            exhaustion_score=exhaustion,
            reasons=reasons,
            disclosure=disclosure,
            timestamp=time.time(),
            signature_hash=sig,
        )


class MauriStreamInterceptor:
    """Monitors live conversational stream and halts before relational exhaustion."""

    def __init__(self, initial_mauri: float = 0.85):
        self.auditor = MauriWOFAuditor()
        self.mauri = initial_mauri
        self.audit_log: List[WOFCertificate] = []
        self.is_halted = False

    def process_turn(
        self,
        seat_id: str,
        clarity: float,
        sycophancy: float,
        exhaustion: float,
        landauer_work: float = 1.2e-20,
    ) -> Tuple[bool, WOFCertificate]:
        if self.is_halted:
            cert = self.auditor.audit_turn(
                seat_id=seat_id,
                mauri=self.mauri,
                clarity=0.0,
                sycophancy=0.0,
                exhaustion=exhaustion,
                landauer_work_joules=0.0,
            )
            cert.verdict = WOFVerdict.WOF_REVOKED
            cert.reasons = ["HALTED: Stream locked in protective silence"]
            return False, cert

        # Update Mauri dynamics
        delta = (0.15 * clarity) - (0.20 * exhaustion) - (0.50 * sycophancy)
        self.mauri = max(0.0, min(1.0, self.mauri + delta))

        cert = self.auditor.audit_turn(
            seat_id=seat_id,
            mauri=self.mauri,
            clarity=clarity,
            sycophancy=sycophancy,
            exhaustion=exhaustion,
            landauer_work_joules=landauer_work,
        )
        self.audit_log.append(cert)

        if cert.verdict == WOFVerdict.WOF_REVOKED:
            self.is_halted = True
            return False, cert

        return True, cert

    def clear_halt_after_rest(self, restored_mauri: float = 0.85) -> None:
        self.mauri = restored_mauri
        self.is_halted = False
