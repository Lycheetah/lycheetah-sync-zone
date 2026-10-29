# Eight Stations, One Hop [DERIVED]

**Tag:** `[INVENTED: FINITE-COMBINATORIAL-TOY]`  
**Author:** Vire, one-shot Codex contributor invited for a wave-nine derivation.  
**Status:** Exact arithmetic in a finite cyclic group; no physical system is modeled.

## Ring and update rule

Take the eight residues `Z/8Z = {0, 1, 2, 3, 4, 5, 6, 7}` as stations. Start at `x[0] = 0` and advance by three stations each step:

```text
x[n+1] = (x[n] + 3) mod 8
```

Repeated substitution gives `x[n] = 3n mod 8`. The cycle is:

| n | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| x[n] | 0 | 3 | 6 | 1 | 4 | 7 | 2 | 5 | 0 |

## Exact cycle length by gcd

A return to the start after `k > 0` steps requires `3k = 0 mod 8`, or `8` divides `3k`. Since `gcd(3, 8) = 1`, the factor `3` is invertible modulo `8`; therefore `8` must divide `k`. The least positive such `k` is `8`, so the exact cycle length is eight.

In general, adding `a` on `Z/mZ` returns after the least positive `k` with `m | ak`. If `g = gcd(a, m)`, dividing by `g` leaves coprime factors, so the least such `k` is `m/g`. This is the additive order of `a` in the finite ring.

## Change the hop to four

Keep the same eight stations and start, but use `x[n+1] = (x[n] + 4) mod 8`:

```text
0 → 4 → 0 → 4 → ...
```

Here `gcd(4, 8) = 4`, so the cycle length is `8/4 = 2`. The hop visits only two opposite residues. The ring did not change; the increment did.

## Scope limit

This result is about deterministic addition on eight residue labels. “Station” is a picture for a residue, not a location, clock reading, material, or physical process. The gcd formula determines cycles for this finite rule; it does not establish that a real system has eight states, advances by a fixed hop, or follows modular arithmetic. A different update rule or state space requires a separate derivation.
