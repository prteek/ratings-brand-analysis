# ratings-brand-analysis

Is one product really rated better? Each product's 1★ to 5★ ratings are fitted with a beta-binomial model (users
differ in how much they like it), and two products are compared through the profile likelihood of the log odds
ratio of a favourable outcome. This repo holds everything for the blog post
[Is One Product Really Rated Better?](https://huggingface.co/blog/prteek/ratings-brand-analysis) on Hugging Face: the write-up,
its data, and an app built on the same model.

**Blog:** https://huggingface.co/blog/prteek/ratings-brand-analysis · **Live app:** https://huggingface.co/spaces/prteek/ratings-compare · **Data:** https://huggingface.co/datasets/prteek/ratings-compare
(the Hugging Face repos keep the name `ratings-compare`)

## Layout

```
ratings_compare/       shared package
  beta_binomial.py     single-product fit, profile likelihood, exact 95% likelihood interval (used by the app)
  data.py              loads data/ratings.csv; star counts per product
data/ratings.csv       the headphone ratings (published as the Hugging Face dataset)
blog/                  Quarto write-up -> markdown for the Hugging Face article editor
  index.qmd            the blog post; renders to ratings-brand-analysis.md, figures to assets/
  _hf-markdown.lua     writes inline maths as \\( ... \\) for the article editor
  thumbnail.png        the article's cover image
space/                 Gradio app (app.py), Space card and requirements
dataset/               dataset card
publish.sh             upload space and/or dataset
wait_for_space.py      wait until the Space runs its latest commit (used by CI)
tests/                 model checks against the original write-up's numbers, and the app's default example against the data
```

The blog post, the app and the tests all use `ratings_compare`, which finds the interval ends exactly; the original
write-up read them off a 20-point grid, and the two agree within 0.05.

## Common tasks

```bash
uv sync                                                    # package + app + blog + dev groups
uv run pytest -q

QUARTO_PYTHON=.venv/bin/python quarto render blog/index.qmd # blog markdown + assets/ figures (~10 s)
uv run python space/app.py                                 # app on http://127.0.0.1:7860
./publish.sh "message" space                               # publish (targets: space, dataset; default both)
```

## Publishing from CI

Pushes to `main` publish to Hugging Face with the `HF_TOKEN` repository secret (both workflows can also be run by
hand):

- `publish-space.yml`: when the app or `ratings_compare/` changes; runs the tests, uploads, and waits until the
  Space runs the new commit (restarting it once if the upload didn't trigger a rebuild)
- `publish-dataset.yml`: when `data/ratings.csv` or the dataset card changes

Data: a subset of the Electronics ratings from Wan, Ni, Misra & McAuley (2020), *Addressing Marketing Bias in Product
Recommendations*, WSDM ([github.com/MengtingWan/marketBias](https://github.com/MengtingWan/marketBias), Apache-2.0).
