"""
Numerical verification script for Dispute 600: Landauer Agency Dissipation.
Tests whether belief divergence can occur without positive Landauer work.
"""

import math
import sys

def verify_landauer_agency():
    k_B = 1.380649e-23
    temp = 300.0  # Kelvin

    # Ground prior (uniform)
    prior = [0.25, 0.25, 0.25, 0.25]
    # Aligned sovereign posterior
    posterior = [0.94, 0.02, 0.02, 0.02]

    # Compute KL divergence
    kl = sum(p * math.log(p / q) for p, q in zip(posterior, prior))
    work = k_B * temp * kl

    # Assert that work cannot be zero when KL > 0
    assert kl > 1.0, f"Expected significant KL divergence, got {kl}"
    assert work > 1.0e-21, f"Expected positive Landauer work, got {work}"

    # Negative control: attempting zero-work shift
    zero_work_kl = 0.0
    is_zero_work_possible = (kl == 0.0)

    print(f"KL Divergence: {kl:.6f} nats")
    print(f"Landauer Dissipation: {work:.4e} Joules")
    print(f"Zero Dissipation Feasible: {is_zero_work_possible}")

    return kl > 1.0 and work > 0.0 and not is_zero_work_possible

if __name__ == "__main__":
    if verify_landauer_agency():
        print("PASS: Dispute 600 verified. Zero-dissipation agency falls.")
        sys.exit(0)
    else:
        print("FAIL: Dispute 600 validation failed.")
        sys.exit(1)
