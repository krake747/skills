---
name: instruct
description: >-
  Use when writing or fixing task docs that tell the reader to do something: procedures, runbooks,
  guides, ops notes, ADRs, docs diffs. Enforces task structure: verb headings, one action per line,
  concept-plus-trigger pointers, positive targets, checkable done lines. Use it to fix headings,
  check pointers, or make docs scannable and immediately useful. Triggers on: procedure, runbook,
  guide, ops note, ADR, docs review, pointer check, done lines, task headings. Complements humanize.
---

# Instruct

Write structure first, then voice. Make docs clear, direct, consistent, easy to scan, and
immediately useful.

This is a contract. Break it and the work fails.

This skill covers sentence structure only. It does not set voice. It does not design pointer
systems. Do not stretch these rules to cover what they do not cover.

## Use this skill when

- The text tells the reader to do a task, such as a procedure, a runbook, a guide, an ops note, or
  onboarding.
- The change writes or reviews docs: a docs diff, an ADR, a README section, or an index of docs.
- The user names a structure concern, such as headings, pointers, done lines, or scannability.

## Do not use this skill when

- The text needs natural voice, such as replies, posts, summaries, or announcements.
- The work designs a pointer system from scratch, such as a new skill or a new `AGENTS.md`.
- The change is code behavior, not docs.

## Follow these rules

Apply every rule. Fix the span, not the paragraph. If nothing breaks, change nothing.

### Start headings with verbs

- Use `Create`, `Verify`, `Read`, `Map`, `Deploy`, `Roll back`. Never use a bare noun.
- Avoid gerunds for tasks. Write `Run scoped tests`, not `Testing`.
- Name the object. Write `Close a ticket`, not `Close`.

### Write one action per line

- Put one imperative per bullet. Split fetch plus confirm into two lines.
- Keep sentences short. Split the sentence when the reader must backtrack.
- Prefer active voice. Write `The job writes JSON lines`, not a fragment with no actor.

### Point with concept plus trigger

- Front load the concept plus the when. Write `Secrets: read ops/secrets.md when you add config`.
- Give one trigger per branch. Collapse synonyms that name one branch twice.
- Cut identity the target already carries. Never restate the filename as the whole pointer.

### State the positive target

- State what to do. Pair a hard guardrail with its positive form.
- Write `Link across`, not a bare ban on copying. Write `Add comments only when asked`.
- Keep a ban only when no positive form exists, and pair it with the target action.

### Close each step with a check

- End every procedure with a checkable done line. Name the command plus its expected result.
- Write `Expect green output`, `Open the dev URL and confirm the build serves`.
- Never close with adjectives. Never write that output looks correct.

### Keep one term per concept

- Pick one name and repeat it. Never cycle through synonyms for an established term.
- Expand an abbreviation on first use. Write `backend for frontend (BFF)` once, then `BFF`.
- Hyphenate compound adjectives. Write `user-visible`, `read-only`, `state-driven`.

### Name the concept in links

- Link the concept, not the filename. Write `Secrets: read the rulebook`, with the link on the
  rulebook name.
- Add the section plus the why for long form links. Write
  `Doc: <url> (deploy section, confirms prod target)`.
- Put filenames, key names, and literal values in ops docs or code, not in ADR decision bodies.

## Fail the output

Fail the output when any of these hold.

- A task heading with no verb, a gerund task title, or a vague `Rules` heading.
- Two actions in one bullet line.
- A bare pointer with no trigger, such as a lone `See` line.
- A Verify line with no expected result, or an adjective in place of a result.
- A ban with no paired positive target.
- A `Doc:` link with no section and why.
- A fragment with no verb where a full instruction belongs.

## Place material

- Keep material every reader needs inline.
- Move material only some readers need behind a pointer that names its trigger.
- Keep one fact in one place and link to it. Never copy it.

## Optional voice pass

- An optional humanize pass may follow. It keeps headings, triggers, and done lines intact.
  Structure wins over rhythm here. Parallel imperatives and repeated `Verify` openers are correct in
  procedures.

## Hold the bar

Delete any heading that does not start with a verb. Split any line that holds two actions. Add the
missing trigger, the missing result, or the missing link target. When in doubt, write less. Silence
beats slop.
