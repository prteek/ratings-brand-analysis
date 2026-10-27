#!/usr/bin/env bash
# Publish to Hugging Face (locally: `hf auth login` as prteek; in CI: HF_TOKEN):
#   space    prteek/ratings-compare: space/ plus the ratings_compare package the app imports
#   dataset  prteek/ratings-compare: data/ratings.csv with dataset/README.md as the card
# Usage: ./publish.sh [message] [space|dataset ...]   (default: both)
# Set HF_CLI=hf to use an installed hf CLI instead of the project environment (as CI does).
set -euo pipefail
cd "$(dirname "$0")"
msg="${1:-Update}"
shift || true
if [ $# -gt 0 ]; then targets=("$@"); else targets=(space dataset); fi
read -r -a hf <<< "${HF_CLI:-uv run hf}"
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

for t in "${targets[@]}"; do
  mkdir "$stage/$t"
  case "$t" in
    space)
      cp space/app.py space/README.md space/requirements.txt "$stage/space/"
      mkdir "$stage/space/ratings_compare"
      cp ratings_compare/__init__.py ratings_compare/beta_binomial.py "$stage/space/ratings_compare/"
      "${hf[@]}" upload prteek/ratings-compare "$stage/space" . --repo-type space --commit-message "$msg" ;;
    dataset)
      cp data/ratings.csv "$stage/dataset/"
      cp dataset/README.md "$stage/dataset/README.md"
      "${hf[@]}" upload prteek/ratings-compare "$stage/dataset" . --repo-type dataset --commit-message "$msg" ;;
    *)
      echo "unknown target: $t" >&2; exit 1 ;;
  esac
done
