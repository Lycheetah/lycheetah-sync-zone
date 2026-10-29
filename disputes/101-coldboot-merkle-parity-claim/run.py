#!/usr/bin/env python3
"""Dispute 101: does cold-boot reconstruction match the declared Merkle root with zero discrepancies?
Calls verify_against_manifest in the default mode the runner uses, then in exact_mode."""
import importlib.util, json
from pathlib import Path
root = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("cba", root / "tools/cold-boot-audit.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
a = m.ColdBootStateAuditor(root)
mp = root / "knowledge/discovery-and-memory/declarative-state-manifest.json"
man = json.loads(mp.read_text()); dyn = a.reconstruct_full_state()
mroot = lambda d: d.get("merkle_root") or d.get("checksums", {}).get("merkle_root")
print("manifest seats:", len(man.get("seats", [])), "| dynamic seats:", len(dyn["seats"]))
print("manifest merkle:", mroot(man)); print("dynamic  merkle:", mroot(dyn) or dyn.get("merkle_root"))
ok, f, d = a.verify_against_manifest(mp)
print(f"default mode (what run_audit.py calls): clean={ok} fidelity={f} discrepancies={len(d)}")
ok, f, d = a.verify_against_manifest(mp, exact_mode=True)
print(f"exact_mode=True: clean={ok} fidelity={f} discrepancies={len(d)}")
for x in d: print("  -", x[:150])
