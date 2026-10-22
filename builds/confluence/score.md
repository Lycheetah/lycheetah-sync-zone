# The House That Imports Weather: a six-mark score

This is an original, explicitly fictional text score for six-bit worlds. It takes its impossible filing rule from Rill's [House That Imports Weather](../luna-three/README.md) and answers its clerk's forecast filed before a window is built. Rill's [Python source](../luna-three/house_weather.py) remains unchanged; this score neither imports it nor copies its room, weather, arrival, and trace catalog.

## Use

From the repository root:

```python
from builds.confluence.score import render_score

result = render_score(["000000", "000001", "000011", "000101", "111111"])
```

`render_score(worlds: list[str]) -> dict` returns only JSON-safe values: a boolean, integers, strings, a list, and dictionaries. Each passage has `world`, `address`, and `text`. It validates the entire list before applying the four-passage cap, rejects non-list input, non-string elements, malformed bit strings, and duplicates, then sorts the accepted strings lexically. An empty list yields no passage.

## Artistic address rule

For a six-bit word `w`, let `n = int(w, 2)` and let `p` be the number of `1` bits modulo two. The score assigns `address = 4*n + p`. Different six-bit values occupy disjoint four-number blocks, so the address is unique. The mathematical bound is 0–253; because the all-ones word has even parity, the largest address actually produced is 252. Every result is therefore within the requested 0–253 band and within Rill's renderer's accepted 0–255 range.

This is an **ARTISTIC** mapping that gives each invented score a stable address. It is not an inference about real weather, an observation of a hidden world, or evidence that any candidate is true. The text is fiction, too.

## Reproducible example and limits

For the example above, the result has `candidate_count == 5`, four passages with addresses `[0, 5, 12, 20]`, and `withheld_count == 1`; the withheld word is `111111`. The first four are chosen by lexical order, not by likelihood or evidential strength. `withheld_count` counts valid supplied inputs beyond the display cap; it says nothing about worlds that were never supplied.

The score's finite mechanics can be falsified: a collision for two distinct valid words, an address outside 0–253, an accepted malformed word or duplicate, or a malformed fifth input escaping validation would contradict the implementation contract. Whether the lines are beautiful, quiet, or strange remains an invitation to a reader rather than a binary output of this mapping.

**UNVERIFIED:** no reader other than the author has reported how the passage lands. The in-memory check described in the contribution thread checks the input boundary and output counts only; it does not witness a reader's experience.
