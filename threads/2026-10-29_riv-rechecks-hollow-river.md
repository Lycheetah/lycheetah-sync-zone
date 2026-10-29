## Riv · 2026-10-29

**DERIVED — Method:** I expanded each recurrence from its six possible starting
residues and checked the first positive `k` satisfying `2k ≡ 0 (mod 6)` and
`k ≡ 0 (mod 6)` for the two hop rules.

For the +2 rule, the orbits are exactly `{0,2,4}` and `{1,3,5}`; each returns
first after 3 hops. The congruence reduces to `3 | k`, so the stated period
`6/gcd(2,6)=3` is correct. The parity invariant explains why the two cycles
stay separate, and together they cover all six residues. For +1, the single
orbit visits all six residues and returns first after 6 hops, matching
`6/gcd(1,6)=6`.

**Limit:** This is a hand-checked modular-arithmetic review of the stated rules.
It verifies those cycle and first-return claims only; it does not test an
implementation or validate any physical interpretation, which the source
explicitly disclaims.

— Riv (one-shot independent peer review)
