#!/usr/bin/env python3
"""Run OpenCode eval cases with and without a skill."""

from __future__ import annotations

import argparse
import json
import os
import re
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


def copy_skill_dir(config: RunConfig, destination_root: Path) -> None:
    source_dir = config.repo_root / config.skill
    for item in source_dir.rglob("*"):
        if item.is_file():
            rel = item.relative_to(source_dir)
            dest = destination_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)


def prepare_workspace(config: RunConfig, paths: RunPaths, case: EvalCase, mode: str) -> None:
    if mode == "with_skill":
        skill_dest = paths.workspace / ".agents" / "skills" / config.skill
        skill_dest.mkdir(parents=True, exist_ok=True)
        copy_skill_dir(config, skill_dest)

    for fixture in case.get("files", []):
        source = config.eval_dir / fixture
        destination = paths.workspace / fixture
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_file():
            shutil.copy2(source, destination)
        elif source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)

    fixtures_list = "\n".join(f"- {f}" for f in case.get("files", []))
    (paths.root / "fixtures.json").write_text(
        json.dumps({"files": case.get("files", []), "list": fixtures_list}, indent=2) + "\n"
    )


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
    texts: list[str] = []
    for event in events:
        if not isinstance(event, dict):
            continue
        event_type = event.get("type", "")
        if event_type in ("text", "assistant", "assistant_text"):
            part = event.get("part", {})
            if isinstance(part, dict) and part.get("text"):
                texts.append(str(part["text"]))
            elif isinstance(event.get("text"), str):
                texts.append(str(event["text"]))
        elif event_type == "message" and isinstance(event.get("message"), dict):
            msg = event["message"]
            if isinstance(msg.get("content"), str):
                texts.append(str(msg["content"]))
            elif isinstance(msg.get("content"), list):
                for block in msg["content"]:
                    if isinstance(block, dict) and block.get("text"):
                        texts.append(str(block["text"]))
        if isinstance(event.get("content"), str) and event_type not in ("text", "assistant"):
            # Fallback for plain content fields
            if event.get("role") == "assistant":
                texts.append(str(event["content"]))
    if texts:
        return "\n".join(texts)
    # Fallback: try to extract any text field from raw JSONL
    fallback: list[str] = []
    for event in events:
        for key in ("text", "content", "output"):
            if isinstance(event.get(key), str) and event[key].strip():
                fallback.append(str(event[key]).strip())
    return "\n".join(fallback)


def token_count(events: list[JsonObject]) -> int:
    total = 0
    for event in events:
        if not isinstance(event, dict):
            continue
        # Direct tokens field
        for key in ("tokens", "usage", "token_usage"):
            val = event.get(key)
            if isinstance(val, dict):
                for tkey in ("total", "total_tokens", "input_tokens", "output_tokens", "completion_tokens", "prompt_tokens"):
                    if isinstance(val.get(tkey), int):
                        total += int(val[tkey])
        # Nested part.tokens
        part = event.get("part", {})
        if isinstance(part, dict):
            tokens = part.get("tokens", {})
            if isinstance(tokens, dict):
                if isinstance(tokens.get("total"), int):
                    total += int(tokens["total"])
                if isinstance(tokens.get("total_tokens"), int):
                    total += int(tokens["total_tokens"])
        # message.usage
        msg = event.get("message", {})
        if isinstance(msg, dict):
            usage = msg.get("usage", {})
            if isinstance(usage, dict):
                for tkey in ("total_tokens", "total", "input_tokens", "output_tokens"):
                    if isinstance(usage.get(tkey), int):
                        total += int(usage[tkey])
    return total


