import numpy as np

from ratings_compare.beta_binomial import CHI2_95, compare, fit_product, profile_loglik

# Apple (item 4501) and Philips (item 3700) headphones, 1..5 star counts, as in the paper
APPLE = [11, 11, 8, 13, 33]
PHILIPS = [2, 4, 7, 9, 16]


def test_single_product_matches_paper():
    fit = fit_product(APPLE)
    assert np.isclose(fit.alpha, 0.6689, atol=2e-3)
    assert np.isclose(fit.beta, 0.3553, atol=2e-3)
    assert np.allclose(fit.fitted_counts(), [11.5, 9.1, 9.7, 12.8, 32.9], atol=0.1)


def test_comparison_matches_paper():
    c = compare(APPLE, PHILIPS)
    # the paper read these off a 20-point grid: MLE 0.316, 95% CI [-0.261, 0.893]
    assert abs(c.theta - 0.316) < 0.06
    assert abs(c.ci[0] - (-0.261)) < 0.06 and abs(c.ci[1] - 0.893) < 0.06
    assert not c.excludes_zero


def test_interval_ends_sit_on_threshold():
    c = compare(APPLE, PHILIPS)
    ll_max = c.a.loglik + c.b.loglik
    for end in c.ci:
        assert np.isclose(2 * (ll_max - profile_loglik(end, c.a, c.b)), CHI2_95, atol=1e-3)
    assert np.isclose(c.profile_loglik.max(), 0, atol=1e-2)


def test_clear_difference_is_detected():
    c = compare([30, 20, 10, 5, 5], [2, 3, 10, 25, 40])
    assert c.theta > 0 and c.excludes_zero


def test_identical_products_give_zero():
    c = compare(APPLE, APPLE)
    assert abs(c.theta) < 1e-6 and not c.excludes_zero


def test_extreme_counts_do_not_crash():
    c = compare([0, 0, 0, 0, 5], [5, 0, 0, 0, 0])
    assert c.theta < 0
    assert np.all(np.isfinite(c.profile_loglik))
