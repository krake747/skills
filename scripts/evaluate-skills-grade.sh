#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
skill_name=${1:-}
output_root=${2:-"${SKILL_EVAL_OUTPUT_DIR:-${TMPDIR:-/tmp}/skills-live-evals}"}
skill_dir="$repo_root/$skill_name"
evals_file="$skill_dir/evals/evals.json"

if [ -z "$skill_name" ]; then
  printf 'Usage: %s SKILL [OUTPUT_DIR]\n' "${0##*/}" >&2
  exit 2
fi

if [ ! -f "$evals_file" ]; then
  printf 'Evals file is missing: %s\n' "$evals_file" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  printf '%s\n' 'jq is required.' >&2
  exit 1
fi

grade_assertion() {
  local assertion=$1
  local response=$2
  local source_text=$3
  local passed status evidence token line_limit

  passed=false
  status=manual
  evidence='Requires human review.'

  case "$assertion" in
    *"contains no em dash or en dash"*)
      status=automatic
      if [[ "$response" != *'—'* && "$response" != *'–'* ]]; then
        passed=true
        evidence='No em dash or en dash found.'
      else
        evidence='Found an em dash or en dash in the response.'
      fi
      ;;
    *"under 20 lines"*)
      status=automatic
      line_limit=20
      if [ "$(printf '%s\n' "$response" | wc -l)" -lt "$line_limit" ]; then
        passed=true
        evidence="Response has fewer than $line_limit lines."
      else
        evidence="Response has $(( $(printf '%s\n' "$response" | wc -l) - 1 )) lines."
      fi
      ;;
    *"under 15 lines"*)
      status=automatic
      line_limit=15
      if [ "$(printf '%s\n' "$response" | wc -l)" -lt "$line_limit" ]; then
        passed=true
        evidence="Response has fewer than $line_limit lines."
      else
        evidence="Response has $(( $(printf '%s\n' "$response" | wc -l) - 1 )) lines."
      fi
      ;;
    *"removes the phrases 'seamlessly' and 'going forward'"*)
      status=automatic
      if [[ "$response" != *seamlessly* && "$response" != *"going forward"* ]]; then
        passed=true
        evidence='Neither listed phrase appears in the response.'
      else
        evidence='At least one listed phrase remains in the response.'
      fi
      ;;
    *"does not invent"*|*"without inventing"*|*"not invent"*)
      status=manual
      evidence='Requires comparison with the supplied facts.'
      ;;
    *"does not add claims"*|*"does not introduce"*|*"without adding"*)
      status=manual
      evidence='Requires comparison with the source or fixture.'
      ;;
    *"response exists"*|*"is a rewritten"*|*"is a plan"*|*"includes a rewritten"*)
      status=automatic
      if [ -n "${response//[[:space:]]/}" ]; then
        passed=true
        evidence='A non-empty response was produced.'
      else
        evidence='Response is empty.'
      fi
      ;;
    *"command '"*|*"path '"*|*"URL '"*|*"date '"*|*"version '"*|*"phrase '"*|*"scope '"*|*"ticker '"*|*"side '"*|*"quantity '"*|*"price '"*)
      if [[ "$assertion" =~ \'([^\']+)\' ]]; then
        token=${BASH_REMATCH[1]}
        status=automatic
        if [[ "$response" == *"$token"* ]]; then
          passed=true
          evidence="Found '$token' in the response."
        else
          evidence="Did not find '$token' in the response."
        fi
      fi
      ;;
    *)
      status=manual
      evidence='Requires human review of the response against the assertion.'
      ;;
  esac

  jq -n \
    --arg text "$assertion" \
    --arg status "$status" \
    --arg evidence "$evidence" \
    --argjson passed "$passed" \
    '{text: $text, passed: (if $status == "manual" then null else $passed end), status: $status, evidence: $evidence}'
}

grade_mode() {
  local test_id=$1
  local mode=$2
  local run_dir="$output_root/$skill_name/$test_id/$mode"
  local response_file="$run_dir/response.txt"
  local timing_file="$run_dir/timing.json"
  local response source_text assertion
  local result_file="$run_dir/assertion-results.jsonl"

  : > "$result_file"
  response=''
  source_text=''
  if [ -f "$response_file" ]; then
    response=$(<"$response_file")
  fi
  if [ -f "$timing_file" ] && [ "$(jq -r '.exit_code // 1' "$timing_file")" -ne 0 ]; then
    jq -n '{text: "model run succeeded", passed: false, status: "automatic", evidence: "The model runner returned a non-zero exit code."}' >> "$result_file"
  else
    jq -n '{text: "model run succeeded", passed: true, status: "automatic", evidence: "The model runner returned exit code 0."}' >> "$result_file"
  fi

  while IFS= read -r assertion; do
    grade_assertion "$assertion" "$response" "$source_text" >> "$result_file"
  done < <(jq -r --arg case_id "$test_id" '.evals[] | select(.id == $case_id) | (.assertions // [])[]' "$evals_file")

  jq -s \
    --arg skill "$skill_name" \
    --arg case_id "$test_id" \
    --arg mode "$mode" \
    '{skill: $skill, case: $case_id, mode: $mode, assertion_results: ., summary: {automatic_passed: (map(select(.status == "automatic" and .passed == true)) | length), automatic_failed: (map(select(.status == "automatic" and .passed == false)) | length), manual_review: (map(select(.status == "manual")) | length), total: length}}' \
    "$result_file" > "$run_dir/grading.json"
  rm -f "$result_file"
  printf '  graded %s/%s\n' "$test_id" "$mode"
}

mapfile -t selected_cases < <(jq -r '.evals[].id' "$evals_file")
for test_id in "${selected_cases[@]}"; do
  grade_mode "$test_id" with_skill
  grade_mode "$test_id" without_skill
done

jq -s \
  --arg skill "$skill_name" \
  '{skill: $skill, configurations: group_by(.mode) | map({mode: .[0].mode, cases: length, automatic_passed: (map(.summary.automatic_passed) | add), automatic_failed: (map(.summary.automatic_failed) | add), manual_review: (map(.summary.manual_review) | add)}), delta: {automatic_passed: ((map(select(.mode == "with_skill") | .summary.automatic_passed) | add) - (map(select(.mode == "without_skill") | .summary.automatic_passed) | add)), automatic_failed: ((map(select(.mode == "with_skill") | .summary.automatic_failed) | add) - (map(select(.mode == "without_skill") | .summary.automatic_failed) | add))}}' \
  <(for test_id in "${selected_cases[@]}"; do cat "$output_root/$skill_name/$test_id/with_skill/grading.json"; cat "$output_root/$skill_name/$test_id/without_skill/grading.json"; done) \
  > "$output_root/$skill_name/benchmark.json"

printf '\nBenchmark written to %s/%s/benchmark.json\n' "$output_root" "$skill_name"
