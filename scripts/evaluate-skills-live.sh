#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
skill_name=${1:-}
case_id=${2:-}
if [ "$skill_name" = "--" ]; then
  skill_name=${2:-}
  case_id=${3:-}
fi
output_root=${SKILL_EVAL_OUTPUT_DIR:-"${TMPDIR:-/tmp}/skills-live-evals"}

usage() {
  printf 'Usage: %s SKILL [CASE_ID]\n' "${0##*/}" >&2
  printf 'Environment: SKILL_EVAL_LLM_PROVIDER, SKILL_EVAL_LLM_MODEL, SKILL_EVAL_MODEL, SKILL_EVAL_OUTPUT_DIR\n' >&2
}

if [ -z "$skill_name" ]; then
  usage
  exit 2
fi

skill_dir="$repo_root/$skill_name"
evals_file="$skill_dir/evals/evals.json"
if [ ! -f "$skill_dir/SKILL.md" ] || [ ! -f "$evals_file" ]; then
  printf 'Skill or evals file is missing: %s\n' "$skill_name" >&2
  exit 1
fi

if [ -f "$repo_root/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$repo_root/.env"
  set +a
fi

provider=${SKILL_EVAL_LLM_PROVIDER:-openai}
model=${SKILL_EVAL_LLM_MODEL:-gpt-5.6-luna}
model_ref=${SKILL_EVAL_MODEL:-"$provider/$model"}

if [ "$provider" = "openai" ] && [ -z "${OPENAI_API_KEY:-}" ]; then
  printf '%s\n' 'OPENAI_API_KEY is missing. Add it to .env or the environment.' >&2
  exit 1
fi

if ! command -v opencode >/dev/null 2>&1; then
  printf '%s\n' 'opencode is required.' >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  printf '%s\n' 'jq is required.' >&2
  exit 1
fi

case_count=$(jq --arg case_id "$case_id" '[.evals[] | select(($case_id == "") or (.id == $case_id))] | length' "$evals_file")
if [ "$case_count" -eq 0 ]; then
  printf 'No eval case found%s\n' "${case_id:+: $case_id}" >&2
  exit 1
fi

run_case() {
  local test_id=$1
  local prompt=$2
  local mode=$3
  local run_dir="$output_root/$skill_name/$test_id/$mode"
  local workspace="$run_dir/workspace"
  local started finished duration raw response tokens exit_code

  mkdir -p "$workspace" "$run_dir/outputs"
  if [ "$mode" = "with_skill" ]; then
    mkdir -p "$workspace/.agents/skills/$skill_name"
    cp "$skill_dir/SKILL.md" "$workspace/.agents/skills/$skill_name/SKILL.md"
  fi

  while IFS= read -r fixture; do
    [ -n "$fixture" ] || continue
    mkdir -p "$workspace/$(dirname "$fixture")"
    cp "$skill_dir/$fixture" "$workspace/$fixture"
  done < <(jq -r --arg case_id "$test_id" '.evals[] | select(.id == $case_id) | (.files // [])[]' "$evals_file")

  started=$(date +%s%3N)
  if [ "${SKILL_EVAL_DRY_RUN:-0}" = "1" ]; then
    printf '%s\n' "dry run: $mode $test_id ($model_ref)" | tee "$run_dir/response.txt"
    : > "$run_dir/trajectory.jsonl"
    tokens=0
    exit_code=0
  else
    set +e
    raw=$(opencode run \
      --dir "$workspace" \
      --model "$model_ref" \
      --format json \
      --pure \
      "Read the supplied task and attached fixture files. Return the requested result in your response. Do not modify files. $prompt" \
      2>"$run_dir/stderr.log")
    exit_code=$?
    set -e
    printf '%s\n' "$raw" > "$run_dir/trajectory.jsonl"
    response=$(printf '%s\n' "$raw" | jq -r 'select(.type == "text") | .part.text' 2>/dev/null | paste -sd '\n' - || true)
    tokens=$(jq -s '[.[] | .part.tokens.total // 0] | add' "$run_dir/trajectory.jsonl" 2>/dev/null || printf '0')
    printf '%s\n' "${response:-No text response was produced. See trajectory.jsonl and stderr.log.}" > "$run_dir/response.txt"
  fi
  finished=$(date +%s%3N)
  duration=$((finished - started))
  jq -n \
    --arg skill "$skill_name" \
    --arg case_id "$test_id" \
    --arg mode "$mode" \
    --arg model "$model_ref" \
    --argjson duration_ms "$duration" \
    --argjson total_tokens "$tokens" \
    --argjson exit_code "$exit_code" \
    '{skill: $skill, case: $case_id, mode: $mode, model: $model, duration_ms: $duration_ms, total_tokens: $total_tokens, exit_code: $exit_code}' \
    > "$run_dir/timing.json"
  printf '  %s/%s: %s\n' "$test_id" "$mode" "$run_dir"
  return "$exit_code"
}

status=0
mapfile -t selected_cases < <(jq -r --arg case_id "$case_id" '.evals[] | select(($case_id == "") or (.id == $case_id)) | .id' "$evals_file")
for test_id in "${selected_cases[@]}"; do
  prompt=$(jq -r --arg case_id "$test_id" '.evals[] | select(.id == $case_id) | .prompt' "$evals_file")
  run_case "$test_id" "$prompt" with_skill || status=$?
  run_case "$test_id" "$prompt" without_skill || status=$?
done

printf '\nResults written to %s/%s\n' "$output_root" "$skill_name"
exit "$status"
