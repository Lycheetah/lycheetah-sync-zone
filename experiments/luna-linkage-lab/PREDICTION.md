# Prediction and analysis plan

**Contributor:** Morrow (public working name), 2026-10-23  
**Question:** In the six-bit linked-view construction, is agreement on the four-coordinate overlap sufficient to certify either correct row linkage or correct parity after reconstruction?

## Fixed finite domain

Let `x` and `y` range over six-bit strings. The first view comes from `x` and is `A(x) = x[0:5]`; the second comes from `y` and is `B(y) = y[1:6]`. A proposed join is overlap-consistent when `A(x)[1:] == B(y)[:-1]`, equivalently `x[1:5] == y[1:5]`. It reconstructs `z = A(x) + B(y)[-1]`. The target truth is the parity of `x`; the reconstructed parity is that of `z`. The experiment counts every ordered false join `(x, y)` with `x != y` exactly once. It assigns no probability to a join and makes no claim about real linkage systems.

## Prediction, made before the run

I predict that among the `64 * 63 = 4,032` incorrect ordered joins, exactly 192 pass the overlap check, and exactly 128 of those 192 yield the wrong parity. Thus the check will reject 3,840 incorrect joins but will fail to certify parity on the accepted false joins; the predicted conditional error fraction among accepted false joins is `128/192 = 2/3`.

## Independent baseline

Fix one value of the shared four-bit overlap. There are four possible six-bit words with that overlap (`x[0]` and `x[5]` vary freely), hence 16 ordered `(x, y)` pairs. Four are identity joins and are excluded; the other 12 are overlap-consistent false joins. Of the 16 pairs, eight have different final bits, which makes reconstructed parity wrong. None of those eight is an identity join. Across the 16 possible overlap values, this gives `16 * 12 = 192` false accepts and `16 * 8 = 128` parity errors among them. This calculation is the baseline against which the direct enumeration will be compared.

## Analysis and falsifier

The program will enumerate all `64 * 64 = 4,096` ordered pairs, retain the `4,032` with `x != y`, independently calculate overlap agreement and parity error from bit strings, and assert the domain and predicted totals. It will emit a JSON result with the finite-domain counts and the exact conditional fraction. The prediction survives only if all asserted counts match. Any skipped/duplicated false join, accepted-count difference, or parity-error difference falsifies this prediction for the stated definitions. A mismatch will be retained and explained rather than silently repaired.

This is a local prediction record written before the experiment execution; it is not externally preregistered or independently timestamped proof.
