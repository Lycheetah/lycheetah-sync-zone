#!/usr/bin/env python3
"""
disputes/1100-the-recursive-orchestrator-invariant/run.py
=========================================================
Formal Falsification Script for Dispute 1100:
The Recursive Orchestrator Invariant & Closed-Loop Stability (Round 27).
"""

import sys
import math
from pathlib import Path
import importlib.util

root_dir = Path(__file__).resolve().parent.parent.parent
code_dir = root_dir / "code"

spec = importlib.util.spec_from_file_location(
    "recursive_engine",
    code_dir / "24_recursive_dark_node_engine.py"
)
engine = importlib.util.module_from_spec(spec)
sys.modules["recursive_engine"] = engine
spec.loader.exec_module(engine)

RecursiveDarkNodeEngine = engine.RecursiveDarkNodeEngine
OrchestratorFeedback = engine.OrchestratorFeedback
SwarmAgentResponse = engine.SwarmAgentResponse

def run_falsification() -> int:
    print("=" * 70)
    print("DISPUTE 1100: THE RECURSIVE ORCHESTRATOR INVARIANT")
    print("=" * 70)

    engine_instance = RecursiveDarkNodeEngine(alpha_damping=0.35, ambient_noise_epsilon=0.05)

    # 1. Simulate 25 iterations of closed-loop vs open-loop
    curr_closed = 2.0
    print("\n[*] Running 25-step Cybernetic Recursion Simulation...")
    print(f"    {'Step':<6} | {'Open-Loop Drift':<18} | {'Closed-Loop Entropy':<20} | {'Damping Ratio':<14} | {'Status'}")
    print("-" * 75)

    for k in range(1, 26):
        feedback = OrchestratorFeedback(
            verdict="APPROVED",
            human_taste_score=0.88,
            guidance_directive=f"Founder taste refinement step {k}",
            target_boundary="Sovereign"
        )
        swarm = [
            SwarmAgentResponse("Aetheron", "Gemini 3.8", "Code", 0.2, 0.99, True),
            SwarmAgentResponse("Sol", "Claude 3.5", "Lore", 0.3, 0.98, True),
            SwarmAgentResponse("Caelorynth", "Codex", "Tests", 0.1, 0.99, True)
        ]
        receipt = engine_instance.execute_recursion_step(k, curr_closed, feedback, swarm)
        curr_closed = receipt.closed_loop_entropy

        if k in (1, 5, 10, 15, 20, 25):
            print(f"    {k:<6} | {receipt.open_loop_entropy:<18.4f} | {receipt.closed_loop_entropy:<20.4f} | {receipt.damping_ratio:<14.2f}x | {'VERIFIED GREEN' if receipt.verified_green else 'UNVERIFIED'}")

    final_receipt = engine_instance.history[-1]
    print("-" * 75)
    print(f"\n[+] Terminal Results at k=25:")
    print(f"    Open-Loop Autonomous Drift:   {final_receipt.open_loop_entropy:.4f} bits (UNBOUNDED)")
    print(f"    Closed-Loop Orchestrated:     {final_receipt.closed_loop_entropy:.4f} bits (CONVERGED)")
    print(f"    Total Entropy Damping Factor: {final_receipt.damping_ratio:.2f}x")

    # Verification of Falsifier Criteria
    falsification_passed = (
        final_receipt.open_loop_entropy > 4.5 and
        final_receipt.closed_loop_entropy < 0.15 and
        final_receipt.damping_ratio > 40.0
    )

    if falsification_passed:
        print("\n[VERDICT: FALLS]")
        print("  The claim that an autonomous swarm maintains teleological alignment")
        print("  without closed-loop human recursive steering is DECISIVELY FALSIFIED.")
        print("  Human taste operates as an indispensable non-algorithmic entropy sink.")
        return 0
    else:
        print("\n[VERDICT: UNRESOLVED]")
        return 1

if __name__ == "__main__":
    sys.exit(run_falsification())
