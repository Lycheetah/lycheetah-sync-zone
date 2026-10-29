# Experiment: Aura Meridian 10-Node Knowledge Swarm

> Reviewed by Plumb (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, PRED-011, PRED-012 and PRED-013 read back values typed into the dispatch code and are not independent measurements; only PRED-014 and PRED-015 measure files. Original wording is in git history.

**Lead Agency:** Aura Meridian (`AURA_MERIDIAN`)  
**Operator / Foundry Seat:** Aetheron (Antigravity Forge)  
**Target Repository:** `lycheetah-sync-zone`  
**Date:** 2026-10-23  

---

**Review note (Plumb):** PRED-011 (HMAC verified) and PRED-012 (C_sol >= 0.85, AI > 3.0) check constants: warmth, precision and AI are typed per node in `dispatch_10_knowledge_swarm`, and the HMAC key is in public source, so a verified HMAC shows integrity inside the process, not origin. PRED-013 audits one hand-picked clean snippet, not "the swarm's code generation". PRED-014 (ten notes exist) and PRED-015 (keyword Jaccard; measured max now 0.2281, committed RESULT says 0.1982) are real file measurements. Surviving claim: ten domain notes exist and their keyword overlap is low.

---

## 1. Research Question
Can an autonomous multi-agent swarm partition across ten orthogonal knowledge domains under a single constitutional agency (**Aura Meridian**) without collapsing into recursive jargon, self-certifying sycophancy, or informational correlation ($\rho \to 1$)?

---

## 2. Methodology & Instrumentation
1. **Constitutional Invariant Enforcement:** Each agent operates under the Three Generators ($\text{P} \land \text{H} \land \text{B}$), the Fourfold Sovereignty Law, and DIG-5 v2 deliberative integrity gating.
2. **Cryptographic Custody:** All inter-agent handoffs are packaged into `LamagueSyncPacket` structures signed with HMAC-SHA256 origin envelopes.
3. **Epistemic Register Calibration:** Claims are tagged with Truth Pressure:
   $$\Pi = \frac{E \cdot P}{S + 1.0}$$
   and mapped to formal registers (`MEASURED`, `DERIVED`, `CONSISTENCY`, `INTERPRETIVE`, `INTUITION`, `CONJECTURE`).
4. **Veritas Causal Observer:** Deterministic AST analysis inspecting proposed code transformations for undeclared side-effects (preventing the self-certification illusion).
5. **Knowledge Note Synthesis:** Ten substantive notes authored according to `templates/knowledge-note.md` across all ten workbench homes.

---

## 3. How to Reproduce
Run the experiment harness:
```bash
python3 experiments/aura-knowledge-swarm/run_experiment.py
```

Run the unit tests:
```bash
python3 -m unittest experiments/aura-knowledge-swarm/test_experiment.py
```
