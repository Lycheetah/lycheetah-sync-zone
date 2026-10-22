# Iris: The Aperture Slip Constructor

`aperture.py` provides a pure, standard-library-only constructor for one
caller-supplied report. It does not search files, observe a screen, or decide
whether a report is true. Its output is JSON-safe and keeps the target,
boundary, method, and exposure visible beside the outcome.

## Outcome and signal rules

The accepted outcome strings are exactly `FOUND`, `NOT DETECTED`, `NO ACCESS`,
`AMBIGUOUS`, and `NO RECORD HERE`. Required descriptions must be nonempty
strings. Surrounding whitespace is trimmed. Control characters and Unicode
line separators are rejected so a supplied description cannot split the
one-line report. The outcome spelling is exact.

`signal` is reserved for `FOUND`: it must contain a nonempty description for
that outcome and must be empty for every other outcome. For `AMBIGUOUS`, put a
candidate description in the supplied target or method text; the signal field
does not imply that a finding was confirmed. A non-FOUND outcome with a signal
is rejected as contradictory.

The generated `supported_sentence` starts as a supplied report and repeats all
four scope descriptions. Its wording is bounded to the declared outcome:

- `NOT DETECTED` says only that no signal was reported within the named scope.
- `NO ACCESS` says the boundary could not be fully examined; it does not claim a
  completed search.
- `NO RECORD HERE` says only that no record appeared within the named scope; it
  does not establish that the event did not occur elsewhere or was never
  recorded.

Every slip's `limitation` says this is a supplied report rather than independent
validation. The function cannot establish that the method ran, that the
exposure is complete, who supplied the report, or whether any field is true.

## Invented examples

These examples are fictional and describe no actual person, system, or search.

```python
from builds.confluence.aperture import make_slip

found = make_slip(
    target="assignments satisfying the toy constraint",
    boundary="all eight three-bit assignments",
    method="enumerate the finite assignment list",
    exposure="one pass over the listed assignments",
    outcome="FOUND",
    signal="three assignments satisfied the constraint",
)

not_detected = make_slip(
    target="assignments satisfying the toy constraint",
    boundary="all eight three-bit assignments under the stated model",
    method="enumerate the finite assignment list",
    exposure="one pass over the listed assignments",
    outcome="NOT DETECTED",
)
```

The second example reports a result under a stated finite model. It does not
claim that a real-world target is absent. Likewise, a `FOUND` signal reports
what the caller supplied; this constructor does not reproduce the enumeration.

## Limitation on the card

`NOT DETECTED` and `NO RECORD HERE` may blur when the target is itself a report.
The intended distinction depends on whether the target names an event/signal or
a record, and on a boundary that identifies the searched record set. The
outcome label alone cannot supply that meaning, and this constructor cannot
infer the writer's intended target.
