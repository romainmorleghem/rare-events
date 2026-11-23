"""Exact coin-flip mathematics used by the scenes, the fact sheet and the web page."""
import numpy as np
from math import lgamma, log, sqrt, erfc

LN10 = log(10.0)


def log_binom_pmf(n, k, p=0.5):
    """Natural log of P(k heads out of n), vectorised over k."""
    k = np.asarray(k, dtype=float)
    from scipy.special import gammaln
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1) + k * np.log(p) + (n - k) * np.log1p(-p)


def log_tail(n, k, p=0.5):
    """Natural log of P(at least k heads out of n)."""
    ls = log_binom_pmf(n, np.arange(k, n + 1), p)
    m = ls.max()
    return float(m + np.log(np.exp(ls - m).sum()))


def rate(x, p=0.5):
    """Rate function of the coin: I(x) = x ln(x/p) + (1-x) ln((1-x)/(1-p))."""
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(x > 0, x * np.log(np.where(x > 0, x, 1) / p), 0.0)
        b = np.where(x < 1, (1 - x) * np.log(np.where(x < 1, 1 - x, 1) / (1 - p)), 0.0)
    return a + b


def entropy(x):
    """Shannon entropy (natural log) of a coin with heads-probability x."""
    return np.log(2) - rate(x, 0.5)


def log_bell_tail(n, k, p=0.5):
    """Natural log of the bell-curve (CLT) estimate of P(at least k heads), with continuity correction."""
    import mpmath as mp
    z = (k - 0.5 - n * p) / sqrt(n * p * (1 - p))
    return float(mp.log(0.5 * mp.erfc(z / mp.sqrt(2))))


def log_bell_pmf(n, k, p=0.5):
    """Natural log of the bell-curve density at k (the CLT approximation of each bar)."""
    s2 = n * p * (1 - p)
    k = np.asarray(k, dtype=float)
    return -0.5 * np.log(2 * np.pi * s2) - (k - n * p) ** 2 / (2 * s2)
