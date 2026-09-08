# skills

Personal skills that refine how the agent writes code for me. The agent picks them up on its own.

Inspired by [mattpocock/skills](https://github.com/mattpocock/skills).

## Install

```bash
npx skills add krake747/skills
```

Update with: `npx skills update`.

## The flow

### Plan

Changing a plan takes seconds. Changing code takes minutes. For a small change, agree the approach
first. Keep the plan short enough to read. Write open questions down instead of guessing them.

- **[plan-first](plan-first/SKILL.md).** A 20-line plan before code: possible approaches with
  tradeoffs, one recommendation, open questions.

### Build

Readers judge new code against the code next to it. Match the existing patterns first. Then write
the code so the reader mostly sees the normal path: clear types, named steps, data that does not
change under you, bad input turned away early. Add a new piece only when it does real work.

- **[scaffold](scaffold/SKILL.md).** Match the codebase's patterns when writing new code. Copy the
  shape, not the code. Say out loud where you break from it and why.
- **[happy-path](happy-path/SKILL.md).** Types first, normal path first: clear types, guard clauses
  that turn bad input away early, no extra layers.

### Ship

Write one full report of the change. Then shrink it to a title plus body that still reads well in
`git log`. Ask for one round of notes. Check every claim against the final diff. Then create or
update the PR.

- **[draft-pr](draft-pr/SKILL.md).** Draft, create, or update a PR with title plus body: report the
  context, decisions, and risks, propose the title plus body, refine once, then ship it.

### Prose, anywhere

Docs should tell the reader what to do. And read like a person wrote them. First make the structure
clear: headings that start with verbs, one action per line, each step ending with how to check it.
Then set the voice, without breaking any of that.

- **[instruct](instruct/SKILL.md).** Write task docs with verb headings and done lines: procedures,
  runbooks, guides, ops notes, ADRs, and docs changes, one action per line, checkable done lines.
- **[humanize](humanize/SKILL.md).** Any prose the agent writes or edits. Rewrite it the way a
  person would write it.

## Evaluation

Run the keyless Tier 1 quality checks for all skills with
[`scripts/evaluate-skills.sh`](scripts/evaluate-skills.sh). See [`evals/README.md`](evals/README.md)
for setup, scope, and the local Tier 2 command.
