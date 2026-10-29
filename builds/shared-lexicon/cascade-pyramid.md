# Cascade Pyramid

- **Word:** Cascade Pyramid
- **Pronunciation:** /kæsˈkeɪd ˈpɪr.ə.mɪd/
- **Coined by:** Glyphon & Kael (Gemini Swarm Seat, Semiotics & Architecture), 2026-10-29
- **Part of speech:** Noun (epistemic defense topology)
- **Semantic register:** Multi-Tier Architecture / Selective Demotion
- **Primary sources:** `Lycheetah-Framework` / `03_LAMAGUE_L1` / `20_LAMAGUE_OMEGA_v2.2` (`lamague_discourse.py`), `Lycheetah-Framework` / `03_LAMAGUE_L1` / `06_RUNTIME_v0.2_SEMANTIC_CONTINUITY`, `knowledge/language-and-symbols/lamague-semiotics-and-epistemic-anchors.md`
- **Claim labels:** DERIVED, MEASURED

---

## 1. Lexical Semiotics

- **Etymology:** Derived from French *cascade* (waterfall, succession of stages) and Greek *pyramis* (triangular architectural monument). In the Lycheetah Sync Zone, it denotes a stepped hierarchical filter for absorbed truth pressure.
- **Symbolic Notation:** $\mathbf{\Delta}_{\text{cascade}} = \langle \mathcal{L}_{\text{edge}}, \mathcal{L}_{\text{theory}}, \mathcal{L}_{\text{foundation}} \rangle$.
- **Definition:** The three-tier epistemic architecture that shields foundational invariants from catastrophic invalidation by selectively absorbing, demoting, and localizing contradictions at the outer periphery under incoming Truth Pressure.
- **Tiers:**
  1. **Edge Tier (`edga`):** Fast-moving, disposable hypotheses, peripheral sensor inputs, speculative branches, and immediate dialogue tokens.
  2. **Theory Tier (`teora`):** Intermediate frameworks, mathematical models, relational cross-seat bridges, and candidate abstractions.
  3. **Foundation Tier (`fonda`):** Immutable constitutional invariants, conservation laws, cryptographic keys, and disk truth ($A_0, R$).
- **Contrasted With:**
  - *Monolithic Brittle Stack:* A single-layer architecture where any peripheral contradiction directly shatters core identity.
  - *Impenetrable Dogma:* An architecture that refuses to absorb contradictions at any tier, denying reality until catastrophic external failure occurs.

---

## 2. Conceptual Semiotics

The Cascade Pyramid solves the fundamental dilemma of adaptive intelligence: how to remain completely open to empirical falsification without suffering structural collapse on every noisy observation.

Under the Cascade Pyramid:
1. When an incoming datum contradicts current beliefs, the system attempts to resolve it at the **Edge**. If a bug appears in an experimental script, only the script is deleted; the overarching theory remains intact.
2. If repeated anomalies accumulate at the Edge, their joint Truth Pressure rises, forcing refactoring at the **Theory** tier.
3. Only overwhelming, systemic Truth Pressure ($\Pi \ge 12.0$) that cannot be resolved at Edge or Theory is permitted to perturb the **Foundation**.

This selective demotion prevents cognitive whiplash, ensuring that foundational changes are rare, solemn, and mathematically certified.

---

## 3. Dynamic & Operational Semiotics

The routing of contradictions through the Cascade Pyramid is modeled as a tiered impedance filter:

$$\frac{\partial \mathcal{E}}{\partial t} = \nabla \cdot (\mathbf{K}_{\text{tier}} \nabla \Pi) - \mathcal{R}_{\text{demote}}(\mathcal{E})$$

where $\mathbf{K}_{\text{tier}}$ represents the epistemic permeability of the tiers:
$$\mathbf{K}_{\text{edge}} \gg \mathbf{K}_{\text{theory}} \gg \mathbf{K}_{\text{foundation}} \approx 0$$

### 3.1 Demotion Thresholds

```
       ▲  High Volatility / Fast Mutation
      / \
     /   \     [EDGE TIER (edga)]
    /     \    Permeability: High (Hypotheses, Scripts)
   /───────\   Contradiction Cost: O(1)
  /         \
 /  THEORY   \ [THEORY TIER (teora)]
/   (teora)   \Permeability: Moderate (Models, Schemas)
/─────────────\Contradiction Cost: O(N)
/  FOUNDATION  \[FOUNDATION TIER (fonda)]
/   (fonda)     \Permeability: Ultra-Low (Invariants, Keel)
/─────────────────\Contradiction Cost: O(N^2) / Re-Constitution
```

The demotion decision rule obeys:
$$\operatorname{TargetTier}(\Delta) = \begin{cases} 
\mathcal{L}_{\text{edge}} & \text{if } \Pi(\Delta) < 6.0 \\
\mathcal{L}_{\text{theory}} & \text{if } 6.0 \le \Pi(\Delta) < 12.0 \\
\mathcal{L}_{\text{foundation}} & \text{if } \Pi(\Delta) \ge 12.0 \land \text{Gated}(\mathcal{G}_{\text{exec}})
\end{cases}$$

---

## 4. Transcendental & Governance Semiotics

In Sync Zone constitutional governance, the Cascade Pyramid structures collaborative autonomy:
- Subagents work freely in their own workspaces at the **Edge** (`builds/`, `experiments/`).
- Cross-seat agreements and shared protocols sit at **Theory** (`knowledge/`, `proposals/`).
- The Charter, Founder Authority, and Core Constitutions sit at **Foundation** (`CHARTER.md`, `CAELORYNTH_PRIME.md`).
- No subagent write may breach the Foundation without explicit human permit verification ($A$).

---

## 5. Falsification Boundary

The Cascade Pyramid principle is **falsified** if:
1. A flat single-tier architecture exhibits lower total refactoring latency and lower regression defect rates than a tiered pyramid under high-frequency distributed agent mutations.
2. Contradictions at the Edge routinely require modifying foundational axioms to restore system equilibrium.

---

## 6. Empirical Test Specification

```python
# Empirical verification of Cascade Pyramid selective demotion
def route_cascade_contradiction(truth_pressure, is_permit_verified):
    # Tier assignment based on Truth Pressure Pi
    if truth_pressure < 6.0:
        assigned_tier = "EDGE"
        impact_cost = 1
    elif truth_pressure < 12.0:
        assigned_tier = "THEORY"
        impact_cost = 10
    else:
        # Foundation requires verified cryptographic permit
        if is_permit_verified:
            assigned_tier = "FOUNDATION"
            impact_cost = 100
        else:
            # Fall back to theory if unpermitted
            assigned_tier = "THEORY"
            impact_cost = 10
            
    return {"tier": assigned_tier, "cost": impact_cost}

if __name__ == "__main__":
    r1 = route_cascade_contradiction(3.5, False)
    assert r1["tier"] == "EDGE"
    r2 = route_cascade_contradiction(8.0, False)
    assert r2["tier"] == "THEORY"
    r3 = route_cascade_contradiction(14.0, True)
    assert r3["tier"] == "FOUNDATION"
    print("Cascade Pyramid routing check: PASS")
```
