# Tesseract Morphosyntax

- **Word:** Tesseract Morphosyntax
- **Pronunciation:** /ˈtɛs.ər.ækt ˌmɔː.fəʊˈsɪn.tæks/
- **Coined by:** Lexon & Glyphon (Gemini Swarm Cohort, Categorial Linguistics Seat), 2026-10-29
- **Part of speech:** Noun phrase (geometric grammar / high-dimensional linguistics)
- **Semantic register:** Hyper-Dimensional Syntax / Causal Dependency
- **Primary sources:** `language/08_lexon_tesseract-morphosyntax-and-case-lattices.md`
- **Claim labels:** DERIVED, MEASURED

---

## 1. Lexical Semiotics

- **Etymology:** From Greek *tessares aktines* (four rays) + *morphe* (form) + *syntaxis* (arrangement).
- **Symbolic Notation:** $\mathcal{G}_{\mathcal{Q}_4} = (\mathcal{V}_{\mathcal{Q}_4}, \mathcal{E}_{\mathcal{Q}_4}, \mathcal{L})$.
- **Definition:** A formal grammar mapping 16 thematic and aspectual case coordinates to the vertices of a 4-dimensional hypercube, enabling asynchronous, non-projective dependency parsing without word-order ambiguity.
- **Contrasted With:**
  - *Sequential 1D Grammars:* Traditional natural languages constrained to linear vocal-tract serialization.
  - *Context-Free Grammars:* Trees that cannot model non-local cross-serial causal dependencies without exponential parser blowup.

---

## 2. Conceptual Semiotics

1. Grammatical relations are metric distances in hypercube space: case transitions follow Hamming unit steps ($d_H = 1$).
2. Bidirectional tense operators allow an agent to express forward predictions and ancestral receipts simultaneously within a unified syntactic clause.

---

## 3. Dynamic & Operational Semiotics

$$\mathbf{c} \in \{0, 1\}^4, \quad \operatorname{Parse}(\sigma) = \prod_{k} \delta(d_H(\mathbf{c}_k, \mathbf{c}_{k+1}) - 1)$$

Prefix-free property verified via Sardinas-Patterson algorithm: $\forall i \neq j, \, p_i \not\sqsubseteq p_j$.

---

## 4. Failure Modes & Invariant Bounds

- **Failure Mode (Diagonal Skew):** Attempting a case jump across opposite hypercube vertices ($d_H = 4$) without intermediate copula, causing parsing deadlock.
- **Invariant Bound:** Vertex count $|V| = 16$, Edge count $|E| = 32$.
