#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: evaluate-skills-tier2.sh [options] [skills_root]

Options:
  --skill <name>   Check a single skill directory
  --clean          Remove previous tier2 reports before running
  --help           Show this help

Env:
  SKILL_EVAL_OUTPUT_DIR  Output directory (default /tmp/skills-skillevaluator-tier2)
  OLLAMA_URL             Ollama base URL (default http://127.0.0.1:11434/v1)
USAGE
}

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
skills_root="$repo_root"
output_dir=${SKILL_EVAL_OUTPUT_DIR:-"${TMPDIR:-/tmp}/skills-skillevaluator-tier2"}
ollama_url=${OLLAMA_URL:-"http://127.0.0.1:11434/v1"}
skill_filter=""
clean=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill)
      skill_filter="${2:-}"
      [[ -n "$skill_filter" ]] || { echo "--skill requires a name" >&2; exit 1; }
      shift 2
      ;;
    --clean)
      clean=1
      shift
      ;;
    --help | -h)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      skills_root="$1"
      shift
      ;;
  esac
done

if [[ "$clean" -eq 1 ]]; then
  rm -rf "$output_dir"
fi

if [[ -n "$skill_filter" ]]; then
  skills_root=$(realpath -m "$skills_root")
  if [[ "$skills_root" == "$repo_root" ]]; then
    skills_root="$repo_root/$skill_filter"
  fi
  if [[ ! -f "$skills_root/SKILL.md" ]]; then
    # Search from repo root if skills_root was a custom path
    if [[ -f "$repo_root/$skill_filter/SKILL.md" ]]; then
      skills_root="$repo_root/$skill_filter"
    else
      printf 'Skill not found: %s\n' "$skill_filter" >&2
      exit 1
    fi
  fi
fi

if ! curl -fsS "${ollama_url%/v1}/api/version" >/dev/null 2>&1; then
  printf '%s\n' "Ollama is not running. Start it with: ollama serve" >&2
  exit 1
fi

if ! command -v uvx >/dev/null 2>&1 && [[ -x "$HOME/.local/bin/uvx" ]]; then
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

if [[ -z "$skill_filter" ]]; then
  printf 'Tier 2: similarity-check %s\n' "$skills_root" >&2
  "${evaluator[@]}" similarity-check "$skills_root" \
    --full-body \
    --report cli \
    --output-dir "$output_dir/similarity" || status=$?
else
  printf 'Tier 2: skipping similarity-check for single skill filter %s\n' "$skill_filter" >&2
fi

check_one() {
  local skill_dir="$1"
  local skill_name
  skill_name=$(basename "$skill_dir")
  printf 'Tier 2: context-optimization-check %s\n' "$skill_name" >&2
  "${evaluator[@]}" context-optimization-check "$skill_dir" \
    --report cli \
    --output-dir "$output_dir/$skill_name" || return $?
}

if [[ -n "$skill_filter" ]]; then
  check_one "$skills_root" || status=$?
else
  for skill_file in "$skills_root"/*/SKILL.md; do
    [[ -f "$skill_file" ]] || continue
    skill_dir=$(dirname "$skill_file")
    check_one "$skill_dir" || status=$?
  done
fi

printf '\nReports: %s\n' "$output_dir" >&2
exit "$status"
