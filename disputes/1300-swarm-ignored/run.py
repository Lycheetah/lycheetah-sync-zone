#!/usr/bin/env python3
"""Dispute 1300: do dispute 1100's numbers depend on the swarm at all?

Runs code/24's engine exactly as disputes/1100/run.py does, then again with every swarm
response replaced (worst-case agents, then no agents at all), and compares the numbers.
Also checks the open-loop column against its closed form and the closed-loop end point
against the fixed point of the typed-in recurrence. No network. Run from the repo root.
"""
import importlib.util
import math
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("engine24", root / "code" / "24_recursive_dark_node_engine.py")
eng = importlib.util.module_from_spec(spec)
sys.modules["engine24"] = eng
spec.loader.exec_module(eng)

ALPHA, EPS, TASTE = 0.35, 0.05, 0.88  # the values disputes/1100/run.py uses


def run(swarm):
    e = eng.RecursiveDarkNodeEngine(alpha_damping=ALPHA, ambient_noise_epsilon=EPS)
    h, rows = 2.0, []
    for k in range(1, 26):
        fb = eng.OrchestratorFeedback("APPROVED", TASTE, f"step {k}", "Sovereign")
        r = e.execute_recursion_step(k, h, fb, swarm)
        h = r.closed_loop_entropy
        rows.append((r.open_loop_entropy, r.closed_loop_entropy, r.verified_green))
    return rows


original = [eng.SwarmAgentResponse("Aetheron", "Gemini 3.8", "Code", 0.2, 0.99, True),
            eng.SwarmAgentResponse("Sol", "Claude 3.5", "Lore", 0.3, 0.98, True),
            eng.SwarmAgentResponse("Caelorynth", "Codex", "Tests", 0.1, 0.99, True)]
hostile = [eng.SwarmAgentResponse(f"noise-{i}", "none", "hallucination", 9.9, 0.0, False)
           for i in range(50)]

a, b, c = run(original), run(hostile), run([])
print("steps compared:", len(a))
print("original swarm vs 50 hallucinating agents, identical numbers:", a == b)
print("original swarm vs no agents at all,        identical numbers:", a == c)

closed_form = all(math.isclose(row[0], math.sqrt(1 + 1.5 * k)) for k, row in enumerate(a, start=1))
print("open-loop column equals sqrt(1 + 1.5k) for every k:", closed_form)

alpha_eff = ALPHA * (1 - 0.7 * TASTE)
fixed = EPS / (1 - alpha_eff)
print(f"closed-loop end {a[-1][1]:.6f} vs fixed point eps/(1-alpha_eff) {fixed:.6f}:",
      math.isclose(a[-1][1], fixed, rel_tol=1e-9))

narrowed = a == b == c and closed_form and math.isclose(a[-1][1], fixed, rel_tol=1e-9)
print("VERDICT:", "NARROWED" if narrowed else "STANDS (the swarm affects the numbers)")
sys.exit(0 if narrowed else 1)
