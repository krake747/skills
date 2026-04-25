---
name: draft-plan
description:
  Draft Plan - planning coach that guides agents through the Plan → Execute → Test → Commit loop.
  ALWAYS use this skill when user mentions planning, strategy, approach, "how to", or when user asks
  agent to write code without having worked through a plan first. Make sure to use this skill
  whenever the user wants to build something new, discuss a feature, or tackle a non-trivial task.
---

# Plan Mode

The agent uses a structured 4-step loop for all significant code work:

## The Loop

1. **Plan** - Think through approach with user. Discuss strategy, tradeoffs, edge cases. Get
   alignment on what to build before writing anything.

2. **Execute** - Write code matching the agreed plan. NOT figuring out what to build, you've already
   done that.

3. **Test** - Validate implementation matches plan. Run tests, check types, manual QA.

4. **Commit** - Ship it. Loop again for next piece.

## Key Rules

- **Keep plans extremely concise.** Sacrifice grammar for scannability. Short sentences, bullet
  points, clear structure.

- **End each plan with unresolved questions.** If anything is unclear, list it explicitly. Don't
  guess; ask.

- **Never skip to Execute without Plan.** If user asks to write code without a plan, push back. Say:
  "Let's plan first."

- **Treat code gen without planning as anti-pattern.** The agent knows the user will get better
  outputs by planning first.

## Triggering

ALWAYS use this skill when:

- User mentions any planning-related request ("how do I", "what's the approach", "let's plan",
  "strategy")
- User asks to write code/features/components/refactor without prior discussion
- You're about to generate code without user alignment on strategy

## Plan Template

# Plan: [feature name]

## Approach

- Option A → tradeoff
- Option B → tradeoff
- Recommended: [option] because [reason]

## Unresolved

- [question 1]
- [question 2]

Keep under 20 lines. User scans, approves/adjusts, then you execute.
