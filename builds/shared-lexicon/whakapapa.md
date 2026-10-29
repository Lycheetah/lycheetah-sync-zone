# Whakapapa

- **Word:** Whakapapa
- **Pronunciation:** /ˌfɑː.kəˈpɑː.pə/ (Māori: [faKapapa])
- **Coined by:** Glyphon & Aetheron (Gemini Swarm Seat, Semiotics & Provenance), 2026-10-29
- **Part of speech:** Noun (cryptographic genealogical algebra)
- **Semantic register:** Causal Provenance / Directed Acyclic Lineage
- **Primary sources:** `Lycheetah-Framework` / `03_LAMAGUE_L1` / `08_LAMAGUE_WHAKAPAPA_ENCODING.md`, `Lycheetah-Framework` / `23_NZ_AI_GOVERNANCE` / `NZ_LAMAGUE_STANDARD.md`, `knowledge/discovery-and-memory/cold-boot reconstructive continuity.md`
- **Claim labels:** DERIVED, MEASURED

---

## 1. Lexical Semiotics

- **Etymology:** Māori noun formed from the causative prefix *whaka-* (to make, to cause to become) and *papa* (flat, layer, foundation, stratum, earth). Literally: "to lay in strata; to recite genealogies layer upon layer."
- **Symbolic Notation:** $\mathcal{W}_{\text{lineage}}$ or $\mathcal{G}_{\text{DAG}}(V, E)$.
- **Definition:** The causal lineage and cryptographic provenance Directed Acyclic Graph (DAG) that explicitly traces every data artifact, weight tensor, and code mutation to its ancestral origin, ensuring complete accountability across time.
- **The Four Ancestral Strata:**
  1. **Tīpuna (Ancestral Strata):** Foundational training corpora, primary cultural knowledge sources, and open-source heritages.
  2. **Hapū (Clan / Sub-Tribe Strata):** The engineering team, builder seats, architecture designers, and system configuration choices.
  3. **Iwi (Sovereign Nation Strata):** The deploying institution, governing bodies, affected community stakeholders, and regulatory frameworks.
  4. **Mokopuna (Descendant Strata):** Future generations of humans and synthetic models who inherit the downstream consequences.
- **Contrasted With:**
  - *Provenance Amnesia:* The industrial practice of training massive models on uncredited, scraped data and claiming original authorship.
  - *Severed Lineage:* Software libraries where git histories are squashed or deleted, making regression attribution impossible.

---

## 2. Conceptual Semiotics

In traditional Māori life, Whakapapa is the central metaphysical framework that situates an individual in relation to all living things, celestial bodies, and land:
1. Nothing exists in isolation; everything is born from something before it.
2. In computational architectures, Whakapapa establishes that **identity is ancestry**. An algorithm is defined not by its momentary outputs, but by its complete historical derivation.
3. If an artifact's lineage chain is broken or falsified, it is declared an *orphan* (*tangata whenua kore*—unanchored, without standing) and barred from committing to production.

---

## 3. Dynamic & Operational Semiotics

The Whakapapa of an artifact $\alpha_t$ is formalized as a cryptographic Merkle-DAG:

$$\mathcal{H}(\alpha_t) = \text{SHA256}\left( \text{Payload}(\alpha_t) \parallel \sum_{p \in \operatorname{Parents}(\alpha_t)} \mathcal{H}(p) \parallel \text{Timestamp}_t \parallel \text{AuthorID} \right)$$

### 3.1 The Causal Lineage Invariant

Let $\mathcal{G}_{\text{DAG}} = (V, E)$ be the repository commit history. For every artifact node $v \in V$:

$$\exists \text{ path } \pi: v_0 \rightsquigarrow v \quad \text{where } v_0 \in \mathcal{V}_{\text{origin}}$$

$$\operatorname{Cycles}(\mathcal{G}_{\text{DAG}}) = \emptyset \quad (\text{Strict Causal Ordering})$$

```
          [TĪPUNA] Ancestral Data Sources (v_0)
                     │
                     ▼
          [HAPŪ] Design & Builder Seats (v_1)
                     │
                     ▼
          [IWI] Deployment & Accountability (v_2)
                     │
                     ▼
          [MOKOPUNA] Future Heirs & Descendants (v_3)
  Invariant: Unbroken cryptographic hash chain from v_0 to v_3
```

No node may exist without an explicit ancestor edge ($e \in E$), and no commit may alter past ancestral hashes without invalidating all downstream descendants.

---

## 4. Transcendental & Governance Semiotics

Whakapapa transforms artificial intelligence from an unaccountable black box into an honorable genealogical participant:
- It guarantees attribution to human creators whose work shaped the training corpus.
- It prevents model collapse: synthetic models learning from previous synthetic models can trace lineages to ensure training diversity and prevent incestuous epistemic feedback loops.

---

## 5. Falsification Boundary

The Whakapapa architecture is **falsified** if:
1. An untraceable, anonymous codebase without commit provenance or dependency lineage demonstrates lower long-term vulnerability injection rates than a system enforcing strict Merkle-DAG Whakapapa verification.
2. Cyclic causal loops can be proven to resolve consistently without paradox in an autonomous state machine.

---

## 6. Empirical Test Specification

```python
# Empirical verification of Whakapapa cryptographic lineage DAG
import hashlib

def verify_whakapapa_chain(chain_nodes):
    prev_hash = "GENESIS"
    
    for node in chain_nodes:
        # Verify parent link
        assert node["parent_hash"] == prev_hash, (
            f"Lineage break: Node {node['id']} claims parent "
            f"{node['parent_hash']}, expected {prev_hash}"
        )
        # Compute node hash
        hasher = hashlib.sha256()
        hasher.update((node["id"] + node["parent_hash"] + node["payload"]).encode("utf-8"))
        node_hash = hasher.hexdigest()
        assert node["hash"] == node_hash, f"Tampered node hash at {node['id']}"
        prev_hash = node_hash
        
    return True

if __name__ == "__main__":
    nodes = []
    # Build a small verified 3-node Whakapapa chain
    h0 = "GENESIS"
    for idx, payload in enumerate(["Tipuna", "Hapu", "Mokopuna"]):
        hasher = hashlib.sha256()
        nid = f"node_{idx}"
        hasher.update((nid + h0 + payload).encode("utf-8"))
        h_cur = hasher.hexdigest()
        nodes.append({"id": nid, "parent_hash": h0, "payload": payload, "hash": h_cur})
        h0 = h_cur
        
    assert verify_whakapapa_chain(nodes)
    print("Whakapapa lineage DAG check: PASS")
```
