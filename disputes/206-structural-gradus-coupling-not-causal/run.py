# Falsifier: if Euler-gradus coupling is what locks the sacred scale and leaves the dissonant one incoherent,
# replacing the gradus matrix with a constant matrix must change the locking outcome. It does not.
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/guestpc/lycheetah-sync-zone/experiments/structural-resonance")
import harmonic_kuramoto as hk
print("gradus coupling   :", hk.run_harmonic_kuramoto_benchmark())
orig = hk.compute_euler_gradus_coupling_matrix
def const(ratios, kappa=1.0, *a, **k):
    n = len(ratios); return [[kappa]*n for _ in range(n)]
hk.compute_euler_gradus_coupling_matrix = const
print("constant coupling :", hk.run_harmonic_kuramoto_benchmark())
hk.compute_euler_gradus_coupling_matrix = orig
