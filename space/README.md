---
title: Compare Star Ratings
emoji: ⭐
colorFrom: yellow
colorTo: gray
sdk: gradio
sdk_version: 6.30.0
python_version: "3.12"
app_file: app.py
pinned: false
license: cc-by-4.0
short_description: Is one product really rated better? Beta-binomial comparison
datasets:
  - prteek/ratings-compare
---

Interactive companion to the blog post [Is One Product Really Rated Better?](https://huggingface.co/blog/prteek/ratings-brand-analysis) on Hugging Face. Enter how many 1★ to 5★ ratings two products have, or the total and the percentage at each star as Amazon shows them. Each product is fitted with a beta-binomial model (users differ in how much they like it), and the two are compared through the profile likelihood of the odds ratio of a favourable outcome, with a 95% likelihood interval.

Code: [github.com/prteek/ratings-brand-analysis](https://github.com/prteek/ratings-brand-analysis) · Data: [prteek/ratings-compare](https://huggingface.co/datasets/prteek/ratings-compare). Default example: Apple and Philips headphones from the electronics ratings in Wan, Ni, Misra & McAuley (2020), *Addressing Marketing Bias in Product Recommendations*, WSDM.
