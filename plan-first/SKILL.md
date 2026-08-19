---
name: plan-first
description: >-
  Plan before code for small to medium tasks. Use when the user wants a quick plan before building:
  "how to", "approach", "strategy", "let's plan", "planning". For deep design work, run the
  interview skill instead.
---

# Plan First

Plan first. Code second. Every significant piece of work runs one loop:

A plan takes seconds to change, code takes minutes. Agree the approach while it is cheap.

Small tasks get a quick plan, under 20 lines, so the user will actually read it. Deep design work
belongs in the interview skill.

1. **Plan.** Align on approach before writing anything.
2. **Execute.** Write code matching the agreed plan.
3. **Test.** Validate it matches the plan. Run tests, check types, manual QA.
4. **Commit.** Ship, but only when the user asks. Loop again.

## Rules

- Use short sentences and bullets, with clear structure.
- End each plan with unresolved questions. Don't guess; ask.
- Never skip to Execute without a plan. If the user asks for code without one, say "Let's plan
  first."

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
