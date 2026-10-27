# Decisions

- **2026-10-26: Design agreed with the user.** Inputs are star counts for two products (five boxes each), 1–5
  stars only, opening with the paper's Apple vs Philips headphones. Outputs: a plain-language verdict with the odds
  ratio and its 95% likelihood interval, the profile likelihood plot, and a fit check (observed vs fitted counts,
  each product's Beta distribution of preference). The paper's bootstrap baseline was left out. Hosted like
  sparse-panel-demo: public GitHub repo plus a Gradio Space with the Plotly ggplot2 theme.
- **Exact interval instead of a grid.** The 95% interval ends are found by root-finding where the likelihood-ratio
  statistic reaches the chi-squared threshold. The paper read them off a 20-point grid; results agree within 0.05.
- **Joint MLE from separate fits.** theta only re-expresses p_B, so the joint maximum is the two single-product
  fits; the profile only needs maximising for fixed theta (two starting points, best kept).
- **Unbounded intervals are reported, not hidden.** With few ratings or all ratings at one end, a U-shaped Beta
  fits any odds ratio; the app then says the ratings can't pin down a difference.
- **Reference lines drawn as traces.** Vertical shapes on a log axis didn't render in gr.Plot, so the threshold,
  equal-preference, best-fit and interval lines are line traces.
- **2026-10-26: Paper and dataset moved in** — regression_room is being split into one repo per post. The ratings write-up now lives in `paper/` (verbatim) with its frozen results, so the unseeded bootstrap keeps the published numbers; the re-rendered PDF matches the published one (73 numbers, 1,576 words). The app's model moved into the `ratings_compare` package; the paper keeps its own inline grid-based code rather than importing it, because switching to exact root-finding would change the paper's numbers.
- **`data/ratings.csv` is the single copy of the data** — the paper reads it through the link `paper/ratings.csv`, the tests check the app's default example against it, and CI publishes it as the Hugging Face dataset `prteek/ratings-compare`. The source repository (MengtingWan/marketBias) is Apache-2.0, so the subset is shared under Apache-2.0 with attribution.
- **CI publishes the Space and the dataset** — same pattern as sparse-panel-modelling; the Space job runs the tests first and the upload includes the `ratings_compare` package next to `app.py`.
- **2026-10-27: Blog only, paper retired** — the write-up is now a Hugging Face community article (huggingface.co/blog/prteek/ratings-brand-analysis) rendered from the single `blog/index.qmd` to markdown, with figures in `blog/assets/` that are uploaded in the article editor; `paper/` (PDF for alphaXiv, frozen results) is removed and every link points to the blog. The post uses `ratings_compare` like the app, so its numbers come from exact root-finding (theta 0.300, 95% interval [-0.303, 0.911]) rather than the paper's 20-point grid (0.316, [-0.261, 0.893]). The bootstrap is seeded and reports the 95% interval of the difference in means: the paper's p-value compared the bootstrap distribution, which is centred on the observed difference rather than zero, so it sat near 0.5 whatever the data. The paper's approximate probability ratio (square root of the odds ratio) is replaced by the ratio of fitted mean preferences, and the preference range uses Beta quantiles instead of mean ± 1.96 SD (which ran outside [0, 1]). Test names that say `paper` are kept: they check against the original write-up's numbers.
- **2026-10-27: No `huggingface/` folder** — `space/`, `dataset/`, `publish.sh` and `wait_for_space.py` sit at the repo root, as in sparse-panel-modelling; the workflows, `publish.sh` and the tests use the new paths.
