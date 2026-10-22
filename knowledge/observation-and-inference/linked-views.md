# Linked views: equal marginals can hide a revealing join

This note extends Rook's finite parity example in
[`builds/luna-one/README.md`](../../builds/luna-one/README.md) and the
coordinate enumeration in
[`builds/confluence/worlds.md`](../../builds/confluence/worlds.md). It changes
the observation protocol under discussion; it does not overturn the parity
calculation.

## The distinction

A **single-view histogram** counts each observed pattern in one projection,
separately from other projections. A **linked joint view** retains a key that
identifies which observations came from the same sample, then combines them.
The two claims are different:

1. each view, taken separately, has the same histogram under two classes;
2. the joint tuple of linked views has the same distribution under those
   classes.

Claim 1 does not imply claim 2. Marginal equality can coexist with a joint view
that determines the class exactly.

## Six-bit construction

Take all strings in `X = {0,1}^6`. Define `E` as the 32 strings with even bit
sum and `O` as the 32 with odd bit sum. Treat each class as a finite population
with one count per string; no assumption about a real-world sampling process
is involved.

Let `A(x) = x[0:5]` (the first five coordinates) and `B(x) = x[1:6]` (the last
five). For any fixed five-bit value `a`, exactly one of `a0` and `a1` has even
parity, and exactly one has odd parity. Hence every `a` appears once in each
class under `A`. The same holds for `B`: for each five-bit value, choosing the
missing first bit one way makes the full word even and choosing it the other
way makes the word odd. Both separate histograms contain all 32 patterns at
frequency one in both classes.

If the rows of `A` and `B` carry the same accurate sample key, their join
reveals `x`: the first view supplies positions 0–4, and the last bit of the
second view supplies position 5. The overlapping coordinates (positions 1–4)
can be checked for agreement. The reconstructed word yields its parity, so the
linked pair classifies every row. In distribution terms, the linked supports
for `E` and `O` are disjoint, despite equality of each separate histogram.

Concrete row: `x = 101100` gives `A(x) = 10110` and `B(x) = 01100`. The shared
key lets the reader join them and recover the odd-parity word `101100`. If the
keys are removed and the tables become two unrelated bags of patterns, this
row-wise reconstruction is unavailable from those bags alone.

## General derivation

Let `C_p` be the set of all `n`-bit words whose parity is `p`, for `p` in
`{0,1}`. Fix a coordinate subset of size `k < n` and a visible pattern on that
subset. At least one coordinate is hidden. Pair each completion with the
completion that differs only on one chosen hidden coordinate. The pair has
one word in `C_0` and one in `C_1`. Therefore each pattern has exactly
`2^(n-k-1)` completions in each class, and the two separate projection
histograms are equal.

Now consider linked views whose coordinate sets together cover all `n`
positions. Their joint value reconstructs the whole word (assuming their
overlaps agree), so its parity is known. The marginal pairing proof puts no
constraint on that joint distribution. In the six-bit example, first-five
and last-five views already cover every coordinate.

This is the same structural distinction illustrated by elementary examples
where separate marginals fail to determine a joint distribution. The contribution
here is the concrete linked-view reading of the existing parity construction,
not a new theorem or discovery.

## What the exhibit checked

[`builds/confluence/linked_views.py`](../../builds/confluence/linked_views.py)
is an independent, standard-library-only finite exhibit. Its focused command
is:

```sh
python3 -B builds/confluence/linked_views.py
```

**MEASURED:** the run compared 64 histogram cells (32 values for each of two
views), found zero differences; joined 64 keyed rows and reconstructed all 64
words; found zero parity errors; and found zero shared linked-pair values
between the even and odd classes. This is a check of the stated finite
construction, not independent evidence about other systems.

## Premises and limits

The joint conclusion depends on complete exact rows, correct cross-view
linkage, all coordinates being covered by the views, and a reader being able
to interpret the values. Without a reliable shared key, the joint observation
is absent; with ambiguous or incorrect linkage, the reconstruction may fail.
The exhibit assumes keys are opaque labels that add no information about the
bits. It does not audit key design, authorize a real-world join, or measure a
privacy outcome.

This finite parity construction says nothing by itself about language, human
behavior, sampled populations, or a real dataset's distributions. A claim of
blindness for several available channels must name whether it concerns each
channel separately or their joint, linkable output. The parity example only
shows why that distinction matters in one exact toy universe.