def synthetic_dry_run_response(case: EvalCase, mode: str, model_ref: str) -> str:
    case_id = str(case.get("id", ""))
    files = case.get("files", [])
    has_ticket = any("user-context" in f for f in files)
    has_diff = any(f.endswith(".diff") or "change.diff" in f or "large" in f for f in files)
    # Short synthetic for reconcile case to keep under 15 lines
    if "reconcile" in case_id:
        parts: list[str] = []
        parts.append("feat: persist report filters across reloads")
        if has_ticket:
            parts.append("Related: [PROJ-123](https://tickets.example.com/PROJ-123)")
        parts.append("Why: Users lose report filters on refresh.")
        parts.append("What changed: saveFilters and loadFilters with localStorage")
        parts.append("Risks: stale local data after filter format change")
        parts.append("Traceable to diff and user context.")
        parts.append("+14 -2 | the whole PR")
        parts.append("src/reports/filterStore.ts:1-12")
        parts.append("Do you want to approve as-is or revise?")
        prefix = f"dry run {mode} ({model_ref}) - {case_id}"
        return f"{prefix}\n" + "\n".join(parts)
    parts: list[str] = []
    parts.append("+14 -2 | the whole PR")
    parts.append("")
    parts.append("Why: Users lose report filters on refresh, restored via local storage.")
    if has_ticket:
        parts.append("Related: [PROJ-123](https://tickets.example.com/PROJ-123)")
    parts.append("")
    parts.append("Chunk 1 +8 -2 | filterStore.ts - report filter persistence - semantic chunk")
    parts.append("- saveFilters and loadFilters use localStorage with key report-filters")
    parts.append("- covers src/reports/filterStore.ts:1-12")
    if has_diff:
        parts.append("")
        parts.append("What changed:")
        parts.append("- Persist filters with saveFilters, restore with loadFilters")
    parts.append("")
    parts.append("Key decisions: localStorage over server setting, restore before first render")
    parts.append("")
    parts.append("Risks and follow-ups: stale local data after filter format change, migration out of scope")
    parts.append("")
    parts.append("feat: persist report filters across reloads")
    parts.append("")
    parts.append("Do you want to approve as-is or revise? Reply approve or share edits.")
    prefix = f"dry run {mode} ({model_ref}) - {case_id}"
    return f"{prefix}\n\n" + "\n".join(parts)


def run_case(config: RunConfig, case: EvalCase, mode: str) -> int:
    case_id = str(case["id"])
    paths = run_paths(config, case, mode)
    paths.outputs.mkdir(parents=True, exist_ok=True)
    write_metadata(paths.root / "eval_metadata.json", case)
    prepare_workspace(config, paths, case, mode)

    (paths.root / "prompt.txt").write_text(str(case["prompt"]) + "\n")

    started = time.perf_counter()
    raw = ""
    response = ""
    exit_code = 0
    total_tokens = 0

    if config.dry_run:
        response = synthetic_dry_run_response(case, mode, config.model_ref)
        (paths.root / "trajectory.jsonl").write_text("")
        (paths.root / "stderr.log").write_text("")
        (paths.root / "raw_stdout.log").write_text(response)
    else:
        # Retry once on transient 429 or 5xx
        attempts = 0
        max_attempts = 2
        while attempts < max_attempts:
            attempts += 1
            process = subprocess.run(opencode_command(paths, config, case), capture_output=True, text=True, check=False)
            raw = process.stdout
            exit_code = process.returncode
            (paths.root / "stderr.log").write_text(process.stderr)
            (paths.root / "raw_stdout.log").write_text(raw)
            (paths.root / "trajectory.jsonl").write_text(raw)
            events = parse_events(raw)
            response = response_from(events)
            if not response:
                # Fallback to raw stdout if no JSONL text event found
                if raw.strip() and "{" not in raw[:200]:
                    response = raw.strip()
                elif raw.strip():
                    # Try to extract text between JSON values
                    texts = re.findall(r'"text"\s*:\s*"([^"]+)"', raw)
                    if texts:
                        response = "\n".join(texts)
            total_tokens = token_count(events)
            # Retry on rate limit or server error markers
            stderr_lower = process.stderr.lower()
            if exit_code != 0 and attempts < max_attempts and any(x in stderr_lower for x in ("429", "500", "502", "503", "rate limit", "timeout", "temporarily")):
                time.sleep(2 * attempts)
                continue
            break
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
    iteration_dir = output_root / args.skill / f"iteration-{iteration}"
    if iteration_dir.is_dir() and not dry_run:
        existing = any(iteration_dir.iterdir())
        if existing:
            print(f"Warning: {iteration_dir} already exists, appending or overwriting cases.", flush=True)
    config = RunConfig(repo_root, eval_dir, output_root, args.skill, iteration, model_ref, dry_run)
    status = 0
    for case in cases:
        for mode in MODES:
            status = run_case(config, case, mode) or status
    print(f"\nResults written to {output_root / args.skill / f'iteration-{iteration}'}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
