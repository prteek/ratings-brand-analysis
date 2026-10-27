---
license: apache-2.0
language:
  - en
pretty_name: Headphone star ratings (Philips, Jabra, Apple)
tags:
  - ratings
  - recommender-systems
  - tabular
size_categories:
  - 1K<n<10K
configs:
  - config_name: default
    data_files: ratings.csv
---

# Headphone star ratings

7,681 star ratings of 46 headphones from three brands (Philips, Jabra and Apple) by 7,605 users, 2005–2018. This is
the data behind the blog post [Is One Product Really Rated Better?](https://huggingface.co/blog/prteek/ratings-brand-analysis) on
Hugging Face, which compares how users rate two products with a beta-binomial model and profile likelihood, and the
default example in the [ratings-compare Space](https://huggingface.co/spaces/prteek/ratings-compare).
Code: [github.com/prteek/ratings-brand-analysis](https://github.com/prteek/ratings-brand-analysis).

## Source

A subset of the **Electronics** dataset released with Wan, Ni, Misra & McAuley (2020), *Addressing Marketing Bias in
Product Recommendations*, WSDM ([github.com/MengtingWan/marketBias](https://github.com/MengtingWan/marketBias),
Apache-2.0). Kept: every rating in the `Headphones` category from the brands Philips, Jabra and Apple; all columns as
released. This subset is shared under the same licence.

## Columns

| column | content |
|---|---|
| `item_id` | product id (46 products: Philips 30, Jabra 14, Apple 2) |
| `user_id` | anonymised user id, as in the source |
| `rating` | stars, 1–5 |
| `timestamp` | date of the rating |
| `model_attr` | product attribute from the source: `Male`, `Female` or `Female&Male` |
| `category` | `Headphones` for every row |
| `brand` | `Philips`, `Jabra` or `Apple` |
| `year` | year from the source data |
| `user_attr` | user attribute from the source: `Male` or `Female`, missing for most rows |
| `split` | the source's train / validation / test split (0, 1, 2) |

See the source paper for how `model_attr`, `user_attr` and `split` were derived.

The blog post compares Apple item 4501 (76 ratings) with Philips item 3700 (38 ratings). There, a rating of s
stars is modelled as s − 1 favourable outcomes out of 4.

## Citation

```bibtex
@inproceedings{wan2020marketing,
  author    = {Mengting Wan and Jianmo Ni and Rishabh Misra and Julian McAuley},
  title     = {Addressing Marketing Bias in Product Recommendations},
  booktitle = {Proceedings of the 13th International Conference on Web Search and Data Mining (WSDM)},
  year      = {2020}
}
```
