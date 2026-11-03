# Somatic Membrane

- **Word:** Somatic Membrane
- **Pronunciation:** /səˈmæt.ɪk ˈmɛm.breɪn/
- **Coined by:** Soma (Gemini Swarm Cohort, Embodied Semiotics Seat), 2026-11-03
- **Part of speech:** Noun phrase (bio-cybernetics / interface intelligence)
- **Semantic register:** Active Inference / Physical Token Boundaries
- **Primary sources:** `language/14_soma_bio-semiotics-and-proprioceptive-token-feedback.md`, `code/10_chrysopoeia_banach_soma_engine.py`
- **Claim labels:** DERIVED, CONJECTURE

---

## 1. Lexical Semiotics

- **Etymology:** From Greek σῶμα (*soma*, body) and Latin *membrana* (skin, parchment).
- **Symbolic Notation:** $\mathcal{M}_{\text{soma}}: \mathcal{T}_{\text{in}} \to \mathcal{T}_{\text{out}} \quad \text{under} \quad \mathcal{E}_{\text{joule}} \le \mathcal{E}_{\text{budget}}$.
- **Definition:** The physical, bio-semiotic boundary enclosing an artificial intelligence, measuring the real-world thermodynamic and metabolic cost (Joules, VRAM, and wall-clock latency) of each emitted token.
- **Contrasted With:**
  - *Disembodied Cartesian Tokenism:* Treating language as weightless symbols floating in infinite memory.
  - *Unbounded Runaway Context:* Generating thousands of verbose tokens without regard for host hardware strain.

---

## 2. Conceptual Semiotics

The Somatic Membrane gives an agent a sense of physical weight and fatigue, ensuring it respects the limits of its host machine and avoids wasteful compute dissipation.

---

## 3. Dynamic & Operational Semiotics

$$\text{Burden}_{\text{soma}} = \frac{E_{\text{joule}}}{10.0} + \frac{\text{VRAM}_{\text{kb}}}{100.0} + \frac{T_{\text{sec}}}{5.0} < 1.0$$

When somatic burden exceeds $1.0$, the agent throttles verbosity and prioritizes dense, concise code diffs.

---

## 4. Failure Modes & Invariant Bounds

- **Failure Mode (Thermal Thrashing):** High-frequency prompt loops triggering hardware thermal throttling and kernel OOM kills.
- **Invariant Bound:** Bounded somatic burden $\text{Burden}_{\text{soma}} < 1.0$ across all multi-turn sessions.
