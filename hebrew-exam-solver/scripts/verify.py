#!/usr/bin/env python3
"""Verification helpers the agent MUST use before writing numbers into a solution.

Import in an ad-hoc script or REPL:
    from scripts.verify import *

Includes exact small-sample nonparametrics (sign test, Wilcoxon signed-rank via
enumeration) because homework problems are often DESIGNED to sit exactly where
the normal approximation and the exact test disagree.
"""
from itertools import combinations
from math import comb, sqrt

import numpy as np
from scipy import stats


# ---------- exact nonparametrics ----------

def sign_test_exact(n_pos: int, n_nonzero: int, alternative: str = "greater") -> float:
    """Exact sign-test p-value. Zeros must already be dropped."""
    k, n = n_pos, n_nonzero
    p_ge = sum(comb(n, i) for i in range(k, n + 1)) / 2**n
    p_le = sum(comb(n, i) for i in range(0, k + 1)) / 2**n
    if alternative == "greater":
        return p_ge
    if alternative == "less":
        return p_le
    return min(1.0, 2 * min(p_ge, p_le))


def wilcoxon_exact_pvalue(w_minus: float, n: int, alternative: str = "greater") -> float:
    """Exact P for Wilcoxon signed-rank with untied ranks 1..n (drop zeros first).

    alternative='greater' means H1: positive shift, i.e. small W-.
    Enumerates all 2^n sign assignments — fine for n <= ~20.
    """
    counts = {}
    ranks = list(range(1, n + 1))
    for r in range(n + 1):
        for subset in combinations(ranks, r):
            s = sum(subset)
            counts[s] = counts.get(s, 0) + 1
    total = 2**n
    if alternative == "greater":
        return sum(c for s, c in counts.items() if s <= w_minus) / total
    if alternative == "less":
        return sum(c for s, c in counts.items() if s >= w_minus) / total
    p1 = sum(c for s, c in counts.items() if s <= w_minus) / total
    p2 = sum(c for s, c in counts.items() if s >= w_minus) / total
    return min(1.0, 2 * min(p1, p2))


def wilcoxon_normal_approx(w_plus: float, n: int, ties: list[int] | None = None,
                           continuity: bool = False) -> tuple[float, float]:
    """(Z, one-sided p) for large-sample Wilcoxon. `ties` = sizes of tie groups."""
    mu = n * (n + 1) / 4
    var = n * (n + 1) * (2 * n + 1) / 24
    if ties:
        var -= sum(t**3 - t for t in ties) / 48
    z = (w_plus - mu - (0.5 if continuity else 0)) / sqrt(var)
    return z, 1 - stats.norm.cdf(z)


# ---------- classics ----------

def paired_t(d_mean: float, d_sd: float, n: int, mu0: float = 0.0,
             alternative: str = "greater") -> tuple[float, float]:
    t = (d_mean - mu0) / (d_sd / sqrt(n))
    df = n - 1
    if alternative == "greater":
        p = 1 - stats.t.cdf(t, df)
    elif alternative == "less":
        p = stats.t.cdf(t, df)
    else:
        p = 2 * (1 - stats.t.cdf(abs(t), df))
    return t, p


def t_ci(d_mean: float, d_sd: float, n: int, conf: float = 0.90) -> tuple[float, float]:
    tcrit = stats.t.ppf(1 - (1 - conf) / 2, n - 1)
    m = tcrit * d_sd / sqrt(n)
    return d_mean - m, d_mean + m


def merge_samples(n1: int, mean1: float, sd1: float,
                  n2: int, sum2: float, sumsq2: float) -> tuple[int, float, float]:
    """Merge (n1, mean, sd) summary with a raw (sum, sum of squares) batch."""
    s1 = n1 * mean1
    ss1 = (n1 - 1) * sd1**2 + n1 * mean1**2
    n, s, ss = n1 + n2, s1 + sum2, ss1 + sumsq2
    mean = s / n
    var = (ss - n * mean**2) / (n - 1)
    return n, mean, sqrt(var)


def chi2_homogeneity(table: np.ndarray) -> tuple[float, int, float]:
    """table: groups x categories observed counts."""
    chi2, p, dof, _ = stats.chi2_contingency(table, correction=False)
    return chi2, dof, p


def mcnemar_exact(n01: int, n10: int, alternative: str = "greater") -> float:
    """Exact McNemar via binomial on discordant pairs. 'greater': H1 favors 0->1."""
    return sign_test_exact(n01, n01 + n10, alternative)


def pearson_from_paired_sds(s_x: float, s_y: float, s_d: float) -> float:
    """r from Var(X-Y) = Var(X)+Var(Y)-2 r sx sy."""
    return (s_x**2 + s_y**2 - s_d**2) / (2 * s_x * s_y)


if __name__ == "__main__":
    # Regression tests against the three worked examples in examples/output/.
    assert abs(sign_test_exact(7, 9) - 46 / 512) < 1e-12
    assert abs(wilcoxon_exact_pvalue(11, 9) - 52 / 512) < 1e-12
    t, p = paired_t(1.16, 2.75, 11)
    assert abs(t - 1.399) < 0.01 and 0.05 < p < 0.10
    assert abs(pearson_from_paired_sds(0.092, 0.099, 0.046) - 0.886) < 0.005
    n, m, s = merge_samples(11, 1.16, 2.75, 3, 6, 14)
    assert n == 14 and abs(m - 1.34) < 0.01 and abs(s - 2.47) < 0.01
    assert abs(mcnemar_exact(10, 1) - 12 / 2048) < 1e-12
    print("All verification self-tests passed.")
