"""The headphone ratings behind the paper (data/ratings.csv), published as the Hugging Face dataset.

A subset of the Electronics ratings from Wan, Ni, Misra & McAuley (2020), "Addressing Marketing Bias in Product
Recommendations", WSDM (github.com/MengtingWan/marketBias, Apache-2.0): every Headphones rating of the brands
Philips, Jabra and Apple. Ratings are 1-5 stars.
"""
from pathlib import Path

import pandas as pd

RATINGS = Path(__file__).resolve().parents[1] / "data" / "ratings.csv"
# The two products the paper compares
APPLE, PHILIPS = 4501, 3700


def load(path: Path = RATINGS) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["timestamp"])


def star_counts(ratings: pd.DataFrame, item_id: int) -> list[int]:
    """Number of 1★ … 5★ ratings of one product."""
    stars = ratings.loc[ratings["item_id"] == item_id, "rating"].round().astype(int)
    return [int((stars == s).sum()) for s in range(1, 6)]
