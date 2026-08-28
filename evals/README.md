# Skill Evaluation

Run the keyless Tier 1 checks for every skill in this repository:

```bash
./scripts/evaluate-skills.sh
```

The command uses [NVIDIA SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator) through `uvx`. It
checks schema, PII, licensing, quality, Unicode safety, and scripts without making model calls. No
API key, Docker daemon, or paid evaluation service is required.

Install `uv` first if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The script accepts an optional directory argument for checking a different skill collection:

```bash
./scripts/evaluate-skills.sh ./skills
```

This is a static quality gate, not a measure of whether a skill improves agent output. Live
with-skill versus without-skill evaluation requires model inference and is intentionally outside the
repository's zero-cost default.

## Tier 2

Tier 2 checks semantic overlap locally using Ollama:

```bash
pnpm eval:skills:tier2
```

The default models are `nomic-embed-text` for embeddings and `qwen2.5-coder:3b` for within-skill
duplicate verification. The verifier uses a non-reasoning model because SkillEvaluator requires
structured JSON verdicts. Override it with `SKILL_EVAL_LLM_MODEL`, or override the embedding model
with `SKILL_EVAL_EMBEDDING_MODEL`.

Install the models with:

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5-coder:3b
```

The command compares all skills with `similarity-check`, then checks each skill independently with
`context-optimization-check`. All skill content remains on this machine.

## Live Model Evals

The skill-specific eval cases under `evals/<skill>/evals.json` follow the workflow described by
[agentskills.io](https://agentskills.io/skill-creation/evaluating-skills). Run one skill or one case
with OpenCode:

```bash
pnpm eval:skills:live humanize humanize-commit
```

The runner loads `.env`, stages fixtures in a temporary workspace, runs both with and without the
skill, and writes responses and timing data under `/tmp/skills-live-evals` by default. Use
`SKILL_EVAL_DRY_RUN=1` to verify staging without making model calls. Automated runs require
`OPENAI_API_KEY`; manual assertion grading does not.

Grade saved live results without another model call:

```bash
pnpm eval:skills:grade humanize 1 /tmp/skills-live-evals
```

Append a case ID to grade a partial iteration:

```bash
pnpm eval:skills:grade humanize 1 /tmp/skills-live-evals humanize-commit
```

The grader writes one `grading.json` per configuration and a `benchmark.json` summary. Objective
assertions are checked automatically; prose quality and other contextual assertions are marked for
human review.

Generate a standalone review page without another model call:

```bash
pnpm eval:skills:review humanize 1 /tmp/skills-live-evals
```

The page is written beside the iteration benchmark. Review each paired output and download the
resulting `feedback.json` for the next iteration.
