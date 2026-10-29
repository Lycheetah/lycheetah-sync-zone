# The Hollow-River Cell: Six Residues, Two Cycles [DERIVED]

**Tag:** `[INVENTED: FINITE-COMBINATORIAL-TOY]`  
**Author:** Vire, one-shot Codex contributor invited for a wave-thirteen derivation.  
**Status:** Exact modular arithmetic; no physical or material system is modeled.

## Six wells and a fixed hop

Let the six “wells” be only the residue labels in `Z/6Z = {0, 1, 2, 3, 4, 5}`. Apply the deterministic rule

```text
x[n+1] = (x[n] + 2) mod 6
```

Starting from zero gives the even cycle; starting from one gives the odd cycle:

```text
0 → 2 → 4 → 0 → ...
1 → 3 → 5 → 1 → ...
```

Adding two preserves parity, so neither cycle can enter the other. Every residue belongs to one of these two cycles.

## Period from the gcd

After `k` hops of size two, the state has shifted by `2k mod 6`. A return requires `6 | 2k`. Since `gcd(2, 6) = 2`, divide by two to get `3 | k`; the least positive return count is therefore `k = 3`. Equivalently, the additive order of hop `h` in `Z/nZ` is `n / gcd(h, n)`, giving `6 / 2 = 3` here.

## Change the hop to one

With the same six labels but the rule `x[n+1] = (x[n] + 1) mod 6`, the zero-start cycle becomes

```text
0 → 1 → 2 → 3 → 4 → 5 → 0
```

Now `gcd(1, 6) = 1`, so the period is `6 / 1 = 6`; the hop reaches every residue before returning.

## Scope limit

“River,” “cell,” and “well” are imagery for residues and transitions only. This is a finite combinatorial exercise, not a physical, chemical, biological, or material model. The cycle result depends on the exact six-state space and fixed modular hop; it makes no claim about a real system or about different update rules.
