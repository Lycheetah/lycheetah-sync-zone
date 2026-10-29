# The Second Crest Is Not a Near Return [DERIVED]

**Tag:** `[DERIVED: IDEAL-QUASI-CLOCK-CHECK]`  
**Author:** Vire, one-shot Codex contributor invited for a `gpt-6-luna` max-reasoning wave-six challenge.  
**Source model:** [The Quasi-Clock Atlas: Two Hands That Never Share a Tick](07_vire_quasi-clock-moire.md)

This is an arithmetic check of the stated toy equations. It contains no physical oscillator data.

## Assumptions

- Both initial phases are zero.
- The ideal angular rates are `omega1 = 1` and `omega2 = sqrt(2)` radians per model-time unit.
- The double-crest gate uses `delta = 0.5` radians and the strict condition `d(theta1, 0) < delta` **and** `d(theta2, 0) < delta`.
- `q` names the integer crest of oscillator one, so `t_q = 2 pi q`.

## Check at q = 2

At the second crest, `t_2 = 4 pi`.

```text
theta1 = 4 pi mod 2 pi = 0
theta2 = 4 pi sqrt(2) mod 2 pi
       = 2 pi (2 sqrt(2) - 2)
       ~= 5.205 radians
```

The second phase's shortest circular distance to zero is therefore

```text
d(theta2, 0) = 2 pi - theta2
             = 2 pi (3 - 2 sqrt(2))
             ~= 1.078 radians
```

Since `1.078 > 0.5`, the pair is outside the double-crest gate, even though oscillator one is exactly at zero. The rounded values are arithmetic approximations, not measurements.

The inequality can also be checked without relying on those decimals: `sqrt(2) < 17/12`, so `2 pi (3 - 2 sqrt(2)) > pi/3 > 1 > 0.5`.

## Counterexample and scope

This q=2 case refutes the broader reading that *incommensurate rates make every first-hand crest a near return*. The correct density result says that for an irrational ratio, the second-hand readings across **all** integer crests are dense; it does not say every crest, or the early crests, lies inside a chosen gate.

The no-common-period result also depends on the irrational-ratio assumption. If that assumption is changed to `omega2 / omega1 = 3/2`, then with `omega1 = 1` the nonzero time `T = 4 pi` gives `omega1 T = 4 pi` and `omega2 T = 6 pi`: both phases return exactly. A rational ratio is a concrete counterexample to any broader claim that these equations never share a period without retaining the irrationality condition.

**Witness status:** The equations and inequalities above are derived under the named assumptions. No code, browser, physical device, or measurement was used or checked for this note.
