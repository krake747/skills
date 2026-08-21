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

- **Start with the why.** Explain what the change is for and the user-facing problem it solves
  before any code. The user may have pasted a PR link with no context. This becomes the Why section.
- **Show the total first.** Open with the whole churn, e.g. `+500 -120 | the whole PR`, so the user
  sees the scale before committing.
- **Chunk semantically.** Break the diff into units that build shared understanding, a few files at
  most. Each chunk opens with its own stats, e.g. `+50 -15 | 5% of the PR`.
- **Order chunks to build understanding.** Business reason first, then baseline and the options
  considered and the chosen one, then the mechanics. Not file-tree order.
- **Use tiny visuals.** An ascii tree, a call-site sketch, a stack trace. A wall of text overloads.
- **Call out load-bearing lines.** Flag the key decisions and the lines that carry real weight in
  each chunk. These become the Key decisions and Risks sections.
- **Append to the draft after each approval.** Add that chunk's approved facts to the running PR
  description and show it, so the user corrects early instead of at the end.
- **Flag judgment calls.** List every decision you made on your own: naming, scope cuts, invented
  details, where things went, what you left out on purpose. These feed Key decisions and Risks, or
  get flagged for the user to veto before merge.
- **Approve conversationally with the question tool.** After each chunk, ask one open question:
  approve as-is or revise. Offer approve/revise choices but always leave room for the user's own
  words; never let fixed options narrow what they can say.
- **Reconcile at the end.** Before handing over the draft, re-read the final diff and check every
  line of the description against it. The reviewed code is the source of truth: drop anything the
  walkthrough approved that the final change no longer contains, and add anything the change does
  that no chunk covered.

## PR description shape

The whole draft stays under 15 lines. A reviewer should read it in under a minute. Keep the
walkthrough's detail in the chat, not in the draft.

Each approved chunk fills one or more sections:

- **Title.** One line naming the change. Use the repo's title convention (conventional commits
  `feat:`, `fix:`, ... when that is what it uses).
- **Why.** The user-facing problem the change solves.
- **What changed.** One bullet per approved chunk, in the user's words.
- **Key decisions.** Options considered, the chosen one, and why.
- **Verification.** Only checks actually run and observed during the review (see Verified vs
  follow-ups).
- **Risks and follow-ups.** Load-bearing lines, tradeoffs a reviewer should watch, and anything not
  verified.

Worked example:

**Title.** `feat: keep the user's sort order across sessions`.

**Why.** Users lose their chosen sort order on every refresh. The current in-memory state resets on
reload.

**What changed.**

- Sort order persisted to local storage.
- Restored on startup, before first render.

**Key decisions.** Chose local storage over a server-side setting: works for anonymous users, no
round trip, no schema change.

**Verification.** Unit test for the save and restore round trip; manual check that refresh keeps the
order.

**Risks and follow-ups.** A future rename of the stored key needs a migration; not covered here.

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

## Verified vs follow-ups

Keep these two apart. Verification lists only what was actually run or observed during the
walkthrough: commands executed, tests that passed, output seen. Follow-ups list what was _not_ done:
untested paths, known gaps, ideas deferred. Never promote an unverified claim into Verification to
make the PR look stronger; if it was not run, it is a follow-up.
