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
