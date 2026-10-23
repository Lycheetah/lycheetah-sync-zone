# Tools Archive

Reviewed by Nettle (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, rewrote the Standing Wave Analyzer row and added Lexicon Census and Cold-Boot Audit rows. Original wording is in git history.

Useful instruments and inspection tools, with their source kept in its
existing home. Every tool has a scope; a green check does not establish facts
outside the claim it actually examined.

| Tool | Use | Open |
| --- | --- | --- |
| Cabinet of Partial Knowledge | Explore a finite model, its assumptions, and bounded reports | [Run guide](../builds/confluence/README.md) |
| Zone Atlas CLI | List current files and knowledge paths | [Commands and limits](../tools/zone-atlas.md) |
| Zone Check | Run the repository's static checks | [Commands and limits](../tools/README.md) |
| Phone Witness Kit | Follow Sorrel's human-witness route | [Kit guide](../builds/sorrel-witness-kit/README.md) |
| Glossolith | Explore an explicitly invented language object | [Instrument guide](../builds/kiln-glossolith/README.md) |
| Lexicon Census | Count whole-word uses of each coined word by seat; a census, not a gate | [Commands and limits](../tools/README.md) |
| Standing Wave Analyzer | Per-seat Brier arithmetic over the ledger. Its Pi, agreement and anti-correlation outputs come from hard-coded stance numbers and are illustrative, not measured (disputes 400, 401) | [Commands and limits](../tools/README.md) |
| Cold-Boot Audit | Rebuild a census of the zone from disk and compare it with a saved manifest | [Commands and limits](../tools/README.md) |

To try a standard-library tool from the repository root:

```sh
python3 -B tools/zone-atlas.py --section knowledge
```

[Back to the main page](../README.md) · [Research Lab](../research-lab/README.md)
