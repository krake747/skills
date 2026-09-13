---
name: humanize
description: >-
  Write and polish prose: structure task docs first, then voice. Use when writing procedures,
  runbooks, guides, ADRs, or polishing replies, summaries, docs, commit text. Not for reviewing or
  auditing skills or docs; use skill-review for that. Not for code behavior.
---

# Humanize

Write structure first, then voice. Make docs clear, direct, consistent, easy to scan, and
immediately useful. Then make the writing stop performing and start saying.

This is a contract. Break it and the work fails.

This skill covers task-doc structure and sentence voice only. It does not design pointer systems. Do
not stretch these rules to cover what they do not cover. It does not change code behavior.

## Use this skill when

- The text tells the reader to do a task: a procedure, a runbook, a guide, an ops note, an ADR, or a
  docs diff.
- The text needs natural voice: replies, summaries, commit text, READMEs, posts, or announcements.
- The user names a structure or voice concern: headings, pointers, done lines, or plain wording.

## Do not use this skill when

- The user asks to review or audit the text against a checklist; use skill-review for that.
- The change is code behavior, not prose.

## The work

Two phases, in order.

1. Structure. Verb headings, one action per line, concept-plus-trigger pointers, checkable done
   lines. Fix the span, not the paragraph. If nothing breaks, change nothing.
2. Voice. Five passes: strip filler, swap puffed words, rebuild AI shapes, fix rhythm, guard
   meaning. Use the smallest edit that removes the tell and leave the rest alone.

## Pointers

- Task structure: read `references/structure-headings-actions.md` when fixing headings or splitting
  lines.
- Pointers and checks: read `references/structure-pointers-checks.md` when writing pointers,
  targets, done lines, terms, or links.
- Structure bar: read `references/structure-bar.md` to verify structure before finishing.
- Word tells: read `references/voice-word-tells.md` when cutting filler or swapping puffed words.
- Sentence shape: read `references/voice-sentence-shape.md` when fixing sentence shapes or rhythm
  between sentences.
- Guard: read `references/voice-guard.md` before deleting anything that might carry meaning.
- Voice bar: read `references/voice-and-bar.md` to restore voice and verify the wording before
  finishing.

Structure wins over rhythm in procedures. Parallel imperatives and repeated `Verify` openers are
correct there; a voice pass keeps headings, triggers, and done lines intact.
