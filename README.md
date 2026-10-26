# ratings-compare

Is one product really rated better? Each product's 1★ to 5★ ratings are fitted with a beta-binomial model (users
differ in how much they like it), and two products are compared through the profile likelihood of the log odds
ratio of a favourable outcome. This repo holds everything for the paper
[Ratings ~ Brand, Analysis](https://www.alphaxiv.org/abs/2610.ratings-brand-analysis) on alphaXiv: the write-up,
its data, and an app built on the same model.

**Live app:** https://huggingface.co/spaces/prteek/ratings-compare · **Data:** https://huggingface.co/datasets/prteek/ratings-compare

## Layout

```
ratings_compare/       shared package
  beta_binomial.py     single-product fit, profile likelihood, exact 95% likelihood interval (used by the app)
  data.py              loads data/ratings.csv; star counts per product
data/ratings.csv       the headphone ratings (published as the Hugging Face dataset)
paper/                 Quarto write-up -> PDF for alphaXiv
  index.qmd            the paper (Python; reads ratings.csv, a link to data/ratings.csv)
  _quarto.yml          PDF format; renders to paper/_output/ratings-brand-analysis.pdf
  _freeze/             frozen results of the paper's code (tracked; its bootstrap test is unseeded)
  references.bib, ratings.png, _wide-tables.lua
huggingface/
  space/               Gradio app (app.py), Space card and requirements
  dataset/             dataset card
  publish.sh           upload space and/or dataset
  wait_for_space.py    wait until the Space runs its latest commit (used by CI)
tests/                 model checks against the paper, and the app's default example against the data
```

The paper keeps its own inline implementation (a 20-point grid for the profile likelihood), exactly as published;
the app's `beta_binomial.py` finds the interval ends exactly and agrees with the paper within 0.05.

## Common tasks

```bash
uv sync                                                    # package + app + paper + dev groups
uv run pytest -q

QUARTO_PYTHON=.venv/bin/python quarto render paper         # paper PDF from the frozen results
uv run python huggingface/space/app.py                     # app on http://127.0.0.1:7860
huggingface/publish.sh "message" space                     # publish (targets: space, dataset; default both)
```

## Publishing from CI

Pushes to `main` publish to Hugging Face with the `HF_TOKEN` repository secret (both workflows can also be run by
hand):

- `publish-space.yml`: when the app or `ratings_compare/` changes; runs the tests, uploads, and waits until the
  Space runs the new commit (restarting it once if the upload didn't trigger a rebuild)
- `publish-dataset.yml`: when `data/ratings.csv` or the dataset card changes

Data: a subset of the Electronics ratings from Wan, Ni, Misra & McAuley (2020), *Addressing Marketing Bias in Product
Recommendations*, WSDM ([github.com/MengtingWan/marketBias](https://github.com/MengtingWan/marketBias), Apache-2.0).
