# ratings-compare

Gradio app that answers "is one product really rated better?" from the 1★ to 5★ rating counts of two products.
Each product is fitted with a beta-binomial model and the two are compared through the profile likelihood of the
log odds ratio of a favourable outcome. Method from the blog post
[ratings ~ brand](https://prteek.github.io/regression_room/posts/ratings_inference/).

Live: [huggingface.co/spaces/prteek/ratings-compare](https://huggingface.co/spaces/prteek/ratings-compare)

- `beta_binomial.py`: the model (single-product fit, profile likelihood, 95% likelihood interval)
- `app.py`: the Gradio app
- `tests/`: checks against the post's numbers and edge cases
- `hf/`: Space card, requirements and `publish.sh`

```bash
uv run python app.py                 # run locally on http://127.0.0.1:7860
uv run --group dev pytest -q tests   # tests
hf/publish.sh "message"              # upload to the Space
```
