# Skill Checks

What to flag in a SKILL.md, grouped by rule. Each check lists fail signals with the reasoning behind
them.

## Trigger precision

The description is one sentence of what plus one precise when, in imperative intent language. Fail
the description when any of these hold.

- A synonym stack or `Triggers on` list naming half the workflow
  (`implement, refactor, add, build, fix, change`). One vague trigger fires the skill everywhere and
  teaches the model nothing. Cover intent broadly, never through keyword stacks.
- The doctrine restated inside the description instead of the body. The description routes, the body
  teaches. Stay under the 1024-character limit.
- A dangling reference to a skill, command, or doc that does not exist in the repo.
- No when-not clause where a sibling skill overlaps. Without the boundary, both fire on every task
  and every similarity scan drifts upward.

## Progressive disclosure

Reading a skill burns context. The root is a router, detail lives behind pointers. Fail the layout
when any of these hold.

- A root over ~50 lines carrying content the model needs only sometimes. Move it to `references/`
  and point at it.
- A pointer with no trigger, such as a lone `See references/`. Write `read X when Y`, naming the
  condition that loads the file.
- Reference material the root never points at. Unpointed files are dead weight in every similarity
  scan.

## Recipes versus nuance

Match specificity to fragility. Fail the body when any of these hold.

- Ordered steps each gated by a completeness clause (`Run these steps in order`,
  `This step is complete when...`) on work that tolerates variation. State principles plus a
  completion standard instead.
- A hard gate that assumes the weakest model (`Never skip to Execute`,
  `This is a contract. Break it and the work fails`). Capable models take these literally and stall
  where judgment would do. Fragile sequences are the exception; see normal-model checks.
- Two approval stops where one suffices. Merge refine and handoff gates into a single decision.

## Boundaries and completion

Models stop early unless completion is defined, and over-read boundaries written for weaker models.
Fail the body when any of these hold.

- No definition of done. Done means implemented plus focused verification, artifacts removed, one
  simplification pass. A skill that ends at the first draft pulls the model toward an early stop.
- A stop-for-review default on work the user asked to be built. Plan-only stops belong to plan-only
  requests.
- Blanket bans with no positive target. Pair every guardrail with what to do instead.

## AGENTS.md hygiene

AGENTS.md loads on every task in the repo, so every line pays rent on every run. Fail it when any of
these hold.

- A blanket read before every edit (`read architecture.md before changing code`). Point at docs
  contextually instead: `Use architecture.md for service boundaries`.
- Blanket test or format runs on every task. Scope verification to behavior or script changes; the
  model already checks its own work.
- No persistence grant for safe local workflows. Name the disposable fixtures and permit run, fix,
  rerun without per-step approval, or the model will ask at each step.

## Pointer docs

Docs an agent reaches through a pointer (`architecture.md`, `database.md`, `deployment.md`) earn
their load cost only when fresh and linkable. Fail them when any of these hold. Flag staleness
markers, never domain truth the review cannot verify.

- Staleness markers: TODO notes, version stamps older than the repo's, or claims the request context
  contradicts.
- A copied fact instead of a link. One fact lives in one place; every other doc links to it.
- No reader-side trigger. The doc never states what it is for and when to read it, so the pointer
  line and the doc disagree about its job.
- Task-adjacent sections that ignore structure rules: noun headings, two actions in one line,
  pointers with no trigger, steps with no checkable done line.
