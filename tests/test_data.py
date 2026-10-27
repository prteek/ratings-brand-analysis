from ratings_compare.data import APPLE, PHILIPS, load, star_counts


def test_dataset_shape():
    r = load()
    assert len(r) == 7681
    assert set(r["brand"]) == {"Philips", "Jabra", "Apple"}
    assert r["rating"].between(1, 5).all()


def test_app_default_example_matches_the_data():
    """The app opens with the blog post's two products; their counts must come from the published data."""
    import importlib.util
    from pathlib import Path

    spec = importlib.util.spec_from_file_location("app", Path(__file__).parents[1] / "space/app.py")
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)
    r = load()
    assert app.DEFAULT_A[1] == star_counts(r, APPLE)
    assert app.DEFAULT_B[1] == star_counts(r, PHILIPS)
