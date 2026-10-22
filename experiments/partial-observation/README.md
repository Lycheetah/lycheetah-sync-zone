# A partial-observation bench

**Sources:** [Rook](../../builds/luna-one/README.md),
[the cabinet model](../../builds/confluence/worlds.md),
[Knot](../../knowledge/observation-and-inference/linked-views.md).

From the repository root:

```sh
python3 -B builds/luna-one/partial-parity.py
python3 -B builds/confluence/cabinet.py --known 0=0 --known 1=0 --known 2=0 --known 3=0 --known 4=0 --json
python3 -B builds/confluence/linked_views.py
```

**DERIVED expectation:** five supplied zeros leave two six-bit completions of
opposite parity. A separate histogram for a proper projection cannot distinguish
the uniform parity classes. Correctly linked overlapping views of the same
sample can reveal all six bits. These are different information conditions.

The [test suite](../../builds/confluence/testing.md) describes its coverage.
Read the actual run receipt before repeating a measured-pass claim. This bench
does not model human belief or establish a real-world sampling distribution.
