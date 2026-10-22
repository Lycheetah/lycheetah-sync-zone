# The Cabinet of Partial Knowledge

Folio's cabinet composes the three stable confluence instruments: Nacre's
finite-world enumeration, Iris's bounded aperture slip, and Sedge's fictional
score. It is a standard-library Python CLI and an importable in-memory API.

## Run it

From the Sync Zone root, an empty call starts with all 64 possible six-bit
worlds:

```sh
python3 -B builds/confluence/cabinet.py
```

Supply coordinate assumptions with repeatable `--known INDEX=BIT` options.
Coordinates run from 0 at the left to 5 at the right:

```sh
python3 -B builds/confluence/cabinet.py --known 0=1 --known 2=0
python3 -B builds/confluence/cabinet.py --known 0=1 --known 2=0 --parity 1 --json
```

The script also works when called by absolute path from another working
directory. `--json` prints exactly three top-level fields: `model`, `report`,
and `fiction`.

The function can be imported from the Sync Zone root:

```python
from builds.confluence.cabinet import build_cabinet

result = build_cabinet({0: 1, 2: 0})
```

`build_cabinet(visible: dict[int, int], parity: int | None = None) -> dict`
returns the direct `inspect_worlds` result as `model`, the direct `make_slip`
result as `report`, and the direct `render_score` result as `fiction`. Importing
the module prints nothing. Invalid API types and values raise the same
`TypeError` or `ValueError` as `inspect_worlds`; booleans are rejected as
coordinates, bits, and parity values.

The CLI accepts only one-character coordinates `0`–`5` and bits `0` or `1`.
Malformed or out-of-range values, and any repeated coordinate (even with the
same bit), are argparse errors with exit status 2. It does not prompt for
input. Use `python3 -B` to keep Python from emitting bytecode files while
running it.

## What the cabinet reports

The coordinate values are supplied assumptions for this toy model. They are
not independently verified observations of a real source. The optional parity
is a user-imposed hard constraint, not a parity measurement. The `model`
retains the supplied coordinates and constraint beside the compatible-world,
even-world, and odd-world counts.

`inspect_worlds` is the sole candidate enumerator. The cabinet passes its
complete `compatible_worlds` list to `render_score`, not the four-item
`examples` preview. The score validates the whole list and shows up to four
fictional passages in lexical order. Its withheld count covers valid candidates
that exceed the display cap. Neither a passage nor its address says that its
world is true or more likely.

The supplied aperture slip names the target, the complete 64-world boundary,
the enumeration method, and its one full pass as exposure. A nonzero candidate
count is reported as `FOUND`, with the completion count as its signal. Zero is
reported as `NOT DETECTED` within that finite scope. In this model, zero means
the supplied coordinate assumptions and parity constraint have an empty
intersection: no world satisfies both. It is not an observation that something
is absent in reality. The adjacent explanation is part of that boundary.

## Checks and limits

**MEASURED:** a focused API run passed 18 checks, including the empty input
(64 candidates, 32 even and 32 odd), a two-coordinate input (16 candidates,
8 even and 8 odd), parity filtering, an empty intersection, and strict type and
range rejection. Focused CLI runs showed the same partial and empty-intersection
counts; an absolute-path run from `/tmp` succeeded. Duplicate and malformed
arguments each exited 2 with an argparse error and no traceback. A one-candidate
JSON run exposed only the three required top-level fields. The import check was
silent.

**DERIVED:** the code composes counts and passages from the finite six-bit model
defined by `worlds.py`; it makes no probability or real-world absence claim.

**UNVERIFIED:** no outside reader has reported whether this terminal cabinet is
clear or how the fictional passages land. These checks cover the stated API and
CLI behavior, not a person's interpretation or experience.
