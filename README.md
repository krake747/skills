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
[draft-pr](draft-pr/SKILL.md) turns the reviewed diff into a PR description.

1. **Align.** Big change: `/grill-me` or `/grill-with-docs`. Small change:
   [plan-first](plan-first/SKILL.md) hands you a 20-line plan instead of the interview.
2. **Spec and tickets.** `/to-spec`, `/to-tickets`, unchanged.
3. **Build.** `/implement` drives `/tdd`. Before writing code, [scaffold](scaffold/SKILL.md) fits it
   to the codebase's patterns; [happy-path](happy-path/SKILL.md) keeps the valid flow dominant as
   you go.
4. **Review.** `/code-review` checks the diff against the spec. Then [draft-pr](draft-pr/SKILL.md)
   writes the PR description the review fed on and flags the judgment calls the diff hides.
5. **Prose, anywhere.** [humanize](humanize/SKILL.md) makes text the agent writes read like a person
   wrote it.

Some skills fire on their own, some you must trigger.

| Skill      | Invoked by | When                                                        |
| ---------- | ---------- | ----------------------------------------------------------- |
| plan-first | agent      | Start of a small change, before choosing abstractions       |
| humanize   | agent      | Any prose the agent writes or edits                         |
| scaffold   | agent      | Adding new code to an existing codebase                     |
| happy-path | agent      | Starting an implementation, to keep the valid flow dominant |
| draft-pr   | you        | After code-review, to write the PR description              |

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
- **[draft-pr](draft-pr/SKILL.md).** Draft a PR description by walking the diff in small approved
  chunks; each chunk feeds the draft, and judgment calls made on your own surface for a veto before
  merge. Complements code-review, which checks the diff rather than writing the PR's story.
