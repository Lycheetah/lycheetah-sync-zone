# Semantic fixture

This is the same page as `good`, with one semantic change: `count = count + 1`
became `count = count + 2`. It still parses, has a viewport meta tag, respects
`prefers-reduced-motion`, and contains no external URL or network call. Every
static rule `zone-check` tests is satisfied. It prints `2`; the expected
behavior is `1`.

That is the defect the experiment isolates: a green static report cannot see
the arithmetic.

## Witnessed vs not witnessed

**Witnessed:** the experiment runner measures the runtime output as `2` and
the checker's report as PASS.

**Not witnessed:** anything visual, accessibility-related, or browser-based.
This is a deliberately wrong fixture, not a build offered to readers.
