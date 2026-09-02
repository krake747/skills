#!/usr/bin/env python3
"""Create a standalone HTML review page for a live skill evaluation."""

from __future__ import annotations

import argparse
import html
import json
import subprocess
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from typing import Any

type JsonObject = dict[str, Any]
MODES = (("with_skill", "With skill"), ("without_skill", "Without skill"))
GRADE_STATES: dict[bool | None, tuple[str, str]] = {
    True: ("PASS", "pass"),
    False: ("FAIL", "fail"),
    None: ("REVIEW", "review"),
}


@dataclass(frozen=True, slots=True)
class ReviewConfig:
    skill: str
    iteration: int
    output_root: Path
    output: Path | None
    open_browser: bool


def read_json(path: Path, default: JsonObject) -> JsonObject:
    try:
        value = json.loads(path.read_text())
        return value if isinstance(value, dict) else default
    except (OSError, json.JSONDecodeError):
        return default


def read_text(path: Path) -> str:
    try:
        return path.read_text()
    except OSError:
        return "No response found."


def render_grading(path: Path) -> str:
    grading = read_json(path, {})
    summary = grading.get("summary", {})
    rows = []
    for result in grading.get("assertion_results", []):
        if not isinstance(result, dict):
            continue
        label, css = GRADE_STATES.get(result.get("passed"), GRADE_STATES[None])
        rows.append(
            f'<li class="{css}"><strong>{label}</strong> '
            f'{html.escape(str(result.get("text", "")))}'
            f'<small>{html.escape(str(result.get("evidence", "")))}</small></li>'
        )
    if not rows:
        return "<p>No grading data. Run pnpm eval:skills:grade first.</p>"
    manual = summary.get("manual_review", 0)
    auto_pass = summary.get("automatic_passed", 0)
    auto_fail = summary.get("automatic_failed", 0)
    badge = "all auto" if manual == 0 else f"{manual} need manual review"
    return (
        f'<p><span class="badge">{badge}</span> {auto_pass} automatic passes, '
        f'{auto_fail} automatic failures, '
        f'{manual} manual reviews.</p>'
        f'<ul class="grades">{"".join(rows)}</ul>'
    )


def render_case(case_dir: Path, case: JsonObject, index: int) -> str:
    prompt = html.escape(str(case.get("prompt", "")))
    sections = []
    for mode, label in MODES:
        run_dir = case_dir / mode
        response = html.escape(read_text(run_dir / "outputs/response.txt"))
        grading = render_grading(run_dir / "grading.json")
        timing = read_json(run_dir / "timing.json", {})
        trajectory = (run_dir / "trajectory.jsonl").exists()
        grading_file = (run_dir / "grading.json").exists()
        links = []
        if grading_file:
            links.append(f'<a href="{html.escape(str((run_dir / "grading.json").relative_to(case_dir.parent.parent)))}">grading.json</a>')
        if trajectory:
            links.append(f'<a href="{html.escape(str((run_dir / "trajectory.jsonl").relative_to(case_dir.parent.parent)))}">trajectory</a>')
        links_html = " · ".join(links) if links else "no artifacts"
        sections.append(
            f'<article class="run"><h3>{label}</h3>'
            f'<p class="meta">{timing.get("total_tokens", 0)} tokens, '
            f'{timing.get("duration_ms", 0)} ms · {links_html}</p>'
            f'<pre>{response}</pre><details><summary>Grades</summary>{grading}</details></article>'
        )
    return (
        f'<section class="case" id="case-{index}"><h2>{index + 1}. '
        f'{html.escape(case_dir.name)}</h2><p class="prompt">{prompt}</p>'
        f'<div class="runs">{"".join(sections)}</div>'
        f'<label>Feedback<textarea data-run="{html.escape(case_dir.name)}" '
        f'placeholder="What should change? What worked?"></textarea></label></section>'
    )


