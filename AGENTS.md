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
