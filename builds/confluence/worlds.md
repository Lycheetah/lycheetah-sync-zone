# Cabinet of Partial Knowledge

`inspect_worlds` is a finite instrument over the 64 six-bit strings. A world
is written as six characters, with coordinate `0` at the left and coordinate
`5` at the right. `visible` records the coordinates directly observed and
their bit values.

```python
from builds.confluence.worlds import inspect_worlds

result = inspect_worlds({0: 0, 1: 0, 2: 0, 3: 0, 4: 0})
```

The returned dictionary has exactly these fields:

| Field | Meaning |
| --- | --- |
| `visible` | A copy of the supplied coordinate facts, with sorted string keys. |
| `observed_coordinates` | The supplied coordinate indices, sorted numerically. |
| `matching_worlds` | The number of worlds satisfying both the coordinate facts and the optional parity constraint. |
| `even_worlds` | Even-parity worlds among `compatible_worlds`. |
| `odd_worlds` | Odd-parity worlds among `compatible_worlds`. |
| `parity_constraint` | The supplied hard constraint (`0`, `1`, or `null`). |
| `examples` | The first at most four compatible worlds in lexicographic order. |
| `compatible_worlds` | Every compatible six-character world in lexicographic order. |

`matching_worlds` equals the length of `compatible_worlds`, and the even and
odd counts sum to it. The complete list is the canonical enumeration for
downstream instruments; `examples` is only its compact preview.

## Observation and prior are separate

The optional `parity` argument is a **hard prior/world constraint** in this
model. `parity=0` retains only even worlds; `parity=1` retains only odd worlds.
It does not report a measurement of parity, and this API does not represent
probability weights or Bayesian updating. Counts describe the worlds that
remain after both the visible coordinates and this explicit restriction are
applied. To inspect coordinate evidence alone, call the function with
`parity=None`.

Here is the small surprise: seeing five zeros leaves two worlds,
`000000` and `000001`. Their parities differ, so even after seeing five of six
coordinates the unconstrained counts are still one even and one odd. Adding
`parity=0` leaves only `000000`; that narrowing comes from the chosen
constraint, not from a newly observed sixth bit.

If all six coordinates are visible, exactly one world matches without a
constraint, so its parity is determined by those coordinates. A conflicting
constraint then produces zero compatible worlds. That zero means the
observation and the chosen constraint have an empty intersection; it does not
mean a successful observation of the requested parity. Run again with
`parity=None` to see the observation-only world.

Input validation is strict: `visible` must be a built-in `dict`; coordinate
keys must be exact integers from 0 through 5; bit values and non-null parity
must be exact integers 0 or 1. Booleans are rejected even though Python treats
them as integer subclasses. Wrong types raise `TypeError`; integer values
outside the stated ranges raise `ValueError`.

## Limits

**DERIVED:** the six-bit pairing argument behind Rook's parity result says any
strict coordinate view has equally many even and odd completions. This
instrument makes that finite set explorable; it does not show that a real-world
source has a uniform distribution over these worlds.

The enumeration is deliberately finite and unweighted. It says nothing about
which world is more likely, whether a source was sampled uniformly, or whether
the parity restriction is justified. No visual or human-witness claim is made.
