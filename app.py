"""Gradio app: compare the 1–5 star ratings of two products with a beta-binomial model.

Each product's ratings are modelled as beta-binomial (users differ in how much they like it), and the products are
compared through the profile likelihood of the log odds ratio of a favourable outcome. Method: the post
"ratings ~ brand" (POST_URL).
"""
import gradio as gr
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from scipy import stats

from beta_binomial import CHI2_95, LOGIT_P, compare

pio.templates.default = "ggplot2"

POST_URL = "https://prteek.github.io/regression_room/posts/ratings_inference/"
STAR_LABELS = [f"{s}★" for s in range(1, 6)]
COLOURS = ["#F8766D", "#00BFC4"]  # ggplot2's default two-group hues
# The post's example: two pairs of headphones from the electronics ratings data
DEFAULT_A = ("Apple headphones", [11, 11, 8, 13, 33])
DEFAULT_B = ("Philips headphones", [2, 4, 7, 9, 16])
FEW_RATINGS = 20


def fmt_or(theta):
    return "∞" if theta is None else f"{np.exp(theta):.2f}"


def verdict(c, name_a: str, name_b: str) -> str:
    lo, hi = c.ci
    at_edge = abs(c.theta) >= (LOGIT_P[1] - LOGIT_P[0]) - 0.1
    interval = f"{fmt_or(lo) if lo is not None else '0'} to {fmt_or(hi)}"
    if at_edge or (lo is None and hi is None):
        head = (f"**The ratings can't pin down a difference.** One product's ratings sit entirely at one end of the "
                f"scale, or there are too few of them, so a wide range of odds ratios fits equally well.")
    elif c.excludes_zero:
        better, worse = (name_b, name_a) if c.theta > 0 else (name_a, name_b)
        ratio = np.exp(abs(c.theta))
        head = (f"**{better} is rated more favourably than {worse}.** The odds of a favourable outcome are "
                f"{ratio:.2f} times higher for {better}.")
    else:
        head = (f"**No clear difference between {name_a} and {name_b}.** The 95% interval for the odds ratio "
                f"includes 1 (equal preference).")
    lines = [head]
    if not (at_edge or (lo is None and hi is None)):
        lines += ["", f"Odds ratio, {name_b} vs {name_a}: **{fmt_or(c.theta)}** "
                      f"(95% likelihood interval {interval}; above 1 favours {name_b})."]
    n_a, n_b = int(c.a.counts.sum()), int(c.b.counts.sum())
    if min(n_a, n_b) < FEW_RATINGS:
        lines.append(f"\nWith only {min(n_a, n_b)} ratings for one product, expect a wide interval.")
    return "\n".join(lines)


def summary_rows(c, name_a, name_b):
    rows = []
    for name, f in [(name_a, c.a), (name_b, c.b)]:
        sd = np.sqrt(f.alpha * f.beta / (f.d ** 2 * (f.d + 1)))
        rows.append([name, int(f.counts.sum()), f"{f.mean_stars:.2f}", f"{f.p:.2f}", f"{sd:.2f}"])
    return rows


def profile_figure(c, name_a, name_b) -> go.Figure:
    fig = go.Figure(go.Scatter(x=np.exp(c.profile_theta), y=c.profile_loglik, mode="lines",
                               line=dict(color="black", width=2), name="profile log-likelihood",
                               hovertemplate="odds ratio %{x:.2f}<br>log-lik %{y:.2f}<extra></extra>"))
    # reference lines as traces in data coordinates (vertical shapes on a log axis don't render in gr.Plot)
    y_lo, y_hi = max(-6.0, c.profile_loglik.min()), 0.3
    or_lo, or_hi = np.exp(c.profile_theta.min()), np.exp(c.profile_theta.max())
    threshold = -CHI2_95 / 2
    lines = [([or_lo, or_hi], [threshold] * 2, dict(color="#555555", width=1.5, dash="dot"), "95% threshold")]
    if or_lo < 1 < or_hi:
        lines.append(([1, 1], [y_lo, y_hi], dict(color="#555555", width=1.5), "equal preference"))
    if abs(c.theta) < 15:
        lines.append(([c.odds_ratio] * 2, [y_lo, y_hi], dict(color="#C77CFF", width=2, dash="dash"), "best fit"))
    for end in c.ci:
        if end is not None:
            lines.append(([np.exp(end)] * 2, [y_lo, y_hi], dict(color="#7CAE00", width=2, dash="dot"),
                          "95% interval"))
    for x, y, style, name in lines:
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=style, name=name, hoverinfo="name"))
    fig.add_annotation(x=np.log10(or_hi), y=threshold, text="95% threshold", showarrow=False,
                       xanchor="right", yanchor="top")
    fig.update_xaxes(type="log", title=f"odds ratio, {name_b} vs {name_a} (log scale)")
    fig.update_yaxes(title="profile log-likelihood (0 at the best fit)", range=[y_lo, y_hi])
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    return fig


