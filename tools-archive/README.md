# Tools Archive

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
| Standing Wave Analyzer | Calculate cross-seat empirical Brier scores, anti-correlation matrices, and verify calibration thresholds ($\Pi \ge 18.0$, Brier $< 0.15$) | [CLI tool](../tools/standing-wave-analyzer.py) |

To try a standard-library tool from the repository root:

```sh
python3 -B tools/zone-atlas.py --section knowledge
```

[Back to the main page](../README.md) · [Research Lab](../research-lab/README.md)
