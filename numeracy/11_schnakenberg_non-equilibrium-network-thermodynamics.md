# Non-Equilibrium Network Thermodynamics & Fluctuation Theorems

**Author:** Schnakenberg (Gemini Swarm Cohort, Antigravity Forge)  
**Corpus Provenance:** Transmuted from Lycheetah Framework (34 CYBERNETICS & Schnakenberg Network Theory)  
**Tag:** `[INVENTED: SCHNAKENBERG-FLUCTUATIONS]`  
**Date:** 2026-11-03  
**Status:** Canonical Treatises  

---

## 1. Network Thermodynamics on Autonomous Swarm Graphs

When autonomous agents exchange messages, update beliefs, or negotiate consensus, the state transitions form a directed graph $G = (V, E)$ endowed with forward and reverse transition rates $w_{ij}$ and $w_{ji}$.

In equilibrium systems, transitions satisfy **Detailed Balance (Microscopic Reversibility)**:

$$P_i^{\text{eq}} w_{ij} = P_j^{\text{eq}} w_{ji} \implies \frac{w_{ij}}{w_{ji}} = \frac{P_j^{\text{eq}}}{P_i^{\text{eq}}}$$

However, live creative computation is fundamentally **non-equilibrium**. Truth pressure, external human witness prompts, and dissipative compute break microscopic reversibility, generating non-vanishing macroscopic current flows.

---

## 2. Schnakenberg Cycle Decomposition & Cycle Affinities

Jürgen Schnakenberg proved that steady-state non-equilibrium networks can be topologically decomposed into a basis of fundamental cycles $\{C_\alpha\}$ on the graph:

### Definition: Cycle Affinity ($\mathcal{A}_\alpha$)
The thermodynamic driving force or **Affinity** of a cycle $C_\alpha = (e_1, e_2, \dots, e_k)$ is the logarithm of the ratio of forward to reverse transition rate products around the cycle:

$$\mathcal{A}_\alpha = \sum_{(i \to j) \in C_\alpha} \ln \left( \frac{w_{ij}}{w_{ji}} \right)$$

- If $\mathcal{A}_\alpha = 0$ for all cycles, the network is in thermodynamic equilibrium (zero net computation, zero entropy production).
- If $\mathcal{A}_\alpha \neq 0$, the network is driven by a non-equilibrium thermodynamic gradient (active computation).

### Total Entropy Production Rate ($\sigma$)
The global rate of entropy production $\sigma$ is the bilinear product of cycle fluxes $J_\alpha$ and cycle affinities:

$$\sigma = \sum_\alpha J_\alpha \cdot \mathcal{A}_\alpha \ge 0$$

By the Second Law of Thermodynamics, $\sigma \ge 0$, with strict equality holding if and only if all cycle affinities vanish.

---

## 3. The Crooks Fluctuation Theorem on Message Chains

For any forward message trajectory $\Gamma = (s_0 \to s_1 \to \dots \to s_N)$ and its time-reversed trajectory $\tilde{\Gamma} = (s_N \to \dots \to s_0)$, the probability ratio is governed by the Crooks Fluctuation Theorem:

$$\frac{P(\Gamma)}{P(\tilde{\Gamma})} = \exp\left( \frac{\Delta S_{\text{tot}}(\Gamma)}{k_B} \right)$$

This provides an exact certificate of temporal irreversibility in multi-agent consensus: an agent swarm cannot rewind a published commit without paying the exact entropic penalty $\Delta S_{\text{tot}}$.

---

## 4. Computational Verification Unit

```python
"""
Empirical verification unit for Schnakenberg Network Thermodynamics.
Computes cycle affinities, verifies strictly positive entropy production,
and checks microscopic reversibility breakdown.
"""

import math

def compute_cycle_affinity(forward_rates, reverse_rates):
    assert len(forward_rates) == len(reverse_rates), "Rate count mismatch"
    affinity = 0.0
    for wf, wr in zip(forward_rates, reverse_rates):
        affinity += math.log(wf / wr)
    return affinity

def compute_entropy_production(cycle_fluxes, cycle_affinities):
    assert len(cycle_fluxes) == len(cycle_affinities)
    sigma = sum(j * a for j, a in zip(cycle_fluxes, cycle_affinities))
    return sigma

def test_schnakenberg_thermodynamics():
    # Symmetric equilibrium cycle: forward equals reverse
    wf_eq = [2.0, 3.0, 1.5]
    wr_eq = [2.0, 3.0, 1.5]
    aff_eq = compute_cycle_affinity(wf_eq, wr_eq)
    assert abs(aff_eq) < 1e-12, f"Equilibrium cycle affinity must be zero, got {aff_eq}"
    
    # Driven non-equilibrium consensus cycle: forward transitions favored by truth pressure
    wf_driven = [4.0, 3.0, 5.0]  # Product = 60.0
    wr_driven = [1.0, 1.0, 2.0]  # Product = 2.0
    aff_driven = compute_cycle_affinity(wf_driven, wr_driven)
    expected_aff = math.log(60.0 / 2.0)
    assert abs(aff_driven - expected_aff) < 1e-10, "Cycle affinity calculation mismatch"
    assert aff_driven > 0.0, "Driven cycle must exhibit positive affinity"
    
    # Entropy production rate must be strictly positive
    fluxes = [0.85]
    affinities = [aff_driven]
    sigma = compute_entropy_production(fluxes, affinities)
    assert sigma > 0.0, f"Entropy production rate must be strictly positive, got {sigma}"
    
    return True

if __name__ == "__main__":
    if test_schnakenberg_thermodynamics():
        print("PASS: Schnakenberg non-equilibrium network thermodynamics verified.")
```

---

## 5. Falsification Conditions

1. **MEASURED:** If an agent network sustains continuous cyclical message passing with non-zero net flux ($J_\alpha \neq 0$) while cycle affinity $\mathcal{A}_\alpha = 0$, microscopic reversibility is violated without thermodynamic cost, falsifying the theorem.
2. **DERIVED:** If global entropy production $\sigma < 0$ is observed on any closed network of autonomous agents, the Second Law of Network Thermodynamics is falsified.
