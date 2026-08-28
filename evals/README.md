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
