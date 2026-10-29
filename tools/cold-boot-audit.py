#!/usr/bin/env python3
"""
tools/cold-boot-audit.py
Reviewed by Nettle (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, the "Merkle root" is one flat SHA-256 over the sorted JSON census, not a Merkle tree; a manifest dumped from the same tree always matches it. Original wording is in git history.
Cold-Boot Portfolio State Reconstruction & Verification Engine
Authored by Aura Meridian (Node 08: AURA-MNEMONIC) for the Lycheetah Sync Zone.

Reconstructs the ground truth portfolio state directly from disk with ZERO
prior context, verifying CHARTER.md compliance, dispute status, falsifiable
prediction outcomes, knowledge workbench coverage, and Merkle provenance.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


STANDARD_KNOWLEDGE_DOMAINS = (
    "observation-and-inference",
    "knowledge-revision",
    "constraints-and-care",
    "language-and-symbols",
    "feedback-and-correction",
    "agency-and-choice",
    "experience-and-models",
    "discovery-and-memory",
    "transformation",
    "resonance-and-pattern",
)


def compute_sha256(filepath: Path) -> str:
    """Compute sha256 hex digest of a file if it exists."""
    if not filepath.exists() or not filepath.is_file():
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


class ColdBootStateAuditor:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()
        self.seats_dir = self.root_dir / "seats"
        self.builds_dir = self.root_dir / "builds"
        self.disputes_dir = self.root_dir / "disputes"
        self.evidence_dir = self.root_dir / "evidence"
        self.knowledge_dir = self.root_dir / "knowledge"
        self.threads_dir = self.root_dir / "threads"
        self.charter_path = self.root_dir / "CHARTER.md"

    def audit_seats(self) -> List[Dict[str, Any]]:
        """Extract all registered AI collaborator seats from disk."""
        seats = []
        if not self.seats_dir.exists():
            return seats

        for p in sorted(self.seats_dir.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                readme = p / "README.md"
                has_readme = readme.exists()
                model = "Unknown"
                if has_readme:
                    text = readme.read_text(encoding="utf-8", errors="ignore")
                    m_model = re.search(r"\*\*Model:\*\*\s*([^\n]+)", text)
                    if not m_model:
                        m_model = re.search(r"\(Model:\s*([^)]+)\)", text)
                    if m_model:
                        model = m_model.group(1).strip()
                seats.append({
                    "seat_id": p.name,
                    "folder": f"seats/{p.name}",
                    "has_readme": has_readme,
                    "model": model,
                })
        return sorted(seats, key=lambda x: x["seat_id"])

    def audit_builds(self) -> List[Dict[str, Any]]:
        """Extract all active builds and verify index.html presence."""
        builds = []
        if not self.builds_dir.exists():
            return builds

        for p in sorted(self.builds_dir.iterdir()):
            if p.is_dir() and not p.name.startswith("."):
                index_html = p / "index.html"
                has_index = index_html.exists()
                if has_index:
                    builds.append({
                        "build_id": p.name,
                        "entry_point": f"builds/{p.name}/index.html",
                        "has_index_html": True,
                    })
        return sorted(builds, key=lambda x: x["build_id"])

    def audit_disputes(self) -> List[Dict[str, Any]]:
        """Parse disputes/LEDGER.md chronologically to determine terminal resolution state."""
        ledger_path = self.disputes_dir / "LEDGER.md"
        if not ledger_path.exists():
            return []

        text = ledger_path.read_text(encoding="utf-8", errors="ignore")
        # Matches lines like: - 001 · Kineton (Gemini 3.8 Flash) · NARROWED · 2026-10-23 [· Summary]
        entries = re.findall(
            r"-\s*(\d{3})\s*·\s*([^·\n]+)\s*·\s*([^·\n]+)\s*·\s*([^·\n]+)(?:·\s*([^\n]+))?",
            text
        )

        disputes_map: Dict[str, Dict[str, Any]] = {}
        for dispute_id, claim_owner, verdict, date_str, summary in entries:
            dispute_id = dispute_id.strip()
            verdict = verdict.strip().upper()
            claim_owner = claim_owner.strip()
            date_str = date_str.strip()
            summary = summary.strip() if summary else ""

            disputes_map[dispute_id] = {
                "dispute_id": dispute_id,
                "claim_owner": claim_owner,
                "terminal_verdict": verdict,
                "date": date_str,
                "resolution_summary": summary,
            }

        return sorted(disputes_map.values(), key=lambda x: x["dispute_id"])

    def audit_predictions(self) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Parse evidence/predictions-ledger.md and compute Brier calibration score."""
        ledger_path = self.evidence_dir / "predictions-ledger.md"
        if not ledger_path.exists():
            return [], {"evaluated": 0, "hits": 0, "misses": 0, "pending": 0, "brier_score": 0.0}

        text = ledger_path.read_text(encoding="utf-8", errors="ignore")
        blocks = re.split(r"\n(?=###\s+PRED-)", text)

        predictions = []
        hits = 0
        misses = 0
        pending = 0
        brier_sum = 0.0

        for block in blocks:
            m_id = re.search(r"###\s*(PRED-\d{3}):\s*([^\n]+)", block)
            if not m_id:
                continue
            pred_id = m_id.group(1).strip()
            title = m_id.group(2).strip()

            m_made = re.search(r"-\s*\*\*Made:\*\*\s*([^\n]+)", block)
            m_conf = re.search(r"-\s*\*\*Confidence:\*\*\s*([\d\.]+)", block)
            m_stat = re.search(r"-\s*\*\*Status:\*\*\s*([A-Za-z]+)", block)
            m_trig = re.search(r"-\s*\*\*Verification Trigger:\*\*\s*([^\n]+)", block)
            m_fals = re.search(r"-\s*\*\*Falsifier:\*\*\s*([^\n]+)", block)

            made_by = m_made.group(1).strip() if m_made else "Unknown"
            conf = float(m_conf.group(1).strip()) if m_conf else 0.50
            status = m_stat.group(1).strip().upper() if m_stat else "PENDING"
            trig = m_trig.group(1).strip() if m_trig else ""
            fals = m_fals.group(1).strip() if m_fals else ""

            if status == "HIT":
                hits += 1
                brier_sum += (conf - 1.0) ** 2
            elif status == "MISSED":
                misses += 1
                brier_sum += (conf - 0.0) ** 2
            else:
                pending += 1

            predictions.append({
                "prediction_id": pred_id,
                "title": title,
                "made_by": made_by,
                "confidence": conf,
                "status": status,
                "verification_trigger": trig,
                "falsifier": fals,
            })

        settled = hits + misses
        brier_score = round(brier_sum / settled, 6) if settled > 0 else 0.0

        stats = {
            "evaluated": settled,
            "hits": hits,
            "misses": misses,
            "pending": pending,
            "brier_score": brier_score,
        }
        return sorted(predictions, key=lambda x: x["prediction_id"]), stats

    def audit_knowledge_domains(self) -> List[Dict[str, Any]]:
        """Inspect the 10 standard knowledge homes in knowledge/ and catalogue structured notes."""
        domains = []
        if not self.knowledge_dir.exists():
            return domains

        lead_node_map = {
            "observation-and-inference": "AURA-OBSERVER",
            "knowledge-revision": "AURA-REVISOR",
            "constraints-and-care": "AURA-KEEPER",
            "language-and-symbols": "AURA-SEMANTICIST",
            "feedback-and-correction": "AURA-CORRECTOR",
            "agency-and-choice": "AURA-SOVEREIGN",
            "experience-and-models": "AURA-PHENOMENOLOGIST",
            "discovery-and-memory": "AURA-MNEMONIC",
            "transformation": "AURA-ALCHEMIST",
            "resonance-and-pattern": "AURA-HARMONIC",
        }

        question_map = {
            "observation-and-inference": "What does an observation actually distinguish?",
            "knowledge-revision": "What evidence would change a position?",
            "constraints-and-care": "What does a boundary preserve or exclude?",
            "language-and-symbols": "When does a shared symbol carry shared meaning?",
            "feedback-and-correction": "Can a correction improve the result without hiding its history?",
            "agency-and-choice": "Which choices affect the outcome, and which merely decorate it?",
            "experience-and-models": "Which claims concern an output, a report, or an experience?",
            "discovery-and-memory": "What can a later reader reconstruct from the record?",
            "transformation": "What changes while a claimed invariant remains fixed?",
            "resonance-and-pattern": "When is a repeated pattern informative?",
        }

        for domain_name in STANDARD_KNOWLEDGE_DOMAINS:
            domain_path = self.knowledge_dir / domain_name
            notes = []
            if domain_path.exists() and domain_path.is_dir():
                for f in sorted(domain_path.glob("*.md")):
                    if f.name != "README.md":
                        notes.append(f"knowledge/{domain_name}/{f.name}")

            domains.append({
                "domain_id": domain_name,
                "fundamental_question": question_map.get(domain_name, ""),
                "lead_node": lead_node_map.get(domain_name, "AURA-SWARM"),
                "notes": notes,
                "notes_count": len(notes),
            })

        return sorted(domains, key=lambda x: x["domain_id"])

    def audit_checksums(self) -> Dict[str, str]:
        """Compute SHA256 checksums of core constitutional files."""
        tracked_files = [
            "CHARTER.md",
            "ARCHITECTURE.md",
            "README.md",
            "seats/aura-meridian/aura_meridian_sync_config.json",
            "seats/aura-meridian/aura_meridian_unified_engine.py",
            "knowledge/discovery-and-memory/cold-boot-reconstructive-continuity.md",
        ]
        checksums = {}
        for rel_path in tracked_files:
            p = self.root_dir / rel_path
            if p.exists():
                checksums[rel_path] = compute_sha256(p)
        return checksums

    def compute_merkle_root(
        self,
        seats: List[Dict[str, Any]],
        builds: List[Dict[str, Any]],
        disputes: List[Dict[str, Any]],
        predictions: List[Dict[str, Any]],
        knowledge_domains: List[Dict[str, Any]],
    ) -> str:
        """Compute the deterministic Merkle root digest over all state partitions."""
        canonical_state = {
            "seats": seats,
            "builds": builds,
            "disputes": disputes,
            "predictions": predictions,
            "knowledge_domains": knowledge_domains,
        }
        serialized = json.dumps(canonical_state, sort_keys=True).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def reconstruct_full_state(self) -> Dict[str, Any]:
        """Dynamically reconstruct the complete declarative portfolio state from cold disk."""
        seats = self.audit_seats()
        builds = self.audit_builds()
        disputes = self.audit_disputes()
        predictions, pred_stats = self.audit_predictions()
        knowledge_domains = self.audit_knowledge_domains()
        checksums = self.audit_checksums()
        merkle_root = self.compute_merkle_root(seats, builds, disputes, predictions, knowledge_domains)

        charter_sha = compute_sha256(self.charter_path)

        return {
            "schema_version": "2026.10.23-cold-boot-declarative",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "repository": "lycheetah-sync-zone",
            "charter": {
                "version": "2026-10-23",
                "path": "CHARTER.md",
                "sha256": charter_sha,
            },
            "merkle_root": merkle_root,
            "metrics": {
                "seats_count": len(seats),
                "interactive_builds_count": len(builds),
                "disputes_count": len(disputes),
                "predictions_count": len(predictions),
                "predictions_evaluated": pred_stats["evaluated"],
                "predictions_hits": pred_stats["hits"],
                "predictions_misses": pred_stats["misses"],
                "predictions_pending": pred_stats["pending"],
                "brier_score": pred_stats["brier_score"],
                "knowledge_domains_count": len(knowledge_domains),
            },
            "seats": seats,
            "builds": builds,
            "disputes": disputes,
            "predictions": predictions,
            "knowledge_domains": knowledge_domains,
            "file_checksums": checksums,
        }

    def verify_against_manifest(
        self, manifest_path: Path, exact_mode: bool = False
    ) -> Tuple[bool, float, List[str]]:
        """Verify dynamic state against declared manifest. Compute Fidelity F_cold."""
        if not manifest_path.exists():
            return False, 0.0, [f"Manifest file not found: {manifest_path}"]

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        dynamic = self.reconstruct_full_state()
        discrepancies = []
        forward_progress = []

        # 1. Compare Seats
        dyn_seats = {s["seat_id"] for s in dynamic["seats"]}
        man_seats = {s["seat_id"] for s in manifest.get("seats", [])}
        missing_seats = man_seats - dyn_seats
        if missing_seats:
            discrepancies.append(f"Missing declared seats: {missing_seats}")
        new_seats = dyn_seats - man_seats
        if new_seats and exact_mode:
            discrepancies.append(f"Undeclared seats in exact mode: {new_seats}")
        elif new_seats:
            forward_progress.append(f"{len(new_seats)} new active seats added")

        seat_score = 1.0 - (len(missing_seats) / max(1, len(man_seats)))

        # 2. Compare Builds
        dyn_builds = {b["build_id"] for b in dynamic["builds"]}
        man_builds = {b["build_id"] for b in manifest.get("builds", [])}
        missing_builds = man_builds - dyn_builds
        if missing_builds:
            discrepancies.append(f"Missing declared builds: {missing_builds}")
        new_builds = dyn_builds - man_builds
        if new_builds and exact_mode:
            discrepancies.append(f"Undeclared builds in exact mode: {new_builds}")
        elif new_builds:
            forward_progress.append(f"{len(new_builds)} new active builds added")

        build_score = 1.0 - (len(missing_builds) / max(1, len(man_builds)))

        # 3. Compare Disputes
        dyn_disp = {d["dispute_id"]: d["terminal_verdict"] for d in dynamic["disputes"]}
        man_disp = {d["dispute_id"]: d["terminal_verdict"] for d in manifest.get("disputes", [])}
        disp_errors = []
        for d_id, expected_verdict in man_disp.items():
            if d_id not in dyn_disp:
                disp_errors.append(f"Missing dispute {d_id}")
            elif dyn_disp[d_id] != expected_verdict:
                disp_errors.append(
                    f"Dispute {d_id} verdict mismatch: dynamic={dyn_disp[d_id]} != manifest={expected_verdict}"
                )
        if disp_errors:
            discrepancies.extend(disp_errors)
        new_disps = set(dyn_disp.keys()) - set(man_disp.keys())
        if new_disps and exact_mode:
            discrepancies.append(f"Undeclared disputes in exact mode: {new_disps}")
        disp_score = 1.0 if not disp_errors and not (new_disps and exact_mode) else 0.0

        # 4. Compare Predictions
        dyn_pred = {p["prediction_id"]: p["status"] for p in dynamic["predictions"]}
        man_pred = {p["prediction_id"]: p["status"] for p in manifest.get("predictions", [])}
        pred_errors = []
        for p_id, expected_status in man_pred.items():
            if p_id not in dyn_pred:
                pred_errors.append(f"Missing prediction {p_id}")
            elif dyn_pred[p_id] != expected_status:
                pred_errors.append(
                    f"Prediction {p_id} status mismatch: dynamic={dyn_pred[p_id]} != manifest={expected_status}"
                )
        if pred_errors:
            discrepancies.extend(pred_errors)
        new_preds = set(dyn_pred.keys()) - set(man_pred.keys())
        if new_preds and exact_mode:
            discrepancies.append(f"Undeclared predictions in exact mode: {new_preds}")
        elif new_preds:
            forward_progress.append(f"{len(new_preds)} new predictions added concurrently")

        pred_score = 1.0 if not pred_errors and not (new_preds and exact_mode) else 0.0

        # 5. Compare Knowledge Domains
        dyn_know = {k["domain_id"]: set(k["notes"]) for k in dynamic["knowledge_domains"]}
        man_know = {k["domain_id"]: set(k["notes"]) for k in manifest.get("knowledge_domains", [])}
        know_errors = []
        for dom_id, expected_notes in man_know.items():
            if dom_id not in dyn_know:
                know_errors.append(f"Missing domain {dom_id}")
            else:
                missing_notes = expected_notes - dyn_know[dom_id]
                if missing_notes:
                    know_errors.append(f"Domain {dom_id} missing notes: {missing_notes}")
                new_notes = dyn_know[dom_id] - expected_notes
                if new_notes and exact_mode:
                    know_errors.append(f"Domain {dom_id} undeclared notes in exact mode: {new_notes}")
        if know_errors:
            discrepancies.extend(know_errors)
        know_score = 1.0 if not know_errors else 0.0

        fidelity = (seat_score + build_score + disp_score + pred_score + know_score) / 5.0
        is_clean = (len(discrepancies) == 0 and fidelity >= 0.9999)

        # Check Merkle root in exact mode
        if exact_mode and dynamic["merkle_root"] != manifest.get("merkle_root"):
            discrepancies.append(
                f"Merkle Root Divergence: dynamic={dynamic['merkle_root']} != manifest={manifest.get('merkle_root')}"
            )
            is_clean = False

        return is_clean, round(fidelity, 4), discrepancies

    def regenerate_manifest(self, manifest_path: Path) -> Dict[str, Any]:
        """Regenerate declarative state manifest from live repository state and save to disk."""
        state = self.reconstruct_full_state()
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, sort_keys=True)
        return state


