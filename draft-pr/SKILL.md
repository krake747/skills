---
name: draft-pr
description: >-
  Draft a good PR description by walking the user through the diff in bounded semantically ordered
  chunks, approved one at a time. Each approved chunk feeds the draft, so the user writes the
  description by approving the review. Use after a big change, when a PR needs a description that
  names the problem, the approach, and the risk. Complements code-review.
disable-model-invocation: true
---

# Draft PR

The deliverable is the PR description. The chunked walkthrough is how the agent gathers the
material. The user approves each chunk, and its facts and decisions are appended to a running draft
shown in chat. The user writes the description by approving the review.

An alphabetical diff produces a raw description. Approval forces understanding before a line earns
its place.

## Process

Run these steps in order. Do not move to the next chunk until the current chunk has a clear approval
or revision from the user.

- **Prepare the review.** Read the PR template, CONTRIBUTING or other PR guidance, recent commit
  titles, the user's context, and the complete diff. Identify the platform only from that evidence.
  Record the total added and deleted lines and the files that need coverage. This step is complete
  when the title convention, description shape, platform if known, and full diff are accounted for.
- **Start with the why.** Explain what the change is for and the user-facing problem it solves
  before any code. If the context does not establish a why, say that it is unknown and ask the user
  rather than inventing one. This becomes the Why section. This step is complete when the problem
  and intended outcome are either grounded in user context or explicitly marked unknown.
- **Show the total first.** Open with the whole churn, e.g. `+500 -120 | the whole PR`, so the user
  sees the scale before committing.
- **Chunk semantically.** Break the diff into units that build shared understanding, a few files at
  most. Each chunk opens with its own stats, e.g. `+50 -15 | 5% of the PR`. Order chunks as business
  reason, baseline and options, chosen approach, then mechanics, not file-tree order.
- **Walk one chunk.** Explain the chunk, use a tiny visual when it clarifies the flow, and call out
  load-bearing lines, key decisions, tradeoffs, risks, and any judgment calls you made. State which
  files and changed lines this chunk covers. It is complete only when every covered line has an
  evidence-based explanation and the user has approved it or supplied a revision.
- **Append after approval.** Add only the approved facts and decisions to the running PR
  description, tighten it to the repo's shape and line limit, and show the updated draft. Then
  continue until every changed line belongs to a chunk. Judgment calls include naming, scope cuts,
  inferred details, placement, and deliberate omissions; surface each one for veto rather than
  presenting it as fact.
- **Approve conversationally with the question tool.** After each chunk, ask one open question:
  approve as-is or revise. Offer approve/revise choices but always leave room for the user's own
  words; never let fixed options narrow what they can say. Pause for the answer.
- **Reconcile at the end.** Re-read the final diff and check every line of the description against
  it. The reviewed code is the source of truth: drop anything the walkthrough approved that the
  final change no longer contains, and add anything the change does that no chunk covered. This step
  is complete when every changed line is covered and every claim in the draft is traceable to the
  final diff or to user-provided context.
- **Offer the final handoff.** Show the proposed title and description together. If an existing PR
  is known, ask whether to update it; if no PR exists, ask whether to create one. Use the question
  tool for explicit confirmation before changing or creating anything. Identify the platform from
  the repository or user context rather than assuming one, and report the actual result after the
  operation. If the user declines, return the draft without making the operation.

## PR description shape

The whole draft stays under 15 lines. A reviewer should read it in under a minute. Keep the
walkthrough's detail in the chat, not in the draft.

Each approved chunk fills one or more sections. Keep the sections compact, but use bullets when a
section contains multiple distinct points:

- **Title.** One line naming the change. Use the repo's title convention (conventional commits
  `feat:`, `fix:`, ... when that is what it uses).
- **Why.** Use a few bullets when useful: the user-facing problem, who or what it affects, the
  current limitation, and the intended outcome.
- **What changed.** Use one bullet per approved chunk, in the user's words. Describe the behavior
  introduced, the relevant scope or boundaries, and the user-visible result when those details
  matter.
- **Key decisions.** Use bullets for distinct decisions. For each one, name the chosen approach, the
  alternatives considered, why it won, and the tradeoff or constraint it accepts.
- **Risks and follow-ups.** Use bullets for concrete risks, important assumptions, edge cases,
  rollout or compatibility concerns, and work deliberately deferred from this change.

Worked example:

**Title.** `feat: keep the user's sort order across sessions`.

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

- Every line earns its place. Cut anything that does not help a stranger review the PR.
- No restating the obvious, no section header with a single sentence, no bullet under a bullet.
- Tighten after every append. The draft should never grow long just because the walkthrough did.

## Conventions

- **Read the repo's PR conventions first.** Before drafting, look for a PR template, a CONTRIBUTING
  file, docs on commit or PR style, and recent titles in `git log`. Adopt whatever shape, title
  format, and section names the repo already uses; fall back to the default shape here only when the
  repo has none.
- **Stay platform-agnostic.** Do not assume GitHub, Azure DevOps, GitLab, Jira, or any tracker.
  Never invent issue numbers, work item IDs, or links. If the user gives one, include it verbatim;
  otherwise describe the problem in words.
- The description must read so a stranger with a PR link understands the end, the approach, and the
  risk. Code is a means to an end; the description names the end.
- Correctness and readability beat speed. Flag a simpler change when the code allows one.
- Skip anything the user spelled out.
- Include any extra context the user gave in the request.
