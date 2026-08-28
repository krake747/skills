#!/usr/bin/env python3
"""Run OpenCode eval cases with and without a skill."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict, cast

type JsonObject = dict[str, Any]
MODES: tuple[str, ...] = ("with_skill", "without_skill")


class EvalCase(TypedDict, total=False):
    id: str | int
    prompt: str
    assertions: list[str]
    files: list[str]


@dataclass(frozen=True)
class RunConfig:
    repo_root: Path
    eval_dir: Path
    output_root: Path
    skill: str
    iteration: int
    model_ref: str
    dry_run: bool


@dataclass(frozen=True)
class RunPaths:
    root: Path
    workspace: Path
    outputs: Path


def run_paths(config: RunConfig, case: EvalCase, mode: str) -> RunPaths:
    root = config.output_root / config.skill / f"iteration-{config.iteration}" / str(case["id"]) / mode
    return RunPaths(root, root / "workspace", root / "outputs")


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def write_metadata(path: Path, case: EvalCase) -> None:
    path.write_text(
        json.dumps(
            {
                "eval_id": str(case["id"]),
                "eval_name": str(case["id"]),
                "prompt": case["prompt"],
                "assertions": case.get("assertions", []),
            },
            indent=2,
        )
        + "\n"
    )


def prepare_workspace(config: RunConfig, paths: RunPaths, case: EvalCase, mode: str) -> None:
    if mode == "with_skill":
        skill_path = paths.workspace / ".agents" / "skills" / config.skill / "SKILL.md"
        skill_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(config.repo_root / config.skill / "SKILL.md", skill_path)

    for fixture in case.get("files", []):
        source = config.eval_dir / fixture
        destination = paths.workspace / fixture
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def opencode_command(paths: RunPaths, config: RunConfig, case: EvalCase) -> list[str]:
    return [
        "opencode",
        "run",
        "--dir",
        str(paths.workspace),
        "--model",
        config.model_ref,
        "--format",
        "json",
        "--pure",
        (
            "Read the supplied task and attached fixture files. Return the requested result "
            "in your response. Do not modify files. "
            + str(case["prompt"])
        ),
    ]


def parse_events(raw: str) -> list[JsonObject]:
    return [event for line in raw.splitlines() if (event := parse_event(line)) is not None]


def parse_event(line: str) -> JsonObject | None:
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        return None
    return event if isinstance(event, dict) else None


def response_from(events: list[JsonObject]) -> str:
    return "\n".join(
        str(event["part"]["text"])
        for event in events
        if event.get("type") == "text" and event.get("part", {}).get("text")
    )


def token_count(events: list[JsonObject]) -> int:
    return sum(event.get("part", {}).get("tokens", {}).get("total", 0) for event in events)


def run_case(config: RunConfig, case: EvalCase, mode: str) -> int:
    case_id = str(case["id"])
    paths = run_paths(config, case, mode)
    paths.outputs.mkdir(parents=True, exist_ok=True)
    write_metadata(paths.root.parent / "eval_metadata.json", case)
    prepare_workspace(config, paths, case, mode)

    started = time.perf_counter()
    if config.dry_run:
        raw = ""
        response = f"dry run: {mode} {case_id} ({config.model_ref})"
        exit_code = 0
        total_tokens = 0
        (paths.root / "trajectory.jsonl").write_text("")
    else:
        process = subprocess.run(opencode_command(paths, config, case), capture_output=True, text=True, check=False)
        raw = process.stdout
        exit_code = process.returncode
        (paths.root / "stderr.log").write_text(process.stderr)
        events = parse_events(raw)
        response = response_from(events)
        total_tokens = token_count(events)
        (paths.root / "trajectory.jsonl").write_text(raw)

    if not response:
        response = "No text response was produced. See trajectory.jsonl and stderr.log."
    (paths.outputs / "response.txt").write_text(response + "\n")
    duration_ms = round((time.perf_counter() - started) * 1000)
    (paths.root / "timing.json").write_text(
        json.dumps(
            {
                "skill": config.skill,
                "case": case_id,
                "mode": mode,
                "model": config.model_ref,
                "duration_ms": duration_ms,
                "total_tokens": total_tokens,
                "exit_code": exit_code,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"  {case_id}/{mode}: {paths.root}")
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill")
    parser.add_argument("case_id", nargs="?")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    load_dotenv(repo_root / ".env")
    eval_dir = repo_root / "evals" / args.skill
    evals_path = eval_dir / "evals.json"
    if not (repo_root / args.skill / "SKILL.md").is_file() or not evals_path.is_file():
        parser.error(f"skill or evals file is missing: {args.skill}")

    provider = os.environ.get("SKILL_EVAL_LLM_PROVIDER", "openai")
    model = os.environ.get("SKILL_EVAL_LLM_MODEL", "gpt-5.6-luna")
    model_ref = os.environ.get("SKILL_EVAL_MODEL", f"{provider}/{model}")
    dry_run = os.environ.get("SKILL_EVAL_DRY_RUN") == "1"
    if provider == "openai" and not os.environ.get("OPENAI_API_KEY") and not dry_run:
        parser.error("OPENAI_API_KEY is missing. Add it to .env or the environment.")
    if not shutil.which("opencode") and not dry_run:
        parser.error("opencode is required")

    cases = cast(list[EvalCase], json.loads(evals_path.read_text())["evals"])
    if args.case_id:
        cases = [case for case in cases if str(case["id"]) == args.case_id]
    if not cases:
        parser.error(f"no eval case found: {args.case_id}")

    output_root = Path(os.environ.get("SKILL_EVAL_OUTPUT_DIR", "/tmp/skills-live-evals"))
    iteration = int(os.environ.get("SKILL_EVAL_ITERATION", "1"))
    config = RunConfig(repo_root, eval_dir, output_root, args.skill, iteration, model_ref, dry_run)
    status = 0
    for case in cases:
        for mode in MODES:
            status = run_case(config, case, mode) or status
    print(f"\nResults written to {output_root / args.skill / f'iteration-{iteration}'}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
