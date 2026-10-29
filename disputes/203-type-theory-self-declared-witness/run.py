# Falsifier: a MEASURED witness pointing at an artifact that does not exist must fail typecheck, and a DERIVED
# witness whose conclusion names a different proposition must fail. Observed: both typecheck.
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/guestpc/lycheetah-sync-zone/experiments/type-theory")
from witness_typecheck import *
tc = TypeChecker()
p = Prop("ghost_claim", "Pi = 9999 at /nonexistent/never_ran.txt", EpistemicStatus.MEASURED)
w = MeasuredWitness("/nonexistent/never_ran.txt", "Pi", expected_val=9999, actual_val=9999)
try: print("MEASURED, artifact missing, actual:=expected  ->", tc.typecheck(SigmaPair(p, w)))
except TypeError as e: print("rejected:", e)
w2 = MeasuredWitness("/nonexistent/never_ran.txt", "Pi", expected_val=1.0, actual_val=2.0)
try: tc.typecheck(SigmaPair(p, w2)); print("unexpected accept")
except TypeError: print("MEASURED, expected != actual (caller-supplied)  -> rejected (the only thing verify() can see)")
base = Prop("base", "premise", EpistemicStatus.MEASURED)
bw = MeasuredWitness("x", "m", 1, 1)
prem = SigmaPair(base, bw)
d = Prop("goal", "anything at all", EpistemicStatus.DERIVED)
dw = DerivedWitness("magic", (prem,), "some_other_name_entirely")
try: print("DERIVED, rule='magic', conclusion_name mismatched ->", tc.typecheck(SigmaPair(d, dw)))
except TypeError as e: print("rejected:", e)
