"""Every number quoted in Episode 1, computed from scratch -> data/facts.json.

    python compute/facts.py
"""
import json, sys
from math import log, log10, sqrt, exp
from pathlib import Path
import numpy as np
from scipy.special import gammaln
from scipy.stats import binom, gamma

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from common.coins import log_tail, log_bell_tail, rate, entropy, LN10  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "facts.json"
rng = np.random.default_rng(2026)
N = 1000
F = {"n": N}

# 1. The cold open: exact tail vs bell curve vs e^{-nI}
tails = {}
for k in (600, 700, 900):
    ex, be, ld = log_tail(N, k) / LN10, log_bell_tail(N, k) / LN10, -N * rate(k / N) / LN10
    tails[k] = dict(exact=ex, bell=be, ld=float(ld), bell_over_exact=be - ex, I=float(rate(k / N)))
F["tails"] = tails

# 2. Typical fluctuations
sd = sqrt(N) / 2
lo, hi = binom.ppf(0.025, N, 0.5), binom.ppf(0.975, N, 0.5)
F["typical"] = dict(sd=sd, lo95=int(lo), hi95=int(hi), sigmas_700=(700 - 500) / sd, sigmas_900=(900 - 500) / sd)

# 3. "Each extra coin divides the chance by the same factor"
F["per_coin_factor"] = {str(x): exp(float(rate(x))) for x in (0.6, 0.7, 0.9)}

# 4. Counting sequences
lc = lambda k: (gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1)) / LN10
F["counts_log10"] = {"total": N * log10(2), "500": lc(500), "700": lc(700), "900": lc(900)}
F["entropy"] = {str(x): float(entropy(x)) for x in (0.5, 0.7, 0.9)}

# 5. Naive simulation: a million experiments of 1000 flips
M = 10**6
heads = rng.binomial(N, 0.5, size=M)
F["naive"] = dict(experiments=M, max_heads=int(heads.max()), hits600=int((heads >= 600).sum()),
                  hits700=int((heads >= 700).sum()), hits550=int((heads >= 550).sum()))

# 6. Importance sampling with a rigged coin (10 000 experiments)
imp = {}
for k, q in ((700, 0.7), (900, 0.9)):
    K = 10**4
    h = rng.binomial(N, q, size=K)
    logw = h * log(0.5 / q) + (N - h) * log(0.5 / (1 - q))      # likelihood ratio fair / rigged
    hit = h >= k
    w = np.where(hit, np.exp(logw - logw[hit].max()), 0.0)
    est = log(w.mean()) + logw[hit].max()
    rel = w.std(ddof=1) / sqrt(K) / w.mean()
    imp[k] = dict(q=q, experiments=K, hit_fraction=float(hit.mean()), estimate_log10=est / LN10,
                  exact_log10=tails[k]["exact"], rel_error=float(rel),
                  weight_per_head_log10=log10(0.5 / q), weight_per_tail_log10=log10(0.5 / (1 - q)))
F["importance"] = imp

# 7. How 700 heads happens: random arrangements with exactly 700 heads
def longest_run(a):
    best = cur = 0
    for v in a:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best

runs, wmin, wmax = [], [], []
for _ in range(2000):
    a = np.zeros(N, bool); a[rng.choice(N, 700, replace=False)] = True
    runs.append(longest_run(a))
    win = a.reshape(10, 100).mean(axis=1)
    wmin.append(win.min()); wmax.append(win.max())
fair_runs = [longest_run(rng.random(N) < 0.5) for _ in range(2000)]
F["conspiracy"] = dict(longest_run_mean=float(np.mean(runs)), longest_run_fair_mean=float(np.mean(fair_runs)),
                       window100_min_mean=float(np.mean(wmin)), window100_max_mean=float(np.mean(wmax)))

# 8. Light tails vs heavy tails: 100 claims of mean 1, total at least 200
n, T, alpha = 100, 200.0, 2.5
xm = (alpha - 1) / alpha                                    # Pareto minimum giving mean 1
# light: exponential claims; given the total, the claims are uniform on the simplex
E = rng.dirichlet(np.ones(n), size=20000) * T
emax = E.max(axis=1)
# heavy: Pareto claims, rejection sampling on total >= 200
acc, tried = [], 0
while len(acc) < 400:
    B = (rng.pareto(alpha, size=(200000, n)) + 1) * xm
    tried += B.shape[0]
    acc.extend(B[B.sum(axis=1) >= T])
P = np.array(acc)
pmax = P.max(axis=1)
med_others = lambda X: np.median(np.sort(X, axis=1)[:, :-1], axis=1)
F["tails_kind"] = dict(
    n=n, total=T, alpha=alpha, xm=xm,
    light=dict(largest_mean=float(emax.mean()), largest_share=float((emax / E.sum(1)).mean()),
               median_others=float(np.median(med_others(E))), mean_claim=float(E.mean()),
               prob_log10=float(gamma.logsf(T, n) / LN10)),
    heavy=dict(largest_mean=float(pmax.mean()), largest_median=float(np.median(pmax)),
               largest_share=float(np.median(pmax / P.sum(1))),
               median_others=float(np.median(med_others(P))), prob=len(acc) / tried,
               one_big_jump=float(n * (xm / (T - n)) ** alpha)))
# one representative sample of each kind (median largest share), for the bar charts
def representative(X):
    s = X.max(1) / X.sum(1)
    return X[np.argsort(s)[len(s) // 2]]
samples = {"light": representative(E).round(4).tolist(), "heavy": representative(P).round(4).tolist()}
(OUT.parent / "claims.json").write_text(json.dumps(samples))

# 8b. Height of the 700-heads bar relative to the 500-heads bar (for the "invisible bar" remark)
from common.coins import log_binom_pmf  # noqa: E402
F["bar700_rel_log10"] = float((log_binom_pmf(N, 700) - log_binom_pmf(N, 500)) / LN10)
F["bar700_metres_if_peak_30cm"] = 0.3 * 10 ** F["bar700_rel_log10"]
F["planck_length_m"] = 1.616e-35

# 9. Gas in a box: probability that all N molecules are in the left half
F["gas"] = {"10": -10 * log10(2), "100": -100 * log10(2), "1e23": -1e23 * log10(2)}

OUT.write_text(json.dumps(F, indent=1))
print(json.dumps(F, indent=1))
