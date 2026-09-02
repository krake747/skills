#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: evaluate-skills.sh [options] [skills_root]

Options:
  --skill <name>   Validate a single skill directory (e.g. draft-pr)
  --clean          Remove previous reports before running
  --strict-author  Require metadata.author, fail on author_missing (default in CI)
  --help           Show this help

Env:
  SKILL_EVAL_OUTPUT_DIR  Output directory (default /tmp/skills-skillevaluator-reports)
  SKILL_EVAL_STRICT_AUTHOR 0 to warn on author_missing instead of failing

Positional skills_root defaults to repo root.
USAGE
}

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
skills_root="$repo_root"
skill_filter=""
clean=0
strict_author="${SKILL_EVAL_STRICT_AUTHOR:-0}"
output_dir="${SKILL_EVAL_OUTPUT_DIR:-"${TMPDIR:-/tmp}/skills-skillevaluator-reports"}"

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
    --strict-author)
      strict_author=1
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

if [[ -n "$skill_filter" ]]; then
  skills_root=$(realpath -m "$skills_root")
  if [[ "$skills_root" == "$repo_root" ]] || [[ "$skills_root" == "$repo_root/"* ]]; then
    skills_root="$repo_root/$skill_filter"
  fi
  if [[ ! -f "$skills_root/SKILL.md" ]]; then
    printf 'Skill not found: %s (expected %s/SKILL.md)\n' "$skill_filter" "$skills_root" >&2
    exit 1
  fi
fi

if [[ "$clean" -eq 1 ]]; then
  rm -rf "$output_dir"
fi

if ! command -v uvx >/dev/null 2>&1 && [[ -x "$HOME/.local/bin/uvx" ]]; then
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v uvx >/dev/null 2>&1; then
  printf '%s\n' "uvx is required. Install uv from https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

if [[ "$strict_author" != "1" ]]; then
  fallback_author="$(git -C "$repo_root" config user.name 2>/dev/null || echo "")"
  fallback_email="$(git -C "$repo_root" config user.email 2>/dev/null || echo "")"
  if [[ -n "$fallback_author" && -n "$fallback_email" ]]; then
    printf 'Author fallback: %s <%s> (SKILL_EVAL_STRICT_AUTHOR=0)\n' "$fallback_author" "$fallback_email" >&2
  else
    printf 'Author fallback requested but git user.name or user.email is not set (SKILL_EVAL_STRICT_AUTHOR=0)\n' >&2
  fi
fi

# shellcheck disable=SC2145
printf 'Validating: %s\n' "$skills_root" >&2
printf 'Output dir: %s\n' "$output_dir" >&2
if [[ -n "$skill_filter" ]]; then printf 'Skill filter: %s\n' "$skill_filter" >&2; fi

if [[ "$strict_author" != "1" ]]; then
  # Lenient mode: capture evaluator output, downgrade author_missing to warning
  tmp_out=$(mktemp)
  set +e
  uvx --from 'skillevaluator[all] @ git+https://github.com/NVIDIA/SkillEvaluator.git' \
    skillevaluator validate "$skills_root" \
    --checks schema,pii,license,quality,unicode,lint \
    --no-dedup \
    --output-dir "$output_dir" >"$tmp_out" 2>&1
  status=$?
  set -e
  if [[ "$status" -ne 0 ]]; then
    only_author=$(python3 - "$output_dir" <<'PY'
import json, pathlib, sys
out_dir = pathlib.Path(sys.argv[1])
# Check all JSON reports written in this run
json_files = list(out_dir.rglob("*.json"))
# Filter to evaluator outputs (contain results/findings)
author_only = True
found_any = False
for jf in json_files:
    try:
        data = json.loads(jf.read_text())
    except Exception:
        continue
    if "results" not in data:
        continue
    found_any = True
    for r in data.get("results", []):
        for f in r.get("findings", []):
            if f.get("severity") == "high" and f.get("check_name") != "author_missing":
                author_only = False
                break
        # also check schema high at top level? already covered
    high = []
    for r in data.get("results", []):
        high.extend([f for f in r.get("findings", []) if f.get("severity") == "high"])
    if high:
        non_author = [f for f in high if f.get("check_name") != "author_missing"]
        if non_author:
            author_only = False
if found_any and author_only:
    # verify at least one high was author_missing, otherwise this is a clean pass with no highs
    has_author_high = False
    for jf in json_files:
        try:
            data = json.loads(jf.read_text())
        except Exception:
            continue
        for r in data.get("results", []):
            for f in r.get("findings", []):
                if f.get("severity") == "high" and f.get("check_name") == "author_missing":
                    has_author_high = True
    if has_author_high:
        print("1")
    else:
        print("0")
else:
    print("0")
PY
)
    if [[ "$only_author" == "1" ]]; then
      echo "Result: PASS (author_missing downgraded to warning, SKILL_EVAL_STRICT_AUTHOR=0)" >&2
      echo "All skills pass when author is optional. Rerun with SKILL_EVAL_STRICT_AUTHOR=1 to enforce." >&2
      echo "Reports: $output_dir" >&2
      rm -f "$tmp_out"
      exit 0
    else
      cat "$tmp_out" >&2
      rm -f "$tmp_out"
    fi
  else
    cat "$tmp_out" >&2
    rm -f "$tmp_out"
  fi
else
  set +e
  uvx --from 'skillevaluator[all] @ git+https://github.com/NVIDIA/SkillEvaluator.git' \
    skillevaluator validate "$skills_root" \
    --checks schema,pii,license,quality,unicode,lint \
    --no-dedup \
    --output-dir "$output_dir"
  status=$?
  set -e
fi

if [[ "$skills_root" == "$repo_root" ]] || [[ "$skills_root" == "$repo_root"/* && -n "$skill_filter" ]]; then
  echo "" >&2
  echo "Reports: $output_dir" >&2
  if [[ "$status" -ne 0 && "$strict_author" != "1" ]]; then
    echo "Note: strict author is off. Rerun with SKILL_EVAL_STRICT_AUTHOR=1 to enforce metadata.author." >&2
  fi
fi

exit "$status"