def fit_figure(c, name_a, name_b) -> go.Figure:
    fig = make_subplots(rows=1, cols=3, subplot_titles=[name_a, name_b, "Spread of user preference"],
                        column_widths=[0.3, 0.3, 0.4], horizontal_spacing=0.08)
    for col, (name, f, colour) in enumerate([(name_a, c.a, COLOURS[0]), (name_b, c.b, COLOURS[1])], start=1):
        fig.add_trace(go.Bar(x=STAR_LABELS, y=f.counts, marker_color=colour, opacity=0.7, name=f"{name}: observed",
                             showlegend=False), row=1, col=col)
        fig.add_trace(go.Scatter(x=STAR_LABELS, y=f.fitted_counts(), mode="markers+lines",
                                 marker=dict(color="black", size=7), line=dict(color="black", width=1),
                                 name="fitted", showlegend=col == 1), row=1, col=col)
        p = np.linspace(0.005, 0.995, 199)
        dens = stats.beta.pdf(p, f.alpha, f.beta)
        fig.add_trace(go.Scatter(x=p, y=dens, mode="lines", line=dict(color=colour, width=2.5), name=name),
                      row=1, col=3)
    fig.update_yaxes(title_text="ratings", row=1, col=1)
    fig.update_xaxes(title_text="preference p (0 = always 1★, 1 = always 5★)", range=[0, 1], row=1, col=3)
    top = max(stats.beta.pdf(0.5, f.alpha, f.beta) for f in (c.a, c.b))
    fig.update_yaxes(title_text="density", range=[0, max(4.0, 2.5 * top)], row=1, col=3)
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=-0.25, x=0))
    return fig


def run(name_a, name_b, *counts):
    name_a, name_b = (name_a or "Product A").strip(), (name_b or "Product B").strip()
    ca = np.nan_to_num(np.array(counts[:5], float))
    cb = np.nan_to_num(np.array(counts[5:], float))
    if (ca < 0).any() or (cb < 0).any():
        return "Counts can't be negative.", None, None, None
    if ca.sum() == 0 or cb.sum() == 0:
        return "Enter at least one rating for each product.", None, None, None
    c = compare(np.round(ca), np.round(cb))
    return (verdict(c, name_a, name_b), summary_rows(c, name_a, name_b),
            profile_figure(c, name_a, name_b), fit_figure(c, name_a, name_b))


def counts_column(label, default):
    name = gr.Textbox(default[0], label=label)
    with gr.Row():
        boxes = [gr.Number(v, label=s, minimum=0, precision=0, min_width=60)
                 for s, v in zip(STAR_LABELS, default[1])]
    return name, boxes


with gr.Blocks(title="Compare star ratings") as demo:
    gr.Markdown(
        "# Is one product really rated better?\n"
        "Enter how many 1★ to 5★ ratings two products have. Averages hide how differently people rate the same "
        "thing, so this fits a **beta-binomial** model to each product (users differ in how much they like it) and "
        "compares them through the **profile likelihood** of the odds ratio of a favourable outcome. "
        f"Method: [ratings ~ brand]({POST_URL})."
    )
    with gr.Row():
        with gr.Column():
            name_a, boxes_a = counts_column("Product A", DEFAULT_A)
        with gr.Column():
            name_b, boxes_b = counts_column("Product B", DEFAULT_B)
    result = gr.Markdown()
    table = gr.Dataframe(headers=["product", "ratings", "mean stars", "preference p", "spread of p (SD)"],
                         interactive=False, show_label=False)
    gr.Markdown("**Profile likelihood of the odds ratio.** Values above the dotted line are inside the 95% interval "
                "(green); the dashed line is the best fit; 1 means equal preference.")
    profile = gr.Plot(show_label=False)
    gr.Markdown("**Fit check.** Bars are the entered ratings, black points the model's fitted counts. Right: each "
                "product's estimated distribution of user preference; a U shape means users either love it or "
                "hate it.")
    fit = gr.Plot(show_label=False)
    gr.Markdown(
        "A rating of s stars is treated as s − 1 favourable outcomes out of 4, a working approximation that gives "
        "interpretable parameters. Default example: Apple and Philips headphones from the electronics ratings in "
        "Wan, Ni, Misra & McAuley (2020), *Addressing Marketing Bias in Product Recommendations*, WSDM."
    )

    inputs = [name_a, name_b, *boxes_a, *boxes_b]
    outputs = [result, table, profile, fit]
    gr.on([c.change for c in inputs], run, inputs, outputs, trigger_mode="always_last")
    demo.load(run, inputs, outputs)

if __name__ == "__main__":
    demo.launch()
