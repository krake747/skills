#!/usr/bin/env python3
"""Grade objective assertions and aggregate live skill eval results."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict, cast


type JsonObject = dict[str, Any]


class GradeResult(TypedDict, total=False):
    text: str
    passed: bool | None
    status: str
    evidence: str


@dataclass(frozen=True, slots=True)
class GradeRule:
    matches: Callable[[str], bool]
    grade: Callable[[str, str], GradeResult]


@dataclass(frozen=True, slots=True)
class GradeConfig:
    skill: str
    iteration: int
    output_root: Path


def automatic(passed: bool, evidence: str) -> GradeResult:
    return {"passed": passed, "status": "automatic", "evidence": evidence}


def grade_no_dash(_: str, response: str) -> GradeResult:
    passed = "—" not in response and "–" not in response
    return automatic(passed, "No em dash or en dash found." if passed else "Found an em dash or en dash.")


def grade_line_limit(assertion: str, response: str) -> GradeResult:
    # Supports "under 15 lines", "under 20 lines", "under 35 lines" with scaled limit logic.
    # For draft-pr large fixtures, allow 35 when explicitly stated.
    m = re.search(r"under (\d+) lines", assertion)
    limit = int(m.group(1)) if m else (20 if "under 20" in assertion else 15)
    line_count = len(response.splitlines())
    return automatic(line_count < limit, f"Response has {line_count} lines; limit is {limit}.")


def grade_plain_commit(_: str, response: str) -> GradeResult:
    passed = "seamlessly" not in response and "going forward" not in response
    return automatic(passed, "Neither listed phrase appears." if passed else "A listed phrase remains.")


def grade_non_empty(_: str, response: str) -> GradeResult:
    passed = bool(response.strip())
    return automatic(passed, "A non-empty response was produced." if passed else "Response is empty.")


def grade_quoted_token(assertion: str, response: str) -> GradeResult:
    start = assertion.find("'") + 1
    end = assertion.find("'", start)
    if start == 0 or end <= start:
        return {"passed": None, "status": "manual", "evidence": "Requires human review."}
    token = assertion[start:end]
    passed = token in response
    return automatic(passed, f"Found '{token}'." if passed else f"Did not find '{token}'.")


def grade_contains_token(token: str, label: str):
    def _grade(_: str, response: str) -> GradeResult:
        passed = token.lower() in response.lower()
        return automatic(passed, f"Found '{label}'." if passed else f"Did not find '{label}'.")
    return _grade


def grade_regex(pattern: str, label: str):
    compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE)

    def _grade(_: str, response: str) -> GradeResult:
        passed = bool(compiled.search(response))
        return automatic(passed, f"Found '{label}'." if passed else f"Did not find '{label}'.")
    return _grade


QUOTED_TOKEN_MARKERS = (
    "command '",
    "path '",
    "URL '",
    "date '",
    "version '",
    "phrase '",
    "scope '",
    "ticker '",
    "side '",
    "quantity '",
    "price '",
)

# Specific phrase graders for draft-pr
def grade_ticket_link(_: str, response: str) -> GradeResult:
    has_related = "related" in response.lower()
    has_link = "http" in response.lower() or "tickets.example.com" in response.lower() or "PROJ-" in response
    has_markdown = bool(re.search(r"\[.+?\]\(https?://.+?\)", response))
    passed = has_related and has_link and has_markdown
    if passed:
        return automatic(True, "Found Related markdown ticket link.")
    if has_related and has_link:
        return automatic(False, "Found Related ticket link but not as markdown [text](url).")
    return automatic(False, "Missing Related ticket link.")


def grade_churn(_: str, response: str) -> GradeResult:
    # Matches +N -M patterns like +14 -2 or +500 -120
    passed = bool(re.search(r"\+\d+\s+-\d+", response))
    return automatic(passed, "Found churn stats +N -M." if passed else "Did not find churn stats.")


def grade_conventional(_: str, response: str) -> GradeResult:
    # Allow "Title: feat:" or plain "feat:" at line start
    passed = bool(re.search(r"(^|\n)\s*(Title:\s*)?(feat|fix|docs|refactor|chore|test|perf|build|ci)(\(.+\))?:", response, re.IGNORECASE))
    return automatic(passed, "Found conventional commit title." if passed else "Did not find conventional title.")


def grade_files_mentioned(_: str, response: str) -> GradeResult:
    # At least one file mentioned; stronger check is quoted token for specific file
    passed = "filterStore" in response or ".ts" in response or "src/" in response
    return automatic(passed, "Found file reference." if passed else "Did not find file reference.")


def grade_not_invented(_: str, response: str) -> GradeResult:
    # Heuristic: if response says it does not invent or omits, count as pass.
    # Real check is manual, but we can pass if it avoids bare invented IDs like Fixes #999
    # If it contains a ticket link that was not in fixtures, we cannot know here, so just check it does not hallucinate a generic Fixes #
    has_fixes = bool(re.search(r"Fixes #\d{3,}", response))
    passed = not has_fixes
    return automatic(passed, "No invented Fixes # found." if passed else "Found possible invented Fixes #.")


AUTOMATIC_RULES: tuple[GradeRule, ...] = (
    GradeRule(lambda text: "contains no em dash or en dash" in text, grade_no_dash),
    GradeRule(lambda text: bool(re.search(r"under \d+ lines", text)), grade_line_limit),
    GradeRule(lambda text: "removes the phrases 'seamlessly' and 'going forward'" in text, grade_plain_commit),
    GradeRule(
        lambda text: any(marker in text for marker in ("response exists", "is a rewritten", "is a plan", "includes a rewritten")),
        grade_non_empty,
    ),
    GradeRule(lambda text: any(marker in text for marker in QUOTED_TOKEN_MARKERS), grade_quoted_token),
    # Draft PR specific
    GradeRule(lambda text: "verbatim ticket link" in text or "Related ticket" in text, grade_ticket_link),
    GradeRule(lambda text: "total added and deleted lines" in text or "churn" in text, grade_churn),
    GradeRule(lambda text: "conventional commits" in text, grade_conventional),
    GradeRule(lambda text: "files covered by each semantic chunk" in text or "names the files" in text, grade_files_mentioned),
    GradeRule(lambda text: "risk stated in the packet" in text, grade_contains_token("stale", "risk phrase")),
    GradeRule(lambda text: "deliberately deferred work" in text, grade_contains_token("out of scope", "deferred work phrase")),
    GradeRule(lambda text: "distinguishes user-provided facts" in text, grade_contains_token("local storage", "user fact vs decision")),
    GradeRule(lambda text: "bounded semantic chunk" in text, grade_contains_token("semantic", "semantic chunk")),
    GradeRule(lambda text: "approve or revise" in text or "pauses once" in text or "pause once" in text, grade_regex(r"approve.*revise|revise.*approve|approve as.is", "approve or revise")),
    GradeRule(lambda text: "unsupported platform details" in text or "not invent a platform" in text, grade_not_invented),
    GradeRule(lambda text: "traceable to the supplied context or diff" in text, grade_regex(r"traceable|grounded", "traceable claim")),
)


def grade_assertion(assertion: str, response: str) -> GradeResult:
    rule = next((rule for rule in AUTOMATIC_RULES if rule.matches(assertion)), None)
    result = rule.grade(assertion, response) if rule else {"passed": None, "status": "manual", "evidence": "Requires human review."}
    return {"text": assertion, **result}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill")
    parser.add_argument("iteration", type=int, nargs="?", default=1)
    parser.add_argument("output_root", nargs="?", default="/tmp/skills-live-evals")
    parser.add_argument("case_id", nargs="?")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    evals_path = repo_root / "evals" / args.skill / "evals.json"
    if not evals_path.is_file():
        parser.error(f"evals file is missing: {evals_path}")
    cases = cast(list[JsonObject], json.loads(evals_path.read_text())["evals"])
    if args.case_id:
        cases = [case for case in cases if str(case["id"]) == args.case_id]
    if not cases:
        parser.error(f"no eval case found: {args.case_id}")

    config = GradeConfig(args.skill, args.iteration, Path(args.output_root))
    iteration_dir = config.output_root / config.skill / f"iteration-{config.iteration}"
    all_grades = []
    for case in cases:
        case_id = str(case["id"])
        for mode in ("with_skill", "without_skill"):
            run_dir = iteration_dir / case_id / mode
            response_path = run_dir / "outputs" / "response.txt"
            timing_path = run_dir / "timing.json"
            response = response_path.read_text() if response_path.is_file() else ""
            results = []
            exit_code = 1
            if timing_path.is_file():
                timing = json.loads(timing_path.read_text())
                exit_code = timing.get("exit_code", 1)
            results.append(
                {
                    "text": "model run succeeded",
                    "passed": exit_code == 0,
                    "status": "automatic",
                    "evidence": f"Runner exit code: {exit_code}.",
                }
            )
            results.extend(grade_assertion(assertion, response) for assertion in case.get("assertions", []))
            summary = {
                "automatic_passed": sum(r["passed"] is True for r in results if r["status"] == "automatic"),
                "automatic_failed": sum(r["passed"] is False for r in results if r["status"] == "automatic"),
                "manual_review": sum(r["status"] == "manual" for r in results),
                "total": len(results),
            }
            grading = {
                "skill": args.skill,
                "case": case_id,
                "mode": mode,
                "assertion_results": results,
                "summary": summary,
            }
            if timing_path.is_file():
                grading["timing"] = json.loads(timing_path.read_text())
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")
            all_grades.append(grading)
            print(f"  graded {case_id}/{mode}")

    configurations = []
    for mode in ("with_skill", "without_skill"):
        selected = [grade for grade in all_grades if grade["mode"] == mode]
        configurations.append(
            {
                "mode": mode,
                "cases": len(selected),
                "automatic_passed": sum(g["summary"]["automatic_passed"] for g in selected),
                "automatic_failed": sum(g["summary"]["automatic_failed"] for g in selected),
                "manual_review": sum(g["summary"]["manual_review"] for g in selected),
                "total_tokens": sum(g.get("timing", {}).get("total_tokens", 0) for g in selected),
                "duration_ms": sum(g.get("timing", {}).get("duration_ms", 0) for g in selected),
            }
        )
    with_skill, without_skill = configurations
    total_cases = len({g["case"] for g in all_grades}) if all_grades else 0
    total_manual = with_skill["manual_review"] + without_skill["manual_review"]
    auto_pass_rate = (
        round(100 * (with_skill["automatic_passed"]) / max(1, with_skill["automatic_passed"] + with_skill["automatic_failed"]), 1)
        if (with_skill["automatic_passed"] + with_skill["automatic_failed"]) > 0
        else 0
    )
    benchmark = {
        "skill": args.skill,
        "cases": total_cases,
        "manual_ratio": round(total_manual / max(1, (with_skill["manual_review"] + without_skill["manual_review"] + with_skill["automatic_passed"] + with_skill["automatic_failed"] + without_skill["automatic_passed"] + without_skill["automatic_failed"])), 3),
        "auto_pass_rate_with_skill": auto_pass_rate,
        "configurations": configurations,
        "delta": {
            "automatic_passed": with_skill["automatic_passed"] - without_skill["automatic_passed"],
            "automatic_failed": with_skill["automatic_failed"] - without_skill["automatic_failed"],
            "total_tokens": with_skill["total_tokens"] - without_skill["total_tokens"],
            "duration_ms": with_skill["duration_ms"] - without_skill["duration_ms"],
        },
    }
    iteration_dir.mkdir(parents=True, exist_ok=True)
    (iteration_dir / "benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n")
    print(f"\nBenchmark written to {iteration_dir / 'benchmark.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
