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
