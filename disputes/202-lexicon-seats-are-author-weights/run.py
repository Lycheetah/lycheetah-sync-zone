# Falsifier: if kappa measured two seats' independent behaviour, it could not be driven to any value by editing the
# author's own scorer constants. It can.
import sys, importlib.util
sys.dont_write_bytecode = True
P = "/home/guestpc/lycheetah-sync-zone/experiments/lexicon-consistency-eval/eval_lexicon.py"
spec = importlib.util.spec_from_file_location("el", P); el = importlib.util.module_from_spec(spec)
sys.modules["el"] = el; spec.loader.exec_module(el)
def k():
    r = el.run_evaluation(); return r["ungrounded_aggregate"].cohens_kappa, r["grounded_aggregate"].cohens_kappa
print("as committed        ungrounded, grounded kappa:", k())
sA, sB = el.DuskenPoeticClassifier.classify_seat_a, el.DuskenPoeticClassifier.classify_seat_b
tA, tB = el.StairrelPoeticClassifier.classify_seat_a, el.StairrelPoeticClassifier.classify_seat_b
el.DuskenPoeticClassifier.classify_seat_b = staticmethod(sA); el.StairrelPoeticClassifier.classify_seat_b = staticmethod(tA)
print("Seat B := Seat A    ungrounded, grounded kappa:", k())
def sBw(f):
    return (1, 1.0, "always-yes")
el.DuskenPoeticClassifier.classify_seat_b = staticmethod(sBw)
print("Seat B := always 1  ungrounded, grounded kappa:", k())
el.DuskenPoeticClassifier.classify_seat_b = staticmethod(sB); el.StairrelPoeticClassifier.classify_seat_b = staticmethod(tB)
orig = el.StandingWaveStateMachine.evaluate.__func__
el.StandingWaveStateMachine.evaluate = classmethod(lambda cls, f, noise_offset=0.0: orig(cls, f, noise_offset=noise_offset*25))
print("Seat B noise x25    ungrounded, grounded kappa:", k())
