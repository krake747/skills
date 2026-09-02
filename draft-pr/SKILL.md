---
name: draft-pr
description:
  Draft a ticket-linked squash PR after code-review. Use when you have a ticket link and a diff and
  need a conventional title plus body that survives squash, in one report and one refine loop.
disable-model-invocation: true
---

# Draft PR

Ticket-linked squash PR. One report holds the exhaustive walkthrough, one tight description survives
squash. A stranger with only `git log` understands the end, the approach, and the risk.

## Process

Run these steps in order.

- **Analyze.** Read recent `git log` titles for the conventional commits style and whether scopes
  like `feat(scope):` are used, the ticket link and context for the Why, and the complete diff.
  Record the total `+N -M`, every file, and mark Why unknown when not grounded in ticket or context.
  Use only these three sources.
- **Report.** Produce one ticket-linked squash report, no gates. Open with the whole churn
  `+500 -120 | the whole PR`. Then cover the user-facing Why, then semantic chunks in order business
  reason, approach, then mechanics. This step is complete when every changed file belongs to a chunk
  and each chunk states its `+N -M | %`, files and lines, load-bearing lines, key decisions with
  alternatives and tradeoffs, risks, and judgment calls like naming, scope cuts, inferred details,
  placement, and deliberate omissions. Include deferred work and assumptions. Include Related
  verbatim when the ticket was given.
- **Propose.** Tighten the report into one ticket-linked squash title plus body. Keep detail in the
  report, not the draft. This step is complete when the draft is under 50 lines and each semantic
  chunk maps to one bullet. Show proposal together with the report.
- **Refine once.** Use the question tool once to ask: approve as-is, edit in your own words, or give
  revision notes. Offer approve and revise choices and always leave room for your own words. Apply
  feedback, tighten, show updated title plus body. Loop only if you provide revisions.
- **Reconcile.** Re-read the final diff and check every line of the description against it. Drop
  anything no longer present, add anything the change does that no chunk covered. This step is
  complete when every claim is traceable to the final diff or to ticket or context.
- **Handoff.** If an existing PR is known ask whether to update it; if none exists ask whether to
  create one. Use the question tool for explicit confirmation before changing or creating anything.
  Report the actual result. If you decline, return the draft without an operation.

## PR description shape

Ticket-linked squash body. Report is unbounded, description is the reviewer summary and squash body.
Keep the description under 50 lines for all sizes. Every line earns its place. Small PRs naturally
stay shorter without padding.

Keep sections compact, use bullets when a section has multiple distinct points:

- **Title.** One line, conventional commits `feat:`, `fix:`, etc. with optional scope `feat(scope):`
  when it clarifies the area, imperative and specific enough to stand alone in `git log` after
  squash. Include scope only when it makes sense.
- **Related.** One markdown link to the verbatim ticket, e.g.
  `[PROJ-123](https://tickets.example.com/PROJ-123)`, when the user provided one. Rendered as a
  clickable link. Omit the section entirely when no ticket was given.
- **Why.** The user-facing problem, who or what it affects, the current limitation, and the intended
  outcome, grounded in ticket or context.
- **What changed.** One bullet per semantic chunk, in the user's words when available. Behavior
  introduced, scope or boundaries, and user-visible result.
- **Key decisions.** One bullet per distinct decision. Chosen approach, alternative considered, why
  it won, tradeoff or constraint accepted.
- **Risks and follow-ups.** Concrete risks, important assumptions, edge cases, rollout or
  compatibility concerns, work deliberately deferred.

Worked example:

**Title.** `feat(reports): keep the user's sort order across sessions`

**Related.** `[PROJ-123](https://tickets.example.com/PROJ-123)`

**Why.**

- Users lose their chosen sort order on every refresh.
- The current in-memory state resets on reload, so the behavior is surprising and repetitive.
- The change should preserve the preference without requiring an account or server-side setting.

**What changed.**

- Sort order persisted to local storage.
- Restored on startup, before first render.

**Key decisions.**

- **Storage:** Chose local storage over a server-side setting because it works for anonymous users,
  avoids a round trip, and requires no schema change.
- **Restore timing:** Restore before the first render so the UI does not briefly show the default
  order and then jump to the saved one.

**Risks and follow-ups.**

- A future rename of the stored key needs a migration.
- Preferences remain device-local and will not follow users across browsers or devices.

## Drafting style

- Every line earns its place. Cut anything that does not help a stranger review the PR or understand
  the squash commit later.
- No restating the obvious, no section header with a single sentence, no bullet under a bullet.
- Tighten after every change. The draft should never grow long just because the report did.

## Conventions

- Use only `git log` titles, the ticket link when given, and the diff as sources for shape and
  scope.
- Stay platform-agnostic except for the ticket link. Include Related as a markdown link `[KEY](url)`
  to the verbatim ticket when given; otherwise describe the problem in words and omit Related.
- Write the title plus body to stand alone after squash. `git log --oneline` plus the commit body
  tells the story without opening the PR.
- Flag a simpler change when the code allows one.
- Skip anything the user spelled out.
- Include any extra context the user gave in the request.