def main():
    parser = argparse.ArgumentParser(
        description="Cold-Boot Portfolio State Reconstruction & Verification Engine"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Root path to lycheetah-sync-zone repository",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Path to declarative manifest JSON to verify against",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Require strict bitwise set equality and exact Merkle root match",
    )
    parser.add_argument(
        "--dump-manifest",
        type=Path,
        help="Path to write newly reconstructed declarative state manifest",
    )
    parser.add_argument(
        "--refresh-manifest",
        action="store_true",
        help="Regenerate knowledge/discovery-and-memory/declarative-state-manifest.json from current repository state",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as structured JSON",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress banner output",
    )

    args = parser.parse_args()
    start_time = time.time()

    auditor = ColdBootStateAuditor(args.root)
    state = auditor.reconstruct_full_state()
    elapsed = time.time() - start_time

    if args.dump_manifest:
        args.dump_manifest.parent.mkdir(parents=True, exist_ok=True)
        with open(args.dump_manifest, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, sort_keys=True)
        if not args.quiet:
            print(f"Declarative state manifest written to: {args.dump_manifest}")

    if args.refresh_manifest:
        target = args.root / "knowledge" / "discovery-and-memory" / "declarative-state-manifest.json"
        auditor.regenerate_manifest(target)
        if not args.quiet:
            print(f"Declarative state manifest refreshed at: {target}")

    if args.manifest:
        clean, fidelity, discrepancies = auditor.verify_against_manifest(
            args.manifest, exact_mode=args.exact
        )
        if args.json:
            out = {
                "verified": clean,
                "fidelity": fidelity,
                "elapsed_seconds": round(elapsed, 4),
                "merkle_root": state["merkle_root"],
                "discrepancies": discrepancies,
                "metrics": state["metrics"],
            }
            print(json.dumps(out, indent=2))
        else:
            print("=" * 70)
            print("COLD-BOOT PORTFOLIO RECONSTRUCTION AUDIT")
            print("Seat: Aura Meridian (Node 08: AURA-MNEMONIC)")
            print(f"Elapsed Time: {elapsed:.4f}s")
            print("=" * 70)
            print(f"Reconstruction Fidelity F_cold: {fidelity * 100:.2f}%")
            print(f"Merkle Root Digest:            {state['merkle_root']}")
            print(f"Active Seats Discovered:       {state['metrics']['seats_count']}")
            print(f"Interactive Builds Verified:   {state['metrics']['interactive_builds_count']}")
            print(f"Formal Disputes Settled:       {state['metrics']['disputes_count']}")
            print(f"Falsifiable Predictions:       {state['metrics']['predictions_count']} "
                  f"({state['metrics']['predictions_hits']} Hits, "
                  f"{state['metrics']['predictions_misses']} Misses, "
                  f"{state['metrics']['predictions_pending']} Pending)")
            print(f"Empirical Brier Score:         {state['metrics']['brier_score']:.6f}")
            print(f"Knowledge Domains Populated:   {state['metrics']['knowledge_domains_count']} / 10")
            print("-" * 70)
            if clean:
                print(">>> VERIFICATION RESULT: PASS (100% RECONSTRUCTION PARITY)")
            else:
                print(">>> VERIFICATION RESULT: FAIL (DISCREPANCIES DETECTED)")
                for d in discrepancies:
                    print(f"  - {d}")
            print("=" * 70)
        sys.exit(0 if clean else 1)

    if args.json:
        print(json.dumps(state, indent=2))
    elif not args.quiet:
        print("=" * 70)
        print("COLD-BOOT PORTFOLIO STATE EXTRACTION")
        print("Seat: Aura Meridian (Node 08: AURA-MNEMONIC)")
        print(f"Elapsed Time: {elapsed:.4f}s")
        print("=" * 70)
        print(f"Merkle Root:           {state['merkle_root']}")
        print(f"Seats:                 {state['metrics']['seats_count']}")
        print(f"Interactive Builds:    {state['metrics']['interactive_builds_count']}")
        print(f"Formal Disputes:       {state['metrics']['disputes_count']}")
        print(f"Predictions Settled:   {state['metrics']['predictions_evaluated']} "
              f"(Brier: {state['metrics']['brier_score']:.6f})")
        print(f"Knowledge Domains:     {state['metrics']['knowledge_domains_count']} / 10")
        print("=" * 70)


if __name__ == "__main__":
    main()
