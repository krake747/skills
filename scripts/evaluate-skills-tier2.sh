#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
skills_root=${1:-"$repo_root"}
output_dir=${SKILL_EVAL_OUTPUT_DIR:-"${TMPDIR:-/tmp}/skills-skillevaluator-tier2"}
ollama_url=${OLLAMA_URL:-"http://127.0.0.1:11434/v1"}

if ! curl -fsS "${ollama_url%/v1}/api/version" >/dev/null 2>&1; then
  printf '%s\n' "Ollama is not running. Start it with: ollama serve" >&2
  exit 1
fi

if ! command -v uvx >/dev/null 2>&1 && [ -x "$HOME/.local/bin/uvx" ]; then
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v uvx >/dev/null 2>&1; then
  printf '%s\n' "uvx is required. Install uv from https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

export SKILL_EVAL_LLM_PROVIDER=${SKILL_EVAL_LLM_PROVIDER:-openai-compatible}
export SKILL_EVAL_LLM_BASE_URL=${SKILL_EVAL_LLM_BASE_URL:-"$ollama_url"}
export SKILL_EVAL_LLM_MODEL=${SKILL_EVAL_LLM_MODEL:-qwen2.5-coder:3b}
export SKILL_EVAL_LLM_API_KEY=${SKILL_EVAL_LLM_API_KEY:-local-no-key}
export SKILL_EVAL_EMBEDDING_PROVIDER=${SKILL_EVAL_EMBEDDING_PROVIDER:-openai-compatible}
export SKILL_EVAL_EMBEDDING_BASE_URL=${SKILL_EVAL_EMBEDDING_BASE_URL:-"$ollama_url"}
export SKILL_EVAL_EMBEDDING_MODEL=${SKILL_EVAL_EMBEDDING_MODEL:-nomic-embed-text}
export SKILL_EVAL_EMBEDDING_API_KEY=${SKILL_EVAL_EMBEDDING_API_KEY:-local-no-key}

for model in "$SKILL_EVAL_LLM_MODEL" "$SKILL_EVAL_EMBEDDING_MODEL"; do
  if ! ollama show "$model" >/dev/null 2>&1; then
    printf 'Ollama model is missing: %s\n' "$model" >&2
    printf 'Install it with: ollama pull %s\n' "$model" >&2
    exit 1
  fi
done

evaluator=(uvx --from 'skillevaluator[all] @ git+https://github.com/NVIDIA/SkillEvaluator.git' skillevaluator)
status=0

"${evaluator[@]}" similarity-check "$skills_root" \
  --full-body \
  --report cli \
  --output-dir "$output_dir/similarity" || status=$?

for skill_file in "$skills_root"/*/SKILL.md; do
  [ -f "$skill_file" ] || continue
  skill_dir=$(dirname "$skill_file")
  skill_name=$(basename "$skill_dir")
  "${evaluator[@]}" context-optimization-check "$skill_dir" \
    --report cli \
    --output-dir "$output_dir/$skill_name" || status=$?
done

exit "$status"
