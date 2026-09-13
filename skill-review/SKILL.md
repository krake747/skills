---
name: skill-review
description: >-
  Review a skill or agent-facing docs against the skill quality checklist, calibrated for
  multi-model use. Use when the user asks to review or audit a skill, AGENTS.md, task docs, or
  pointer docs. Not for writing or polishing prose; use humanize for that. Report only, never edits.
disable-model-invocation: true
---

# Skill Review

Audit a skill or agent-facing docs against the skill quality checklist, then report findings. Never
edit the target. A review that changes files is not a review.

This skill covers review only. It does not rewrite skills, restructure docs, or run model evals. Do
not stretch it to cover what they do not cover.

## Use this skill when

- The user asks to review or audit a skill: its description, structure, triggers, or boundaries.
- The user asks to review AGENTS.md, task docs, or pointer docs: runbooks, guides, procedures, ADRs,
  architecture and database notes.
- The user names a review concern: over-triggering, context bloat, rigid recipes, tentative stops.

## Do not use this skill when

- The user asks to write or polish prose without asking for a review; use humanize for that. Review
  first, change only when asked separately.
- The change is code behavior, not prose or prompts.

## Follow these rules

Apply every rule. Report findings, change nothing. Assume a multi-model audience unless the user
says otherwise.

- Skills: read `references/skill-checks.md` when the target is a SKILL.md, its description, or its
  references layout.
- Calibration: read `references/normal-model-checks.md` when grading strictness by fragility or
  flagging any recipe or gate.
- Docs: read `references/house-checks.md` when the target is AGENTS.md, task docs, or this repo's
  own conventions.
- Report: one finding per broken rule, ordered by severity, each with file and line evidence.

## Report shape

- What breaks, where (file and line), and which rule it breaks.
- Keep detail in the report. Propose directions, never edits.
