# Cabinet contract suite

Run the focused suite from the Sync Zone root:

```sh
python3 -B builds/confluence/test_cabinet.py
```

The suite uses only Python's standard library. Its independent completion oracle
fills hidden coordinates directly, then checks every partial observation made
from six positions where each position is hidden, zero, or one. It evaluates
each of those 729 observations with no parity constraint and with both hard
parity constraints, for 2,187 model cases. The unittest count and the model
scenario count are separate quantities.

Other focused checks cover strict input types and ranges (including booleans),
validation past the four-passage display cap, all 64 unique artistic addresses,
candidate and withheld counts, the five caller-supplied Aperture Slip outcomes,
zero-compatible intersections, and the JSON command line from a foreign
working directory. No browser, server, network, or third-party package is used.

## Run record

**MEASURED, 2026-10-23:** `python3 -B builds/confluence/test_cabinet.py` exited
0: `Ran 11 tests`, `OK`. The exhaustive test evaluated 729 partial observations
with no parity and with each of the two parity constraints, for 2,187 model
cases. It passed type/range/boolean rejection through both `inspect_worlds` and
`build_cabinet`, the score's full-list validation and display cap, all 64 address
uniqueness checks, supplied-report scope checks, and the foreign-directory CLI
cases.

**MEASURED mutation check, 2026-10-23:** a Python standard-library driver copied
`cabinet.py`, `worlds.py`, `aperture.py`, and `score.py` into a temporary tree.
In that copy only, it dropped one candidate from the unconstrained, no-input
result by inserting:

```python
if not visible and parity is None:
    model["compatible_worlds"] = model["compatible_worlds"][:-1]
```

The driver then ran the same suite with
`CONFLUENCE_CABINET_PATH=<temporary-copy>/builds/confluence/cabinet.py`.
The mutated run exited 1 as expected: the exhaustive oracle failed for the
all-hidden, unconstrained case, and the default CLI check caught the missing
world. It ran all 11 test methods. The temporary tree was removed when the
driver exited; the live Cabinet source was not edited.

The suite checks finite software contracts and report boundaries. It does not
validate any caller-supplied report against an outside source, and it does not
judge the fiction's aesthetic effect. It has not been witnessed by a human reader
or on a visual runtime.
