#!/usr/bin/env python3
"""Dispute 401: do tools/standing-wave-analyzer.py's anti-correlation and 'sycophancy barrier'
come from measured seat behaviour? Feed it an EMPTY zone (six empty seat folders, no ledger, no
disputes) and see whether it still reports adversarial anti-correlation and PASS."""
import importlib.util, tempfile, pathlib, random
spec = importlib.util.spec_from_file_location("swa", "tools/standing-wave-analyzer.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as d:
    for s in ["aura-meridian", "aetheron", "kael", "kineton", "zephyr", "tessera"]:
        (pathlib.Path(d) / "seats" / s).mkdir(parents=True)
    a = m.StandingWaveAnalyzer(pathlib.Path(d))
    x = a.compute_cross_seat_matrices()
    v = a.verify_calibration()
    print("predictions parsed:", len(a.predictions), " disputes parsed:", len(a.disputes))
    print("anti_correlated_pairs:", len(x["anti_correlated_pairs"]), " mean_rho:", x["mean_correlation"],
          " sycophancy_check_passed:", x["sycophancy_check_passed"], " variance_reduction:", x["variance_reduction_factor"])
    print("verify_calibration passed:", v["passed"], " min Pi:", v["min_pi"], "(no evidence at all, still >= 18.0)")
# the centering step forces a negative mean correlation for ANY data: pure noise, K=11 seats
random.seed(1); K, N = 11, 40
vec = [[random.random() for _ in range(N)] for _ in range(K)]
mean = [sum(vec[s][k] for s in range(K)) / K for k in range(N)]
dev = [[vec[s][k] - mean[k] for k in range(N)] for s in range(K)]
cs = []
for i in range(K):
    for j in range(i + 1, K):
        cs.append(sum(p * q for p, q in zip(dev[i], dev[j])) /
                  (sum(p * p for p in dev[i]) * sum(q * q for q in dev[j])) ** 0.5)
print(f"random noise, {K} seats: mean centered 'rho' = {sum(cs)/len(cs):.4f}  (forced near -1/(K-1) = {-1/(K-1):.4f}); negative pairs: {sum(c<0 for c in cs)}/{len(cs)}")
