---
name: happy-path
description: >-
  Implement behavior type-first with the happy path flat and readable. Use when writing or changing
  behavior after the surrounding pattern is known. Not for matching existing structure; use scaffold
  for fit.
---

# Happy Path First

Design for the normal user flow. If the happy path is 95% of runtime behavior, it should be 95% of
the code a reader sees. Code is read along the main flow; the edge cases bury it.

Start with context. Inspect the existing code, callsites, data flow, and nearby conventions.
Understand the real use case before choosing abstractions. Preserve good existing patterns; do not
impose a generic architecture.

The examples use one domain, order execution on a trading desk, so the bad and good shapes are
comparable. They are written in pseudocode; apply the shapes in whatever language you work in.

## Pointers

- Types and boundaries: read `references/types-and-boundaries.md` when modeling the domain, parsing
  input, or deciding mutability.
- Pipelines and orchestrators: read `references/pipelines-and-orchestrators.md` when shaping the
  top-level flow, stages, or validation branches.
- Simplicity: read `references/simplicity.md` before adding layers, handling edge cases, extracting
  helpers, or writing tests.

## Completion standard

Finish the complete change, run focused verification, delete temporary artifacts, and do one final
simplification pass. The result should feel boring, obvious, typed, cohesive, and native to the
codebase.

See [scaffold](../scaffold/SKILL.md) for matching existing patterns.
