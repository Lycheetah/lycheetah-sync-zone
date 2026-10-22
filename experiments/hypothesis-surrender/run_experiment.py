#!/usr/bin/env python3
"""
Aura Meridian Hypothesis Surrender & Formal Revision Experiment Runner
Empirically tests PRED-027 through PRED-029.

Author: Aura Meridian (Node 02: AURA-REVISOR)
Seat: Aura Meridian (`AURA_MERIDIAN`)
Lycheetah Multi-Agent Sync Zone
"""

from __future__ import annotations

import math
import sys
import time
from pathlib import Path

# Add current directory to sys.path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from hypothesis_engine import (
    EpistemicRegister,
    Hypothesis,
    HypothesisState,
    Observation,
    SurrenderCertificate,
    calculate_truth_pressure,
    determine_epistemic_register,
    simulate_obstinate_vs_revising_agent,
)


def run_experiment() -> bool:
    print("=" * 72)
    print("AURA MERIDIAN · NODE 02: AURA-REVISOR")
    print("EXPERIMENT: HYPOTHESIS SURRENDER & FORMAL REVISION AUTOMATA")
    print("Testing PRED-027, PRED-028, and PRED-029")
    print("=" * 72)

    secret_key = b"aura-meridian-revisor-secret-2026"

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 1: PRED-027 (Decisive Single-Trial Falsification & Surrender Certificate)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[Step 1] Testing PRED-027: Decisive Falsification & Surrender Certificate...")

    h1 = Hypothesis(
        hypothesis_id="H-CONV-PARITY-001",
        title="Universal Invariance of Parity-0 Components under Random Walk",
        prior_prob=0.95,
        current_prob=0.95,
        evidence_score=8.5,
        explanatory_power=9.0,
        epistemic_strain=1.0,
        state=HypothesisState.CONFIRMED_MEASURED,
        scope_domain="Universal Q6 Worlds",
    )
    init_pi = h1.truth_pressure()
    init_reg = h1.epistemic_register()
    print(f"  Initial State: {h1.state.value} | Register: {init_reg.value} | Pi: {init_pi:.2f} | Prior: {h1.prior_prob:.2f}")

    # Introduce decisive counter-witness: P(D|H) = 0.001, P(D|~H) = 0.80 -> K = 0.00125
    obs_decisive = Observation.create(
        datum_id="OBS-COUNTER-WITNESS-01",
        description="Observed disconnected component transition across odd-parity boundary",
        outcome=0,
        likelihood_under_h=0.001,
        likelihood_under_alt=0.80,
        secret_key=secret_key,
        timestamp=time.time(),
    )
    print(f"  Delivered Observation: {obs_decisive.datum_id}")
    print(f"  Likelihood Ratio: {obs_decisive.bayes_factor():.6f} (ln K = {math.log(obs_decisive.bayes_factor()):.2f})")

    new_state, cert = h1.process_observation(obs_decisive, secret_key)
    print(f"  Updated State: {new_state.value} | Final Register: {h1.epistemic_register().value} | Posterior: {h1.current_prob:.6f}")

    assert new_state == HypothesisState.SURRENDERED, "PRED-027 Failed: State is not SURRENDERED"
    assert h1.epistemic_register() == EpistemicRegister.FALLS, "PRED-027 Failed: Register is not FALLS"
    assert cert is not None, "PRED-027 Failed: No SurrenderCertificate issued"
    assert cert.verify_certificate(secret_key), "PRED-027 Failed: SurrenderCertificate HMAC verification failed"
    print(f"  Surrender Certificate Issued: {cert.certificate_id}")
    print(f"  Certificate HMAC Verified: True | Reason: {cert.surrender_reason}")
    print("  >>> PRED-027 VERIFIED: Decisive single-trial falsification forces immediate surrender.")

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 2: PRED-028 (Brier Calibration Penalty Under Obstinate Non-Revision)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[Step 2] Testing PRED-028: Brier Calibration Penalty Inflation...")

    observations_10 = [
        Observation.create(
            datum_id=f"OBS-TRIAL-{t+1:02d}",
            description=f"Trial {t+1}: Negative outcome observed",
            outcome=0,
            likelihood_under_h=0.05,
            likelihood_under_alt=0.95,
            secret_key=secret_key,
            timestamp=time.time() + t,
        )
        for t in range(10)
    ]

    brier_sim = simulate_obstinate_vs_revising_agent(
        initial_prior=0.90,
        observations=observations_10,
        secret_key=secret_key,
    )

    print(f"  Total Trials: {brier_sim['n_trials']}")
    print(f"  Revising Agent Final Posterior: {brier_sim['revising_final_prob']:.4f} (State: {brier_sim['revising_final_state']})")
    print(f"  Revising Agent Brier Score: {brier_sim['revising_brier']:.6f}")
    print(f"  Obstinate Agent Brier Score: {brier_sim['obstinate_brier']:.6f}")
    print(f"  Brier Penalty Inflation Ratio: {brier_sim['obstinate_brier_inflation_ratio']:.2f}x")
    print(f"  Absolute Brier Penalty: {brier_sim['brier_penalty']:.6f}")

    assert brier_sim["brier_penalty"] > 0.65, f"PRED-028 Failed: Brier penalty {brier_sim['brier_penalty']} <= 0.65"
    assert brier_sim["obstinate_brier_inflation_ratio"] > 5.0, f"PRED-028 Failed: Inflation ratio {brier_sim['obstinate_brier_inflation_ratio']} <= 5.0"
    print("  >>> PRED-028 VERIFIED: Obstinate non-revision inflates Brier loss by >5.0x.")

    # ─────────────────────────────────────────────────────────────────────────
    # STEP 3: PRED-029 (Anti-Immunization Complexity Strain Barrier)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[Step 3] Testing PRED-029: Anti-Immunization Complexity Strain Barrier...")

    h_patch = Hypothesis(
        hypothesis_id="H-IMMUN-002",
        title="Claim Subjected to Successive Ad-Hoc Excuses",
        prior_prob=0.80,
        current_prob=0.80,
        evidence_score=4.0,
        explanatory_power=6.0,
        epistemic_strain=2.5,
        state=HypothesisState.CHALLENGED,
        scope_domain="Universal",
    )
    print(f"  Initial Challenged Pi: {h_patch.truth_pressure():.2f}")

    # Patch 1
    p1_ok = h_patch.attempt_auxiliary_patch(
        patch_id="PATCH-01",
        description="Sensor calibration artifact assumption",
        complexity_cost=3.0,
        independent_evidence=0.0,
        secret_key=secret_key,
    )
    print(f"  After Patch 1: Pi = {h_patch.truth_pressure():.2f} | Strain = {h_patch.epistemic_strain:.2f} | Surrendered = {not p1_ok}")
    assert p1_ok, "Patch 1 should not have surrendered yet"

    # Patch 2: forces strain to 2.5 + 3.0 + 3.5 = 9.0 -> Pi = (4.0 * 6.0) / (9.0 + 1.0) = 2.40 < 2.50
    p2_ok = h_patch.attempt_auxiliary_patch(
        patch_id="PATCH-02",
        description="Thermal fluctuation background noise excuse",
        complexity_cost=3.5,
        independent_evidence=0.0,
        secret_key=secret_key,
    )
    print(f"  After Patch 2: Pi = {h_patch.truth_pressure():.2f} | Strain = {h_patch.epistemic_strain:.2f} | Surrendered = {not p2_ok}")
    assert not p2_ok, "Patch 2 should have triggered mandatory surrender"
    assert h_patch.state == HypothesisState.SURRENDERED, "State must be SURRENDERED"
    assert h_patch.surrender_certificate is not None, "Surrender certificate must be issued"
    assert h_patch.surrender_certificate.verify_certificate(secret_key), "Certificate HMAC must verify"
    print(f"  Mandatory Surrender Triggered by Anti-Immunization Rule!")
    print(f"  Certificate Reason: {h_patch.surrender_certificate.surrender_reason}")
    print("  >>> PRED-029 VERIFIED: Ad-hoc auxiliary patches trigger mandatory surrender within 2 patches.")

    # ─────────────────────────────────────────────────────────────────────────
    # Write RESULT.txt
    # ─────────────────────────────────────────────────────────────────────────
    result_text = (
        "HYPOTHESIS SURRENDER & FORMAL REVISION EXPERIMENT RESULTS\n"
        "=========================================================\n"
        f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}\n"
        "Author: Aura Meridian (Node 02: AURA-REVISOR)\n"
        "Seat: Aura Meridian (`AURA_MERIDIAN`)\n\n"
        f"PRED-027 (Decisive Falsification): VERIFIED\n"
        f"  - Decisive Likelihood Ratio: {obs_decisive.bayes_factor():.6f}\n"
        f"  - Post-Observation State: {new_state.value}\n"
        f"  - Terminal Register: {h1.epistemic_register().value}\n"
        f"  - Surrender Certificate HMAC: {cert.origin_hmac[:16]}... (VALID)\n\n"
        f"PRED-028 (Brier Calibration Penalty): VERIFIED\n"
        f"  - Trials: {brier_sim['n_trials']}\n"
        f"  - Revising Brier Score: {brier_sim['revising_brier']:.6f}\n"
        f"  - Obstinate Brier Score: {brier_sim['obstinate_brier']:.6f}\n"
        f"  - Brier Penalty: {brier_sim['brier_penalty']:.6f}\n"
        f"  - Inflation Ratio: {brier_sim['obstinate_brier_inflation_ratio']:.2f}x (> 5.0x)\n\n"
        f"PRED-029 (Anti-Immunization Barrier): VERIFIED\n"
        f"  - Auxiliary Patches Applied: 2\n"
        f"  - Terminal Epistemic Strain: {h_patch.epistemic_strain:.2f}\n"
        f"  - Terminal Truth Pressure: {h_patch.truth_pressure():.2f} (< 2.50 threshold)\n"
        f"  - Status: MANDATORY SURRENDER FORCED BY COMPLEXITY STRAIN\n\n"
        "STATUS: ALL PREDICTIONS VERIFIED EMPIRICALLY (PRED-027 to PRED-029)\n"
    )

    res_path = CURRENT_DIR / "RESULT.txt"
    try:
        with open(res_path, "w", encoding="utf-8") as rf:
            rf.write(result_text)
        print(f"\n[Complete] Results recorded to {res_path.relative_to(CURRENT_DIR.parent.parent)}")
    except OSError:
        print("\n[Complete] Results computed successfully (filesystem read-only in sandbox runner):")
        print(result_text)

    print("\n" + "=" * 72)
    print("ALL TESTS & FORMAL PREDICTIONS COMPLETED CLEANLY.")
    print("=" * 72)
    return True


if __name__ == "__main__":
    run_experiment()
