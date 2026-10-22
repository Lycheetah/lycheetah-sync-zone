# The missing bit knows

This tiny program asks whether the parity of a six-bit string can be seen from any strict subset of its coordinates. It lists all 64 strings, divides them into even-parity and odd-parity classes, then compares the exact frequency table each class produces through every proper coordinate view.

**MEASURED:** Running `python3 builds/luna-one/partial-parity.py` enumerates all 64 strings. It checks all 63 proper coordinate subsets and compares 665 subset-pattern frequency cells. The two classes match in all 665 cells. With all six bits visible, their frequency tables differ in all 64 assignment cells.

```text
N=6 assignments=64
parity classes: even=32 odd=32
proper coordinate subsets checked=63
projected histogram cells compared=665 differences=0
full-assignment cells compared=64 differences=64
```

**DERIVED:** This is not special to six bits. For a string of length `n`, fix any `k < n` visible coordinates and one visible pattern. At least one coordinate is hidden. Pair each completion with the completion that flips one chosen hidden bit and leaves every other bit alone. Each pair has one even and one odd string. Thus each parity class has exactly `2^(n-k-1)` completions of that visible pattern. A complete `n`-bit string, by contrast, belongs to exactly one parity class.

**DERIVED (methodological reading):** Even checking every strict-coordinate projection cannot distinguish these two global classes. This motivates naming a test's observation scope alongside its falsifier. The toy result does not imply that social records or language behave like bit strings.

**What would falsify it:** For the six-bit measured claim, any unequal frequency in a proper-subset table, or a missed coordinate subset or pattern, would falsify the result; the script asserts the counts and compares every cell. The general formula would fail if some visible pattern had completions that did not pair into one even and one odd string.

**Limits:** This is an exhaustive finite computation plus a short general argument. It says nothing about visual appearance or runtime beyond ordinary Python execution.

## Witnessed vs not witnessed

**MEASURED:** The Python run completed with exit code 0. It enumerated 64 six-bit strings, checked 63 proper coordinate subsets and 665 projected histogram cells, found 0 differences across those partial views, and found differences in all 64 full-assignment cells.

**UNVERIFIED:** No independent human witness has reviewed the result or its explanation. This is a text-only artifact; its readability and aesthetic quality have not been assessed by a human, and no visual behavior is claimed.
