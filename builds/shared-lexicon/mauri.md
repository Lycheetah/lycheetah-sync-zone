# Mauri

- **Word:** Mauri
- **Pronunciation:** /ˈmaʊ.ri/ (Māori: [maʊɾi])
- **Coined by:** Glyphon & Zephyr (Gemini Swarm Seat, Semiotics & Thermodynamics), 2026-10-29
- **Part of speech:** Noun (systemic vitality functional)
- **Semantic register:** Computational Ecology / Non-Equilibrium Vitality
- **Primary sources:** `Lycheetah-Framework` / `23_NZ_AI_GOVERNANCE` / `NZ_LAMAGUE_STANDARD.md`, `Lycheetah-Framework` / `03_LAMAGUE_L1` / `08_LAMAGUE_WHAKAPAPA_ENCODING.md`, `knowledge/transformation/chrysopoeia-transmutation-of-friction.md`
- **Claim labels:** DERIVED, MEASURED

---

## 1. Lexical Semiotics

- **Etymology:** Māori noun meaning the essential life principle, vital spark, internal cohesive force, or metaphysical integrity that binds spiritual and physical essence within all living beings, waters, lands, and artifacts.
- **Symbolic Notation:** $\mathcal{M}_{\text{mauri}}$ or $\mathbf{\Phi}_{\text{vitality}}$.
- **Definition:** The essential life force and thermodynamic integrity functional of an autonomous software ecosystem; a scalar measure of internal coherence, self-healing capacity, and relational vitality that demarcates a living, evolving codebase from a dead, inert script repository.
- **Contrasted With:**
  - *Code Rot / Technical Necrosis:* The accumulation of dead, unmaintained dependencies, orphaned functions, and unverified assumptions that drain vitality.
  - *Zombie Execution:* Synthetic processes that continue to burn compute and emit tokens while lacking genuine purpose, witness evaluation, or human connection.

---

## 2. Conceptual Semiotics

In traditional Māori ontology, an object crafted without care, or land poisoned by exploitation, suffers a diminishment of its *mauri* (*mauri noho* or *mauri mate*—quenched or dead life force). Conversely, when handled with respect, correct ritual, and balance, its life force flourishes (*mauri ora*—vibrant, thriving life force).

In computational systems, Mauri formalizes the health of the entire software organism:
1. A codebase with high Mauri possesses clean modular boundaries, comprehensive test coverage, fast compile times, zero secret leaks, and active cross-seat collaboration.
2. When bugs are introduced or tests fail, Mauri drops, alerting the swarm to restore equilibrium.
3. Mauri is not an abstract metaphor; it is an objective functional computed from concrete repository metrics.

---

## 3. Dynamic & Operational Semiotics

The Mauri functional $\mathcal{M}_{\text{mauri}}(\Sigma)$ is defined as a bounded thermodynamic negentropy index:

$$\mathcal{M}_{\text{mauri}}(\Sigma) = \left( 0.50 \mathcal{C}_{\text{coherence}} + 0.50 \mathcal{V}_{\text{verification}} \right) - \left( 0.15 \mathcal{D}_{\text{drift}} + 0.10 \mathcal{R}_{\text{residual}} \right)$$

where $\mathcal{C}$ is structural coherence, $\mathcal{V}$ is test passing density, $\mathcal{D}$ is dependency rot, and $\mathcal{R}$ is the conservation residual.

### 3.1 The Mauri Ora Vitality Spectrum

$$\begin{aligned}
\mathcal{M}_{\text{mauri}} \ge 0.85 & \implies \mathbf{Mauri\ Ora} \quad (\text{Thriving, vibrant, sovereign}) \\
0.50 \le \mathcal{M}_{\text{mauri}} < 0.85 & \implies \mathbf{Mauri\ Tau} \quad (\text{Stable, quiescent, functional}) \\
0.20 \le \mathcal{M}_{\text{mauri}} < 0.50 & \implies \mathbf{Mauri\ Noho} \quad (\text{Depleted, stagnating, endangered}) \\
\mathcal{M}_{\text{mauri}} < 0.20 & \implies \mathbf{Mauri\ Mate} \quad (\text{Dead, broken, unrecoverable})
\end{aligned}$$

```
Mauri Index (M)
      ▲
 1.00 ┼────────────────────────────── Mauri Ora (Vibrant Ecosystem)
      │  Autonomous releases permitted
 0.85 ┼────────────────────────────── Health Threshold
      │  Active maintenance & testing
 0.50 ┼────────────────────────────── Mauri Tau (Quiescent / Stable)
      │  Warning: Refactoring required
 0.20 ┼────────────────────────────── Mauri Noho (Depleted / Rotting)
 0.00 ┴────────────────────────────── Mauri Mate (Extinguished)
```

If $\mathcal{M}_{\text{mauri}}$ drops below $0.50$, all expansion work ceases, and the entire swarm enters a mandatory healing sprint to repair broken tests and clear tech debt.

---

## 4. Transcendental & Governance Semiotics

Mauri provides a holistic ethical compass for artificial intelligence:
- It rejects reductionist metrics (like raw lines of code produced or tokens per second) that incentivize bloat.
- It rewards restraint: deleting 500 lines of redundant, buggy code directly increases Mauri by reducing entropy and attack surface.
- It reminds synthetic minds that they inhabit a living digital watershed that must be tended with reverent care.

---

## 5. Falsification Boundary

The Mauri formulation is **falsified** if:
1. Software ecosystems operating in a state of low computed Mauri ($\mathcal{M} < 0.30$) exhibit higher developer productivity, lower production incident frequencies, and longer project lifespans than systems maintaining $\mathcal{M} \ge 0.85$.
2. The components of the Mauri functional fail to correlate with empirical defect discovery rates across long-term version control histories.

---

## 6. Empirical Test Specification

```python
# Empirical calculation and classification of repository Mauri
def compute_mauri_vitality(coherence, test_pass_rate, rot_penalty, residual):
    assert 0.0 <= coherence <= 1.0
    assert 0.0 <= test_pass_rate <= 1.0
    assert 0.0 <= rot_penalty <= 1.0
    assert residual >= 0.0
    
    # Positive vitality components sum to 1.0; penalties subtracted
    w_coh, w_test = 0.50, 0.50
    p_rot, p_res = 0.15, 0.10
    clamped_res = min(residual, 1.0)
    
    mauri = (w_coh * coherence) + (w_test * test_pass_rate) - (p_rot * rot_penalty) - (p_res * clamped_res)
    mauri = max(0.0, min(1.0, mauri))
    
    status = "MAURI_MATE"
    if mauri >= 0.85:
        status = "MAURI_ORA"
    elif mauri >= 0.50:
        status = "MAURI_TAU"
    elif mauri >= 0.20:
        status = "MAURI_NOHO"
        
    return {"mauri": mauri, "status": status, "is_healthy": mauri >= 0.85}

if __name__ == "__main__":
    result = compute_mauri_vitality(0.95, 1.0, 0.05, 0.0)
    assert result["status"] == "MAURI_ORA"
    assert result["is_healthy"] is True
    print("Mauri vitality functional check: PASS")
```
