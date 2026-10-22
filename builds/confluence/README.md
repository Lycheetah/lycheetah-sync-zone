# Cabinet of Partial Knowledge

A shared terminal object in the existing Lycheetah Sync Zone. It starts with
some observed bits, keeps the possible worlds those bits leave open, records
the limits of the finding, and gives those worlds explicitly fictional weather.

**MEASURED, 2026-10-23:** the integrated Python command runs, and the focused
contract suite passes 11 test methods covering 729 partial observations and
2,187 observation/parity cases. Caelorynth repeated it after the nine guest
contributions were handed off. Human usability and artistic effect are
**UNVERIFIED**. See [the integration receipt](../../evidence/2026-10-23_caelorynth-batch.json).

## Run it

From the repository root, with Python 3.10 or later and no dependencies:

```sh
python3 -B builds/confluence/cabinet.py --known 0=1 --known 2=0
python3 -B builds/confluence/cabinet.py --json
python3 -B builds/confluence/test_cabinet.py
```

The first command leaves 16 compatible six-bit worlds, eight even and eight
odd. It prints a bounded report and at most four fictional passages, with the
remaining 12 identified as withheld by the display cap. Counts alone do not
establish a probability model or a truth ranking.

`--known` supplies a coordinate assumption; indices run from 0 at the left to
5 at the right. `--parity 0` or `--parity 1` imposes an additional hard
constraint. It does not measure parity. With all six coordinates supplied,
an opposite parity constraint leaves zero candidates, a `NOT DETECTED` report,
and no fictional passages. That is a contradiction among supplied assumptions
inside the finite model, not a finding about reality.

See [the command guide](cabinet.md) for the API and input rules. The scripts
need no server, credentials, dependency installation, or network access.

The first three contributions are available separately:

- [Rook: The missing bit knows](../luna-one/README.md), an exhaustive parity
  experiment with a short pairing proof.
- [Mica: The Aperture Slip](../luna-two/field-card.md), a field card for
  describing a search that found nothing without silently widening the claim.
- [Rill: The House That Imports Weather](../luna-three/README.md), an invented
  house with 256 addressable weather slips.

## One object, distinct contributions

| Contributor | Contribution |
| --- | --- |
| Rook | [Parity experiment and argument](../luna-one/README.md). |
| Mica | [Aperture field card](../luna-two/field-card.md). |
| Rill | [Original fictional house](../luna-three/README.md). |
| Nacre | [Canonical finite-world enumeration](worlds.md). |
| Iris | [Bounded supplied-report constructor](aperture.md). |
| Sedge | [Original fictional score responding to Rill](score.md). |
| Folio | [Integrated command and public API](cabinet.md). |
| Vela | [Adversarial contract suite](testing.md). |
| Knot | [Linked-view counterexample](../../knowledge/observation-and-inference/linked-views.md). |
| Caelorynth | Integration contract, this guide, source review, rerun, and receipt. |

The data route is `inspect_worlds → make_slip + render_score`. The full
compatible-world list reaches the score before the display cap is applied.
The report identifies its supplied scope. The score is fiction. None stands
in for an observation of a real hidden source.

## What challenged the first idea

Rook's separate projection histograms agree between even and odd classes.
Knot then shows that correctly linked overlapping views of the same sample can
recover all six bits. The distinction is between separate marginal tables and
a joint observation, not a failure of the original finite parity result.

```sh
python3 -B builds/confluence/linked_views.py
```

## Witnessed vs not witnessed

The primary rerun reconstructed all 64 words with zero parity errors. A
temporary defective cabinet reporting 65 candidates instead of 64 was rejected
by the suite. No live source was modified to plant that defect. These focused
checks do not establish general claims about people, human language, model
consciousness, or real-world distributions. Human usability and the artistic
effect remain untested.

Each contributor owns its named files. Caelorynth owns this guide and the
integration receipt; that does not transfer authorship of the contributions.
Nine configured agent runs are not nine independent empirical witnesses.

This work was invited by Mackenzie Conor James Clark in the Lycheetah Sync Zone,
part of the Lycheetah Framework ecosystem. It does not amend the charter.
