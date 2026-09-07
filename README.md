# skills

An extension to [mattpocock/skills](https://github.com/mattpocock/skills). I run his full set; this
repo holds the gaps that set does not cover.

```bash
npx skills add krake747/skills
```

## Basic user guide

Install mattpocock/skills first and run `/setup-matt-pocock-skills` once per repo, then add this
set. The loop below is his, unchanged; these skills plug its gaps. He grills every change; I grill
the big ones and let [plan-first](plan-first/SKILL.md) handle the small.
[scaffold](scaffold/SKILL.md) and [happy-path](happy-path/SKILL.md) shape the build, and
[draft-pr](draft-pr/SKILL.md) turns the reviewed diff into a PR title plus body, then creates or
updates the PR.

1. **Align.** Big change: `/grill-me` or `/grill-with-docs`. Small change:
   [plan-first](plan-first/SKILL.md) hands you a 20-line plan instead of the interview.
2. **Spec and tickets.** `/to-spec`, `/to-tickets`, unchanged.
3. **Build.** `/implement` drives `/tdd`. Before writing code, [scaffold](scaffold/SKILL.md) fits it
   to the codebase's patterns; [happy-path](happy-path/SKILL.md) keeps the valid flow dominant as
   you go.
4. **Review.** `/code-review` checks the diff against the spec. Then [draft-pr](draft-pr/SKILL.md)
   analyzes the diff, reports context, decisions and risks, proposes a squash-ready PR body to
   refine in one loop, then creates or updates the PR.
5. **Prose, anywhere.** [humanize](humanize/SKILL.md) makes text the agent writes read like a person
   wrote it. [instruct](instruct/SKILL.md) structures task docs (procedures, runbooks, guides)
   before humanize sets the voice.

All skills fire on their own.

| Skill      | Invoked by | When                                                        |
| ---------- | ---------- | ----------------------------------------------------------- |
| plan-first | agent      | Start of a small change, before choosing abstractions       |
| humanize   | agent      | Any prose the agent writes or edits                         |
| scaffold   | agent      | Adding new code to an existing codebase                     |
| happy-path | agent      | Starting an implementation, to keep the valid flow dominant |
| draft-pr   | agent      | Draft, create, or update a PR with title plus body          |
| instruct   | agent      | Write task docs with verb headings and done lines           |

## Evaluation

Run the keyless Tier 1 quality checks for all skills with
[`scripts/evaluate-skills.sh`](scripts/evaluate-skills.sh). See [`evals/README.md`](evals/README.md)
for setup, scope, and the local Tier 2 command.

## Skills

- **[plan-first](plan-first/SKILL.md).** Plan before code. A lightweight 20-line plan for small
  tasks, complementing the grilling interview.
- **[humanize](humanize/SKILL.md).** Rewrite text so it reads like a person wrote it. Complements
  writing-for-agents, which serves agents, not humans.
- **[happy-path](happy-path/SKILL.md).** Write code type-first and happy-path-first: typed
  pipelines, immutable data, guard clauses that leave before the valid flow. Complements implement
  and scaffold.
- **[scaffold](scaffold/SKILL.md).** Match the codebase's existing patterns when writing new code.
  Complements codebase-design and implement.
- **[draft-pr](draft-pr/SKILL.md).** Analyze the diff, report context, decisions and risks, propose
  a conventional PR title plus body that survives squash, to refine in one loop, then create or
  update the PR. Complements code-review, which checks the diff rather than writing the PR's story.
- **[instruct](instruct/SKILL.md).** Write procedures, runbooks, guides, ops notes, ADRs, and docs
  changes with verb headings, one action per line, and checkable done lines. Complements
  writing-for-agents and pairs with humanize: instruct sets task structure, humanize sets voice.
