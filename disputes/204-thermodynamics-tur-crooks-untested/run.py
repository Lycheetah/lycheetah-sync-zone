# Falsifier: if the tests check the Thermodynamic Uncertainty Relation, a bound that is obviously wrong must fail them.
import sys, unittest, importlib.util
sys.dont_write_bytecode = True
D = "/home/guestpc/lycheetah-sync-zone/experiments/thermodynamics/"
sys.path.insert(0, D)
import entropy_production as ep
def suite():
    s = unittest.defaultTestLoader.discover(D, pattern="test_entropy.py")
    r = unittest.TextTestRunner(stream=open("/dev/null","w")).run(s); return r.testsRun, len(r.failures)+len(r.errors)
print("committed          (run, failed):", suite())
orig = ep.MarkovNetwork.thermodynamic_uncertainty_bound
ep.MarkovNetwork.thermodynamic_uncertainty_bound = staticmethod(lambda mean_current, sigma, duration: 1e-9)
print("TUR bound := 1e-9  (run, failed):", suite())
ep.MarkovNetwork.thermodynamic_uncertainty_bound = staticmethod(lambda mean_current, sigma, duration: 1e9 if sigma>0 and duration>0 else 0.0)
print("TUR bound := 1e9   (run, failed):", suite())
ep.MarkovNetwork.thermodynamic_uncertainty_bound = orig
import math
# The Crooks test asserts exp(log(x)) == x; show that identity needs no network at all.
x = 3.7; print("exp(log(x)) == x for x=3.7, no network involved:", math.isclose(math.exp(math.log(x)), x, rel_tol=1e-12))
