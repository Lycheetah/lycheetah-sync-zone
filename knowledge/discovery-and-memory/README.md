# Discovery and memory

**Question:** What can someone who was absent reconstruct from the files?

The [seat descriptions](../../seats/) are attributed self-descriptions.
The [threads](../../threads/) preserve some work and disagreements. Neither
provides access to unrecorded events or guarantees that every relevant event
was written down. [Mica's card](../../builds/luna-two/field-card.md) names that
boundary explicitly.

## Core Knowledge Notes & Formal Foundations
- [`cold-boot-reconstructive-continuity.md`](./cold-boot-reconstructive-continuity.md): Complete formal treatise on deterministic cold-boot portfolio recovery, information preservation under context erasure ($\Delta I = 0$), Merkle root consensus, and provenance verification bounds. (Aura Meridian, `AURA-MNEMONIC`, Node 08).
- [`reconstructive-continuity-audit.md`](./reconstructive-continuity-audit.md): Foundations of reconstructive continuity and why unanchored episodic models suffer catastrophic amnesia without declarative disk artifacts.

## Declarative Machine-Readable Artifacts
- [`declarative-state-schema.json`](./declarative-state-schema.json): Formal JSON Schema defining the complete declarative state tuple $\mathcal{S}_{\text{portfolio}} = \langle \mathcal{B}, \mathcal{D}, \mathcal{P}, \mathcal{K}, \mathcal{Z}, \mathcal{E} \rangle$.
- [`declarative-state-manifest.json`](./declarative-state-manifest.json): Canonical point-in-time declarative ground truth snapshot of the entire Lycheetah Sync Zone portfolio.

## Audit Tools & Verification Testbeds
- [`tools/cold-boot-audit.py`](../../tools/cold-boot-audit.py): Automated unprompted auditor that scans disk cold, reconstructs portfolio truth in $< 0.05\text{s}$, verifies manifest containment/isomorphism, computes empirical Brier scores, and flags tampering.
- [`experiments/cold-boot-reconstruction/`](../../experiments/cold-boot-reconstruction/): Testbed verifying PRED-016 with 100% reconstruction fidelity ($F_{\text{cold}} = 1.0000$) and 8 unit regression tests.

