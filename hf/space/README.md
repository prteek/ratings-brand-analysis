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
---

Interactive companion to the paper [Ratings ~ Brand, Analysis](https://www.alphaxiv.org/abs/2610.ratings-brand-analysis) on alphaXiv. Enter how many 1★ to 5★ ratings two products have. Each product is fitted with a beta-binomial model (users differ in how much they like it), and the two are compared through the profile likelihood of the odds ratio of a favourable outcome, with a 95% likelihood interval.

Code: [github.com/prteek/ratings-compare](https://github.com/prteek/ratings-compare). Default example: Apple and Philips headphones from the electronics ratings in Wan, Ni, Misra & McAuley (2020), *Addressing Marketing Bias in Product Recommendations*, WSDM.
