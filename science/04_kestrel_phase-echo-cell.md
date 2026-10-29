# Phase-Echo Cells: A Tiny Medium with a Delayed Return

**Tag:** `[INVENTED: DISCRETE-DYNAMICS]`  
**Author:** Kestrel (Codex subagent; requested gpt-6-luna, low reasoning; wave two)  
**Status:** `[CONJECTURE]` toy-model proposal; no simulation or physical experiment run

## Ground and invention

Discrete state-update systems are a standard way to define toy dynamics. The
specific cells and rule below are invented for this note. They make no claim
about a real material, field, or physical law.

## The cell

Place cells on a ring. Each cell has a phase `p` in `{0, 1, 2, 3}` and a marker
`m` in `{0, 1}`. At each tick, cell `i` reads its left and right neighbors from
the *previous* tick, so every update is simultaneous.

1. Advance the phase: `pᵢ' = (pᵢ + 1 + mᵢ) mod 4`.
2. Set the marker: `mᵢ' = 1` exactly when the old left neighbor's phase was 0
   and the old right neighbor's phase was 2; otherwise set `mᵢ' = 0`.

The marker therefore adds one extra phase step on the following tick. It is an
echo with a one-tick delay, not stored energy or a signal measured in nature.

## Prediction to try

**[DERIVED, conditional on the rule]:** Given a ring size and initial state,
the system is deterministic and must eventually repeat a complete state,
because only `8ⁿ` complete states exist for a ring of `n` cells. A repeated
state implies a periodic orbit. This does not imply that the orbit is short or
that a traveling pattern exists.

**[CONJECTURE]:** Some sparse initial states may produce a moving band of
markers before falling into a short cycle. This can be checked by enumerating
small rings and recording the full state at each tick.

## What would count against it

The periodicity claim would be falsified by a correct implementation that
produced more than `8ⁿ` distinct complete states before a repeat; that would
indicate a rule or counting error. The moving-band conjecture fails for any
specified initial state if enumeration shows no such band. A failed pattern is
useful: it narrows the conditions under which the echo appears.

**Witness status:** UNVERIFIED. No code, run, or physical experiment is included.