def benchmark_header(benchmark: JsonObject) -> str:
    if not benchmark:
        return "<p>No benchmark data. Run grade first.</p>"
    delta = benchmark.get("delta", {})
    configs = benchmark.get("configurations", [])
    with_cfg = next((c for c in configs if c.get("mode") == "with_skill"), {})
    without_cfg = next((c for c in configs if c.get("mode") == "without_skill"), {})
    return (
        f'<div class="bench">'
        f'<span>with_skill {with_cfg.get("automatic_passed", 0)} pass {with_cfg.get("automatic_failed", 0)} fail</span>'
        f'<span>without_skill {without_cfg.get("automatic_passed", 0)} pass {without_cfg.get("automatic_failed", 0)} fail</span>'
        f'<span>delta {delta.get("automatic_passed", 0):+} pass {delta.get("automatic_failed", 0):+} fail · '
        f'{delta.get("total_tokens", 0):+} tokens {delta.get("duration_ms", 0):+} ms</span>'
        f'</div>'
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill")
    parser.add_argument("iteration", type=int, nargs="?", default=1)
    parser.add_argument("output_root", nargs="?", default="/tmp/skills-live-evals")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--open", action="store_true", help="Open the review page in the browser")
    args = parser.parse_args()

    config = ReviewConfig(args.skill, args.iteration, Path(args.output_root), args.output, args.open)
    iteration_dir = config.output_root / config.skill / f"iteration-{config.iteration}"
    if not iteration_dir.is_dir():
        raise SystemExit(f"Iteration directory is missing: {iteration_dir}")

    cases: list[tuple[Path, JsonObject]] = []
    for case_dir in sorted(p for p in iteration_dir.iterdir() if p.is_dir()):
        # Support both old and new metadata locations
        metadata = read_json(case_dir / "eval_metadata.json", {})
        if not metadata:
            # Try nested per-mode location from older live runs
            for mode, _ in MODES:
                cand = case_dir / mode / "eval_metadata.json"
                if cand.is_file():
                    metadata = read_json(cand, {})
                    break
        if isinstance(metadata, dict) and metadata.get("prompt"):
            cases.append((case_dir, metadata))
    if not cases:
        raise SystemExit(f"No eval cases found in {iteration_dir}")

    sections = [render_case(path, metadata, i) for i, (path, metadata) in enumerate(cases)]
    benchmark = read_json(iteration_dir / "benchmark.json", {})
    benchmark_text = html.escape(json.dumps(benchmark, indent=2))
    bench_header = benchmark_header(benchmark)
    case_options = "".join(
        f'<option value="case-{i}">{html.escape(path.name)}</option>' for i, (path, _) in enumerate(cases)
    )
    output = config.output or iteration_dir / "review.html"
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>{html.escape(config.skill)} eval review</title>
 <style>
body{{font:16px system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:24px;background:#f6f5f1;color:#20201d}}
header{{position:sticky;top:0;background:#20201d;color:#fff;padding:16px;z-index:2}}h1,h2,h3{{margin-top:0}}
select,button{{padding:8px 12px;margin-right:8px}}.case{{background:#fff;border:1px solid #ddd8cc;padding:20px;margin:20px 0}}
.prompt{{white-space:pre-wrap;background:#f1efe8;padding:12px}}.runs{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.run{{border:1px solid #ddd8cc;padding:14px}}pre{{white-space:pre-wrap;overflow:auto;background:#faf9f5;padding:12px;min-height:80px}}
.meta,small{{color:#716f67;font-size:.85em}}textarea{{display:block;width:100%;min-height:90px;margin-top:8px;box-sizing:border-box;padding:10px}}
details{{margin-top:12px}}.grades{{padding:0;list-style:none}}.grades li{{padding:6px 0;border-bottom:1px solid #eee}}.grades small{{display:block;margin-left:54px}}
.pass{{color:#47753e}}.fail{{color:#a33}}.review{{color:#87651a}}@media(max-width:700px){{.runs{{grid-template-columns:1fr}}}}
.bench{{display:flex;gap:16px;flex-wrap:wrap;margin:12px 0;font-size:.9em}}.bench span{{background:#fff;color:#20201d;padding:6px 10px;border:1px solid #ddd8cc}}
.badge{{background:#e8f0e4;color:#2d4a26;padding:2px 8px;font-size:.8em;margin-right:8px;border:1px solid #cbdcc5}}
 </style></head><body><header><h1>{html.escape(config.skill)} eval review</h1>
 {bench_header}
<select id="case">{case_options}</select><button onclick="downloadFeedback()">Download feedback.json</button></header>
{"".join(sections)}<details><summary>Benchmark JSON</summary><pre>{benchmark_text}</pre></details>
<script>
const select=document.querySelector('#case');select.addEventListener('change',()=>document.querySelectorAll('.case').forEach((x,i)=>x.hidden=x.id!==select.value));
document.querySelectorAll('.case').forEach((x,i)=>x.hidden=i!==0);
function downloadFeedback(){{const reviews=[...document.querySelectorAll('textarea')].map(x=>({{run_id:x.dataset.run,feedback:x.value,timestamp:new Date().toISOString()}}));const blob=new Blob([JSON.stringify({{reviews,status:'complete'}},null,2)],{{type:'application/json'}});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='feedback.json';a.click();URL.revokeObjectURL(a.href)}}
</script></body></html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page)
    print(f"Review written to {output}")
    if config.open_browser:
        try:
            webbrowser.open(f"file://{output.resolve()}")
        except Exception as e:
            print(f"Could not open browser: {e}", flush=True)
        # Also try xdg-open as fallback on Linux
        try:
            subprocess.run(["xdg-open", str(output)], check=False)
        except Exception:
            pass


if __name__ == "__main__":
    main()
