"""Beta-binomial comparison of two products' 1–5 star ratings.

Following the paper "Ratings ~ Brand, Analysis" (www.alphaxiv.org/abs/2610.ratings-brand-analysis):
- a rating of s stars is treated as k = s - 1 favourable outcomes out of N = 4;
- each user's preference p is drawn from Beta(alpha, beta) for that product, so ratings are beta-binomial;
- each product is parameterised by its mean preference p = alpha / (alpha + beta) and dispersion d = alpha + beta;
- the comparison targets theta = logit(p_B) - logit(p_A), the log odds ratio of a favourable outcome, and is
  inferred from its profile likelihood (nuisance parameters p_A, d_A, d_B maximised out).
"""
from dataclasses import dataclass

import numpy as np
from scipy import optimize, stats
from scipy.special import betaln, expit, gammaln, logit

N = 4  # five stars -> 0..4 favourable outcomes
STARS = np.arange(N + 1)
LOGIT_P = (-9.0, 9.0)                  # keeps p inside (1e-4, 1 - 1e-4)
LOG_D = (np.log(1e-2), np.log(1e4))    # d -> large is the plain binomial (no spread between users)
CHI2_95 = stats.chi2.ppf(0.95, df=1)


def log_pmf(alpha: float, beta: float) -> np.ndarray:
    """Beta-binomial log-probability of 0..N favourable outcomes."""
    k = STARS
    log_comb = gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1)
    return log_comb + betaln(k + alpha, N - k + beta) - betaln(alpha, beta)


def loglik(counts: np.ndarray, p: float, d: float) -> float:
    return float(np.dot(counts, log_pmf(p * d, (1 - p) * d)))


@dataclass
class ProductFit:
    counts: np.ndarray
    p: float      # mean preference
    d: float      # dispersion alpha + beta
    loglik: float

    @property
    def alpha(self) -> float:
        return self.p * self.d

    @property
    def beta(self) -> float:
        return (1 - self.p) * self.d

    @property
    def mean_stars(self) -> float:
        return 1 + N * self.p

    def fitted_counts(self) -> np.ndarray:
        return self.counts.sum() * np.exp(log_pmf(self.alpha, self.beta))


def fit_product(counts) -> ProductFit:
    counts = np.asarray(counts, float)
    start_p = np.clip(np.dot(counts, STARS) / (N * counts.sum()), 0.01, 0.99)
    res = optimize.minimize(lambda x: -loglik(counts, expit(x[0]), np.exp(x[1])),
                            x0=[logit(start_p), np.log(2.0)], bounds=[LOGIT_P, LOG_D], method="L-BFGS-B")
    return ProductFit(counts, float(expit(res.x[0])), float(np.exp(res.x[1])), -float(res.fun))


@dataclass
class Comparison:
    a: ProductFit
    b: ProductFit
    theta: float                 # MLE of logit(p_B) - logit(p_A)
    ci: tuple                    # 95% likelihood interval; an end is None if it runs off the search range
    profile_theta: np.ndarray
    profile_loglik: np.ndarray   # profile log-likelihood minus its maximum (0 at the MLE)

    @property
    def odds_ratio(self) -> float:
        return float(np.exp(self.theta))

    @property
    def excludes_zero(self) -> bool:
        lo, hi = self.ci
        return (lo is not None and lo > 0) or (hi is not None and hi < 0)


def profile_loglik(theta: float, a: ProductFit, b: ProductFit) -> float:
    """Maximise the joint log-likelihood over (p_A, d_A, d_B) with theta fixed; p_B follows from theta."""
    def neg(x):
        la, log_da, log_db = x
        return -(loglik(a.counts, expit(la), np.exp(log_da))
                 + loglik(b.counts, expit(np.clip(la + theta, *LOGIT_P)), np.exp(log_db)))

    starts = [[logit(a.p), np.log(a.d), np.log(b.d)],
              [np.clip(logit(b.p) - theta, *LOGIT_P), np.log(a.d), np.log(b.d)]]
    best = min((optimize.minimize(neg, x0=s, bounds=[LOGIT_P, LOG_D, LOG_D], method="L-BFGS-B") for s in starts),
               key=lambda r: r.fun)
    return -float(best.fun)


def compare(counts_a, counts_b, search: float = 12.0, n_grid: int = 61) -> Comparison:
    a, b = fit_product(counts_a), fit_product(counts_b)
    theta_hat = float(logit(b.p) - logit(a.p))
    ll_max = a.loglik + b.loglik  # the joint MLE is the two separate fits: theta only re-expresses p_B

    def excess(t):  # zero where the likelihood-ratio statistic reaches the 95% threshold
        return 2 * (ll_max - profile_loglik(t, a, b)) - CHI2_95

    def bound(direction):
        step, inner = 0.25, theta_hat
        while abs(inner + direction * step - theta_hat) <= search:
            outer = inner + direction * step
            if excess(outer) > 0:
                return float(optimize.brentq(excess, inner, outer, xtol=1e-4) if direction > 0
                             else optimize.brentq(excess, outer, inner, xtol=1e-4))
            inner, step = outer, step * 1.6
        return None

    lo, hi = bound(-1), bound(+1)
    left = (lo if lo is not None else theta_hat - 3) - 0.5
    right = (hi if hi is not None else theta_hat + 3) + 0.5
    grid = np.linspace(left, right, n_grid)
    prof = np.array([profile_loglik(t, a, b) for t in grid]) - ll_max
    return Comparison(a, b, theta_hat, (lo, hi), grid, prof)
