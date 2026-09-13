---
name: instruct
description: >-
  Structure task docs that tell the reader to do something. Use when writing or fixing procedures,
  runbooks, guides, or ADRs. Not for voice polish or code behavior.
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

- Headings and actions: read `references/headings-and-actions.md` when fixing headings or splitting
  lines.
- Pointers and checks: read `references/pointers-and-checks.md` when writing pointers, targets, done
  lines, terms, or links.
- Bar: read `references/bar.md` to verify the output before finishing.

## Optional voice pass

- An optional humanize pass may follow. It keeps headings, triggers, and done lines intact.
  Structure wins over rhythm here. Parallel imperatives and repeated `Verify` openers are correct in
  procedures.
