#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
skills_root=${1:-"$repo_root"}
output_dir=${SKILL_EVAL_OUTPUT_DIR:-"${TMPDIR:-/tmp}/skills-skillevaluator-reports"}

if ! command -v uvx >/dev/null 2>&1 && [ -x "$HOME/.local/bin/uvx" ]; then
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v uvx >/dev/null 2>&1; then
  printf '%s\n' "uvx is required. Install uv from https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

exec uvx --from 'skillevaluator[all] @ git+https://github.com/NVIDIA/SkillEvaluator.git' \
  skillevaluator validate "$skills_root" \
  --checks schema,pii,license,quality,unicode,lint \
  --no-dedup \
  --output-dir "$output_dir"
