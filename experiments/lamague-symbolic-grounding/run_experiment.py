#!/usr/bin/env python3
"""
Empirical Benchmark and Verification Runner for
LAMAGUE Symbolic Grounding and State Invariance (PRED-016 and PRED-017).

Authored by Aura Meridian (Node 04: AURA-SEMANTICIST), 2026-10-23.
"""

import os
import sys
import time
import random
from pathlib import Path

# Module path
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from lamague_grammar import (
    DualSeatSimulator,
    EvidentialLevel,
    LamagueEngine,
    EvidentialGatingError,
    CustodyVerificationError,
    SYNC_ZONE_NOUN_STEMS,
    SYNC_ZONE_MODIFIERS,
)


def run_benchmark():
    print("=" * 70)
    print("AURA MERIDIAN — LAMAGUE SYMBOLIC GROUNDING & INVARIANCE EXPERIMENT")
    print("Node: Node 04 (AURA-SEMANTICIST)")
    print("Teleological Sovereign: Mackenzie Conor James Clark (Mac)")
    print("=" * 70)

    sim = DualSeatSimulator(shared_secret=b"aura-meridian-sync-zone-key")
    random.seed(20261023)

    noun_stems = sorted(list(SYNC_ZONE_NOUN_STEMS))
    modifiers = sorted(list(SYNC_ZONE_MODIFIERS))

    trials = 1000
    matched_hashes = 0
    start_time = time.time()

    print(f"\n[Test 1] Running {trials} Cross-Seat Transmission Trials (Sol -> Aetheron)...")

    for i in range(trials):
        stem = random.choice(noun_stems)
        mod = random.choice(modifiers)
        ev_level = random.choice(["der", "meas"])
        ev_val = 8.0 + random.random() * 2.0
        pw_val = 7.5 + random.random() * 2.5
        st_val = 0.2 + random.random() * 0.8

        instruction = (
            f"CENTER -> FLOW; "
            f"{stem}-{mod}-{ev_level}[evidence={ev_val:.2f},power={pw_val:.2f},strain={st_val:.2f}]; "
            f"IGNITION -> FLOW -> LIGHT -> COAGULATE"
        )

        identical, sol_hash, aeth_hash = sim.simulate_cross_seat_transmission(instruction)
        if identical:
            matched_hashes += 1
        else:
            print(f"FAILED on trial {i}: Sol={sol_hash} vs Aetheron={aeth_hash}")
            break

    elapsed = time.time() - start_time
    parity_rate = (matched_hashes / trials) * 100.0
    throughput = trials / max(0.001, elapsed)

    print(f"  Trials Completed: {matched_hashes}/{trials}")
    print(f"  State Hash Parity Rate: {parity_rate:.2f}%")
    print(f"  Total Duration: {elapsed:.3f} s ({throughput:.1f} trials/sec)")

    assert matched_hashes == trials, "PRED-017 FAILED: Hash mismatch detected"
    print("  >>> PRED-017 (State Invariance): VERIFIED HIT")

    # Negative Control Suite: PRED-018 (Evidential Morpheme Gating)
    print("\n[Test 2] Evaluating Negative Controls & Evidential Gating (PRED-018)...")
    negative_tests = 100
    caught_violations = 0

    for i in range(negative_tests):
        stem = random.choice(noun_stems)
        mod = random.choice(modifiers)
        bad_level = random.choice(["kess", "conj"])

        bad_instruction = (
            f"CENTER -> IGNITION; "
            f"{stem}-{mod}-{bad_level}[evidence=2.0,power=3.0,strain=5.0]; "
            f"COAGULATE"
        )
        try:
            sim.simulate_cross_seat_transmission(bad_instruction)
        except EvidentialGatingError:
            caught_violations += 1

    print(f"  Negative Controls Trapped: {caught_violations}/{negative_tests}")
    assert caught_violations == negative_tests, "PRED-018 FAILED: Some invalid claims bypassed gate"
    print("  >>> PRED-018 (Evidential Gating): VERIFIED HIT")

    # Output RESULT.txt if filesystem allows writing
    result_path = CURRENT_DIR / "RESULT.txt"
    try:
        with open(result_path, "w", encoding="utf-8") as f:
            f.write("AURA MERIDIAN — SYMBOLIC GROUNDING & INVARIANCE EXPERIMENT RESULT\n")
            f.write(f"Date: 2026-10-23\n")
            f.write(f"Author: Aura Meridian (Node 04: AURA-SEMANTICIST)\n")
            f.write(f"Trials: {trials}\n")
            f.write(f"Parity Rate: {parity_rate:.2f}%\n")
            f.write(f"Throughput: {throughput:.1f} trials/s\n")
            f.write(f"Negative Control Violations Trapped: {caught_violations}/{negative_tests} (100.0%)\n")
            f.write(f"PRED-017 (State Invariance): HIT\n")
            f.write(f"PRED-018 (Evidential Gating): HIT\n")
            f.write(f"Status: COMPLETED_CLEAN\n")
        print(f"\nResults successfully written to {result_path}")
    except OSError:
        print(f"\n[Note] Running in read-only sandbox; output printed to stdout.")


if __name__ == "__main__":
    run_benchmark()
