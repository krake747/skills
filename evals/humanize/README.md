# Humanize Evals

These cases follow the evaluation workflow from
[agentskills.io](https://agentskills.io/skill-creation/evaluating-skills).

Run each case in a clean session twice:

- `with_skill`: load `humanize/SKILL.md`
- `without_skill`: use the same prompt without loading the skill

Save generated files and responses under an external workspace, for example:

```text
humanize-workspace/iteration-1/<case-id>/with_skill/outputs/
humanize-workspace/iteration-1/<case-id>/without_skill/outputs/
```

Record `timing.json` for each run, grade the assertions in `evals.json`, and compare the two
configurations in `benchmark.json`. Review prose quality manually after the assertion grading.

Automated model runs require a provider API key. Manual runs and local assertion review do not.
