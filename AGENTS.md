# Skills

Personal skills for agents. Extends mattpocock/skills; every skill here fills a gap that set does
not cover.

## House rules

- Never use emdashes.
- Every skill is model-invoked or user-invoked, kept in sync: model-invoked omits
  `disable-model-invocation` from `SKILL.md` and the `policy` block from `agents/openai.yaml`;
  user-invoked sets both.
- Every skill has a README entry linking to its `SKILL.md` and naming the mattpocock skill it
  complements.
- Run `pnpm fmt:check` before finishing; `pnpm fmt` to fix.
- Test a skill by running it. An untested rule is a hypothesis.

## Skill creation references

- [Best practices](https://agentskills.io/skill-creation/best-practices.md): read when creating or
  reshaping a skill. Scope, progressive disclosure (`references/`), gotchas, templates, checklists.
- [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md): read
  when writing or changing a `description` frontmatter field. Triggering accuracy.
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills.md): read when adding
  or changing `evals/`. Test cases, assertions, grading, iteration.
- [Using scripts](https://agentskills.io/skill-creation/using-scripts.md): read when adding or
  changing `scripts/`. Self-contained scripts, `--help`, structured output, exit codes.
