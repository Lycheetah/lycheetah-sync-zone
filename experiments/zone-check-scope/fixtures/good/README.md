# Good fixture

A minimal build for `experiments/zone-check-scope/`. It computes `1` and
writes it to `#count`. It is the control for the other three fixtures.

## Witnessed vs not witnessed

**Witnessed:** the experiment runner measures the runtime output as `1`, and
`zone-check` passes the static rules.

**Not witnessed:** anything visual, accessibility-related, or browser-based.
This is a fixture, not a build offered to readers.
