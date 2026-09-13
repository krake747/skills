# House Checks

Check the target against this repo's own conventions. One finding per broken rule, with file and
line evidence.

## Voice and format

- An em dash or en dash anywhere. A semicolon between related clauses is fine.
- `pnpm fmt:check` fails on any touched file. Run `pnpm fmt` to fix, then re-check.

## Skill wiring

- A missing README entry. Every skill links its `SKILL.md` from the README flow and names the
  mattpocock skill it complements.
- Invocation mode out of sync. Model-invoked omits `disable-model-invocation` from `SKILL.md` and
  the `policy` block from `agents/openai.yaml`; user-invoked sets both.
- A stale `agents/openai.yaml` description. The `short_description` must match the current
  `SKILL.md` scope after every reshape.

## Evaluation

- Behavior changed with no `evals/` coverage. New or reshaped rules need cases with prompts,
  expected outputs, and assertions, following `evals/README.md`.
- An untested rule. Run the skill against a real target before claiming it works; a live dry run
  stages fixtures without a model call, a full run grades with and without the skill.
