---
name: plan-first
description: >-
  Plan before code for small to medium tasks. Use when the user asks for a plan before building.
  Skips one-line or copy-only fixes.
---

# Plan First

Run the loop below. Aligning while changes are cheap keeps implementation focused.

A plan takes seconds to change, code takes minutes. Agree the approach while it is cheap.

Small tasks get a quick plan, under 20 lines, so the user will actually read it. Deep design work
gets a longer plan outside this loop.

1. **Plan.** Align on approach before writing anything.
2. **Execute.** When the request includes building, write code matching the agreed plan without
   stopping for approval at each step.
3. **Test.** Validate it matches the plan. Run focused checks for the change.
4. **Commit.** Ship only when the user asks. When the request is plan-only, stop after the plan.

## Rules

- One-line or copy-only fixes may skip the written plan.
- Otherwise align on approach before writing anything. If the user asks for code without one, say
  "Let's plan first."
- Use short sentences and bullets, with clear structure.
- End each plan with unresolved questions. Don't guess; ask.

## Plan template

# Plan: [feature name]

## Approach

- Option A → tradeoff
- Option B → tradeoff
- Recommended: [option] because [reason]

## Unresolved

- [question 1]
- [question 2]

User scans, approves or adjusts, then you execute.
