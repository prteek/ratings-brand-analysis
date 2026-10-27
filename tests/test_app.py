import importlib.util
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location("app", Path(__file__).parents[1] / "space/app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def test_percentages_give_counts_that_add_up_to_the_total():
    # as Amazon shows them: rounded percentages that sum to 99
    counts = app.counts_from_percentages(76, [14, 14, 11, 17, 43])
    assert abs(counts.sum() - 76) <= 2  # rounding each star can shift the total slightly
    assert np.allclose(counts, [11, 11, 8, 13, 33], atol=1)


def test_default_percentages_round_trip_to_the_default_counts():
    for _, counts in (app.DEFAULT_A, app.DEFAULT_B):
        back = app.counts_from_percentages(sum(counts), app.default_percentages(counts))
        assert np.allclose(back, counts, atol=1)


def test_empty_percentages_give_no_ratings():
    assert app.counts_from_percentages(100, [0, 0, 0, 0, 0]).sum() == 0


def test_both_modes_give_the_same_verdict_for_the_default_example():
    counts = [*app.DEFAULT_A[1], *app.DEFAULT_B[1]]
    pct = [sum(app.DEFAULT_A[1]), *app.default_percentages(app.DEFAULT_A[1]),
           sum(app.DEFAULT_B[1]), *app.default_percentages(app.DEFAULT_B[1])]
    by_counts = app.run(app.MODES[0], "A", "B", *counts, *pct)
    by_pct = app.run(app.MODES[1], "A", "B", *counts, *pct)
    assert by_counts[0].split("\n")[0] == by_pct[0].split("\n")[0]
    assert app.run(app.MODES[1], "A", "B", *counts, 0, 0, 0, 0, 0, 0, *pct[6:])[0].startswith("Enter at least")
