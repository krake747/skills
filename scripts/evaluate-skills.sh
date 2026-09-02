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

set +e
uvx --from 'skillevaluator[all] @ git+https://github.com/NVIDIA/SkillEvaluator.git' \
  skillevaluator validate "$skills_root" \
  --checks schema,pii,license,quality,unicode,lint \
  --no-dedup \
  --output-dir "$output_dir"
status=$?
set -e

# Allow missing author when not strict. Filter the JSON report and downgrade that single high error.
if [[ "$status" -ne 0 && "$strict_author" != "1" ]]; then
  # Find the latest JSON report written for this run
  latest_json=$(ls -t "$output_dir"/*.json 2>/dev/null | head -n 1)
  if [[ -z "$latest_json" ]]; then
    latest_json=$(find "$output_dir" -maxdepth 3 -name "*.json" -type f -printf "%T@ %p\n" 2>/dev/null | sort -nr | head -n 1 | cut -d' ' -f2-)
  fi
  if [[ -n "${latest_json:-}" && -f "$latest_json" ]]; then
    only_author=$(python3 - "$latest_json" <<'PY'
import json, sys
path = sys.argv[1]
try:
    data = json.loads(open(path).read())
except Exception:
    print("0")
    sys.exit(0)
findings = []
for r in data.get("results", []):
    for f in r.get("findings", []):
        findings.append(f)
high = [f for f in findings if f.get("severity") == "high"]
# count high findings that are not author_missing
non_author_high = [f for f in high if f.get("check_name") != "author_missing"]
if len(high) > 0 and len(non_author_high) == 0:
    print("1")
else:
    print("0")
PY
)
    if [[ "$only_author" == "1" ]]; then
      echo "" >&2
      echo "Reports: $output_dir" >&2
      echo "Note: author_missing treated as warning SKILL_EVAL_STRICT_AUTHOR=0, exit 0" >&2
      exit 0
    fi
  fi
fi

if [[ "$skills_root" == "$repo_root" ]] || [[ "$skills_root" == "$repo_root"/* && -n "$skill_filter" ]]; then
  echo "" >&2
  echo "Reports: $output_dir" >&2
  if [[ "$status" -ne 0 && "$strict_author" != "1" ]]; then
    echo "Note: strict author is off. Rerun with SKILL_EVAL_STRICT_AUTHOR=1 to enforce metadata.author." >&2
  fi
fi

exit "$status"
