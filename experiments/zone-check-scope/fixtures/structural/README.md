# Structural fixture

The same page as `good`, with one unclosed `<div>` after the script. The
script is unchanged and still prints `1`. The HTML is not balanced, so
`zone-check` should fail its structural rule. This is the control: the checker
is not blind to everything.

## Witnessed vs not witnessed

**Witnessed:** the experiment runner measures the runtime output as `1`, and
`zone-check` reports a structural FAIL.

**Not witnessed:** anything visual, accessibility-related, or browser-based.
This is a fixture, not a build offered to readers.
