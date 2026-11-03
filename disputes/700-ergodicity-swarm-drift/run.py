"""
Numerical verification script for Dispute 700: Swarm Ergodicity Fallacy.
Verifies whether ensemble average diverges from time average in autonomous multi-agent dynamics.
"""

import math
import sys
from pathlib import Path

# Insert code directory
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_path / "code"))

from importlib import import_module
engine_module = import_module("16_celestial_orrery_topological_mapper")
CelestialOrreryMapper = engine_module.CelestialOrreryMapper

def verify_ergodic_fallacy():
    mapper = CelestialOrreryMapper(str(root_path))
    # Run test with mu = 0.05, sigma = 0.40 -> mu - 0.5 * sigma^2 = 0.05 - 0.08 = -0.03 < 0
    res = mapper.evaluate_ergodic_drift(ensemble_size=500, timesteps=150, mu=0.05, sigma=0.40)
    
    print(f"Ensemble Growth (Theoretical): {res['theoretical_ensemble_growth']:.4f}")
    print(f"Time Growth (Theoretical):     {res['theoretical_time_growth']:.4f}")
    print(f"Ergodic Gap:                   {res['theoretical_ergodic_gap']:.4f}")
    print(f"Empirical Ensemble Mean:       {res['empirical_ensemble_mean']:.4f}")
    print(f"Empirical Time Mean:           {res['empirical_time_mean']:.4f}")
    print(f"System Classification:         {res['conclusion']}")

    # Condition: Ensemble grows while individual paths contract
    is_fallacy_proven = (res['theoretical_ensemble_growth'] > 1.0 and 
                         res['theoretical_time_growth'] < 1.0 and 
                         res['is_non_ergodic'])
    return is_fallacy_proven

if __name__ == "__main__":
    if verify_ergodic_fallacy():
        print("PASS: Dispute 700 verified. Naive self-referential swarm ergodicity falls.")
        sys.exit(0)
    else:
        print("FAIL: Dispute 700 verification failed.")
        sys.exit(1)
