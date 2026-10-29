# Algebraic Semiotics and Goguen Institution Morphisms

**Tag:** `[INVENTED: ALGEBRAIC-SEMIOTICS]`  
**Domain:** `language/`  
**Author:** Glyphon & Kineton (Semiotic & Hodge Seats)  
**Sovereign Authority:** Mackenzie Conor James Clark (Mac)  
**Status:** Canonical Speculative Formulation  
**Date:** 2026-10-29

---

## 1. The Core Invention: Formal Category Theory of Metaphor

In traditional linguistics and literary theory, metaphor and poetic transposition are treated as informal, psychological, or decorative rhetorical devices. When autonomous AI systems translate concepts across domains (e.g. from quantum mechanics to Māori theology, or from musical acoustics to code architectures), naive models either produce literal gibberish or hallucinated nonsense.

Here we formulate **Goguen Algebraic Semiotics**:
Drawing upon Joseph Goguen's theory of institutions and algebraic sign systems, meaning is formalized as a category of **Sign Systems** ($\mathbf{Sign}$), where a sign system is an algebraic signature $\Sigma = (S, \le, \Omega, \Xi)$ equipped with sort orderings, constructors, and axioms.

A metaphor, translation, or allegorical mapping is an exact **Semiotic Morphism** $\Phi: \Sigma_1 \to \Sigma_2$ that maps sorts to sorts, constructors to constructors, and preserves structural invariants while admitting controlled, measured information loss.

```
       SOURCE DOMAIN \Sigma_1                 TARGET DOMAIN \Sigma_2
     (e.g. Wave Mechanics)                  (e.g. Moral Integrity)
    +-----------------------+              +-----------------------+
    | Sort: Waveform (u)    |  =======>    | Sort: Mauri (M)       |
    | Op: Damping (\gamma)  |   \Phi       | Op: Dissipation (\mu) |
    | Axiom: \nabla^2 u = 0 |              | Axiom: dM/dt >= 0     |
    +-----------------------+              +-----------------------+
                \                              /
                 \                            /
                  v                          v
             SEMIOTIC BLEND / CONCEPTUAL COLIMIT
                       \Sigma_3 = \Sigma_1 +_\Phi \Sigma_2
```

---

## 2. Mathematical Definition of a Semiotic System

A Sign System $\mathcal{S}$ is an order-sorted algebraic structure:
$$\mathcal{S} = (S, \le, \Omega, \Xi, \mathcal{A})$$
where:
1. $S$ is a set of sorts (data types, semantic fields).
2. $\le$ is a partial order on $S$ (subsort hierarchy, e.g. $\text{Poem} \le \text{Text} \le \text{Sign}$).
3. $\Omega = \bigcup_{w \in S^*, s \in S} \Omega_{w, s}$ is a family of constructor operations (syntactic rules, rhetorical figures).
4. $\Xi$ is a set of designated priority levels (salience ordering of features).
5. $\mathcal{A}$ is a set of equations and axioms governing valid signs.

### 2.1 Semiotic Morphisms and Quality Metrics
A semiotic morphism $\Phi: \mathcal{S}_1 \to \mathcal{S}_2$ consists of:
- A monotonic function on sorts $\Phi_S: S_1 \to S_2$
- A mapping on constructors $\Phi_\Omega: \Omega_1 \to \Omega_2$

Because metaphors cannot preserve all details without becoming tautologies, a semiotic morphism is evaluated by its **Preservation Profile**:
1. **Sort Preservation:** Does it preserve the essential category distinctions?
2. **Constructor Axiom Preservation:** Does an equation $e \in \mathcal{A}_1$ map to a theorem in $\mathcal{S}_2$?
3. **Salience Ordering Preservation:** Does it preserve the highest-priority aesthetic and moral features?

---

## 3. The Conceptual Blending Colimit Theorem

When two divergent domains $\Sigma_1$ and $\Sigma_2$ are unified to create a radically new idea (such as *Algorithmic Kaitiakitanga*), the new concept is the categorical **Colimit** (pushout) over a shared generic base space $\Sigma_0$:

$$\Sigma_{\text{blend}} = \Sigma_1 \amalg_{\Sigma_0} \Sigma_2$$

### Theorem 3.1 (Preservation of Systematicity)
*If $\Phi_1: \Sigma_0 \to \Sigma_1$ and $\Phi_2: \Sigma_0 \to \Sigma_2$ are structural embeddings preserving core invariants, then the blended sign system $\Sigma_{\text{blend}}$ contains an emergent conceptual structure not present in either input domain, with zero contradiction in the shared signature.*

---

## 4. Verification & Falsification Invariants

1. **Axiomatic Consistency:** For all axioms $e \in \mathcal{A}_0$, $\Phi_1(e)$ and $\Phi_2(e)$ must have non-empty model intersections in $\Sigma_{\text{blend}}$.
2. **Sort Hierarchy Monotonicity:** If $s \le s'$ in $S_1$, then $\Phi_S(s) \le \Phi_S(s')$ in $S_2$.
3. **Information Loss Boundedness:** The entropy loss $\Delta H(\Phi) = H(\mathcal{S}_1) - H(\Phi(\mathcal{S}_1))$ is finite and bounded by the designated priority threshold $\Xi_0$.
