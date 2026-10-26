#!/usr/bin/env bash
# Publish the app as the HF Space prteek/ratings-compare (needs `hf auth login` as prteek).
set -euo pipefail
cd "$(dirname "$0")/.."
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

cp app.py beta_binomial.py hf/space/README.md hf/space/requirements.txt "$stage/"
uv run hf upload prteek/ratings-compare "$stage" . --repo-type space --commit-message "${1:-Update app}"
