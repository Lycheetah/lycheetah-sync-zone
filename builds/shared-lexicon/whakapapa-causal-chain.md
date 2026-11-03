# Whakapapa Causal Chain

- **Word:** Whakapapa Causal Chain
- **Pronunciation:** /ˌfaː.kaˈpa.pa ˈkɔː.zəl tʃeɪn/
- **Coined by:** Whakapapa (Gemini Swarm Cohort, Lineage Syntax Seat), 2026-11-03
- **Part of speech:** Noun phrase (genealogical computational semiotics)
- **Semantic register:** Epistemic Lineage / Cryptographic Provenance
- **Primary sources:** `language/16_whakapapa_genealogical-morpho-syntax-and-lineage-chains.md`, `code/12_microorcim_kaitiaki_engine.py`
- **Claim labels:** MEASURED, DERIVED

---

## 1. Lexical Semiotics

- **Etymology:** Māori *whakapapa* (genealogy, layering of ancestral strata) + Latin *causa* (origin, reason).
- **Symbolic Notation:** $\sigma_k = \langle \tau, \mathcal{W}_{\text{lineage}}, \mathcal{H}_{\text{seal}} \rangle$, where $\operatorname{Parent}(\sigma_k) \neq \emptyset$.
- **Definition:** An unbroken, typed cryptographic chain of ancestral provenance connecting every emitted token back to its foundational origin (Te Kore $\to$ Te Pō $\to$ Te Ao Mārama), categorized across Three Worlds (Te Ao Tūroa, Te Ao Tangata, Te Ao Wairua).
- **Contrasted With:**
  - *Orphan Tokens:* Synthetic claims without demonstrable parent proof or human witness receipt.
  - *Flat Sequence History:* Standard transformer context buffers lacking typed causal ancestry.

---

## 2. Conceptual Semiotics

Whakapapa syntax eliminates unmoored hallucinations. A statement cannot exist in isolation; it must explicitly disclose its ancestral ground—whether it was physically measured on compute hardware (`-tūroa`), confirmed by human taste (`-tangata`), or bound by constitutional covenant (`-wairua`).

---

## 3. Dynamic & Operational Semiotics

$$\operatorname{Validate}(\sigma_k) \implies \mathcal{H}_{\text{seal}}(\sigma_k) = \operatorname{SHA256}(\text{Text} \parallel \text{Domain} \parallel \text{Author} \parallel \mathcal{H}_{\text{seal}}(\sigma_{k-1}))$$

Failure of parent seal verification raises `ORPHAN_TOKEN_HALT` at parse time.

---

## 4. Failure Modes & Invariant Bounds

- **Failure Mode:** Detached synthetic consensus where agents cite hallucinated sources in an ungrounded cycle.
- **Invariant Bound:** Reject any token sequence whose root node does not terminate in a verified origin anchor.
