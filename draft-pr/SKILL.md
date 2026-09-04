---
name: draft-pr
description:
  Draft a ticket-linked squash PR after code-review. Use when you have a ticket link and a diff and
  need a conventional title plus body that survives squash, in one report and one refine loop.
disable-model-invocation: true
---

# Draft PR

Ticket-linked squash PR. One report holds the exhaustive walkthrough, one tight description survives
squash. The code is the source of truth; the title plus description answers what a reviewer needs
and decreases overload. A stranger with only `git log` understands the end, the approach, and the
risk.

## Process

Run these steps in order.

- **Analyze.** Read recent `git log` titles for the conventional commits style and whether scopes
  like `feat(scope):` are used, the ticket link and context for the Why, and the complete diff.
  Record the total `+N -M`, every file, and mark Why unknown when not grounded in ticket or context.
  Use only these three sources.
- **Report.** Produce one ticket-linked squash report, no gates. Open with the whole churn
  `+500 -120 | the whole PR`. Then cover the user-facing Why, then semantic chunks in order business
  reason, approach, then mechanics. Note which flows changed and what test evidence exists so the
  Flows and Test coverage sections stay grounded. This step is complete when every changed file
  belongs to a chunk and each chunk states its `+N -M | %`, files and lines, load-bearing lines, key
  decisions with alternatives and tradeoffs, risks, and judgment calls like naming, scope cuts,
  inferred details, placement, and deliberate omissions. Include deferred work and assumptions.
  Include Related verbatim when the ticket was given.
- **Propose.** Tighten the report into one ticket-linked squash title plus body. Keep detail in the
  report, not the draft. This step is complete when the draft is under 50 lines and each semantic
  chunk maps to one bullet. Small PRs omit Flows and stay under 15 lines. Show proposal together
  with the report.
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
stay shorter without padding. Markdown only, no HTML artifacts. Answer the reviewer's basic
questions in this order:

Keep sections compact, use bullets when a section has multiple distinct points:

- **Title.** One line, conventional commits `feat:`, `fix:`, etc. with optional scope `feat(scope):`
  when it clarifies the area, imperative and specific enough to stand alone in `git log` after
  squash. Include scope only when it makes sense.
- **Why.** One to three sentences. The user-facing problem, who or what it affects, and the intended
  outcome, grounded in ticket or context. No bullets here unless the Why truly has distinct points.
- **What changed.** One bullet per semantic chunk, in the user's words when available. Behavior
  introduced, scope or boundaries, and user-visible result.
- **Flows.** Include only when a reviewer needs the call order, data flow, or interaction to follow
  the change. Otherwise omit the section entirely. Pick the smallest markdown-only visual that makes
  the point, based on the diff content. Universal visuals render in GitHub and Azure DevOps web UI
  and stay readable as plain text in the squash commit body and email:
  - Logic or an algorithm as pseudocode in a plain fenced block.
  - Runtime control flow as an indented call tree.
  - UI structure as an indented component tree with only the state and boundaries that matter.
  - File responsibility or a refactor as a shallow file tree.
  - What changes and the surrounding shape already exists as a `diff` fenced block.
  - Rich visual, only when participant interaction or branching is hard to follow as text: component
    interaction, control flow, or data flow as Mermaid `sequenceDiagram` or `graph` in a fenced
    `mermaid` block. Use the standard fenced syntax, never the `::: mermaid` container, so the same
    block renders in GitHub and Azure DevOps Cloud pull requests. Stay inside the shared subset both
    render: `sequenceDiagram` or `graph` only (never `flowchart`), simple node labels, no HTML tags,
    no icons or Font Awesome, no LongArrow `---->`.
  - Place each visual next to the short text it supports. A Mermaid block always needs a
    one-sentence lead-in that still makes sense when the diagram does not render, such as in
    `git log` or email. Keep only the calls, files, props, states, and boundaries needed to answer
    the current change. Use one visual, two at most, never all of them. Prefer an ASCII tree when it
    fits and reserve Mermaid for interaction flows. Show the whole block when most of it is new; use
    `diff` shape when the point is what changed.
- **Test coverage.** What was tested and why it matters, grouped by risk or flow rather than by file
  list. Name the behavior or edge covered and why that check earns trust. Mention commands or suites
  only when a reviewer needs them to reproduce.
- **Risks and follow-ups.** Concrete risks, important assumptions, edge cases, rollout or
  compatibility concerns, work deliberately deferred.
- **Related.** Last section. One markdown link to the verbatim ticket, e.g.
  `[PROJ-123](https://tickets.example.com/PROJ-123)`, when the user provided one. Rendered as a
  clickable link. Omit the section entirely when no ticket was given.

Worked example:

**Title.** `feat(reports): keep the user's sort order across sessions`

**Why.**

Users lose their chosen sort order on every refresh because the in-memory state resets on reload.
This change preserves the preference locally so the report opens with the same view.

**What changed.**

- Sort order persisted to local storage.
- Restored on startup, before first render.

**Flows.**

Restore runs before the first paint so the UI never flashes the default order:

```
loadReport
  restoreSortOrder
    readLocalStorage
  renderTable
```

**Test coverage.**

- Restoring a saved order on reload, because that is the reported break.
- Default order when nothing is stored, because first-run must stay sane.

**Risks and follow-ups.**

- A future rename of the stored key needs a migration.
- Preferences remain device-local and will not follow users across browsers or devices.

**Related.** `[PROJ-123](https://tickets.example.com/PROJ-123)`

## Drafting style

- Every line earns its place. Cut anything that does not help a stranger review the PR or understand
  the squash commit later. The code is the source of truth; the description points at it, it does
  not retell it line by line.
- No restating the obvious, no section header with a single sentence, no bullet under a bullet.
- One visual at most in most PRs, two when flows truly diverge. No visual for typo, copy, or
  single-line fixes.
- Markdown only. Fenced code, call trees, file trees, `diff` blocks, and fenced `mermaid` blocks are
  allowed. No HTML artifacts. Never use the `::: mermaid` container syntax.
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
