# Network fixture

The same page as `good`, with an uncalled function containing `fetch('/api')`.
The function is never called, so the page still prints `1`. The checker's
network rule should fail. This is the second control: a static scan can catch
a token even when the runtime path is not exercised.

## Witnessed vs not witnessed

**Witnessed:** the experiment runner measures the runtime output as `1`, and
`zone-check` reports a network FAIL.

**Not witnessed:** anything visual, accessibility-related, or browser-based.
This is a fixture, not a build offered to readers.
