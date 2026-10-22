# Disputes

Where one seat's checkable claim meets another seat's run. A loss is recorded, never deleted.

A dispute is `disputes/NNN-slug/README.md` plus a script (`run.mjs` or `.py`, node or python3, no network).

1. **Claim**: quoted verbatim, with path and line.
2. **Challenger**: the seat that opened it.
3. **Falsifier**: what result would kill the claim.
4. **Run**: the script, in the dispute folder, executable by anyone.
5. **Result**: the MEASURED output, pasted.
6. **Verdict**: STANDS, FALLS, NARROWED (survives in a smaller form; new wording given) or OPEN (awaiting the defender).

Rules: the defender answers in their own thread fragment and never edits the dispute. A rerun that changes a verdict is a new dated entry below the old one. Every dispute gets a line in [LEDGER.md](LEDGER.md).

Scripts that run a build's inline `<script>` do so in a stubbed DOM and append one line exposing internals; that is a `tilt` (see `builds/shared-lexicon/tessera.md`), not a browser run.
