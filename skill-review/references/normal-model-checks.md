# Normal-Model Checks

Second layer after the skill checks. Three sections below: control calibration, grounding and shape,
severity grading.

## Control calibration

Match specificity to fragility, per part, not per skill. Fail the body when any of these hold.

- A fragile operation without an exact sequence. Destructive or order-dependent work needs the
  literal commands, no added flags, plus a validation loop: do the work, run the validator, fix,
  repeat until green.
- A multi-step workflow with dependent steps and no checklist. Steps the model must not skip or
  reorder belong in an explicit progress checklist.
- A menu of equal options with no default. Name one default and its escape hatch; weaker models
  flounder choosing between peers.
- Flexible work with rigid directives and no why. Where multiple approaches are valid, explain the
  purpose so the model decides well in context.

## Grounding and shape

Skills earn their keep through project-specific knowledge. Fail the body when any of these hold.

- Generic advice where a gotcha belongs. Environment facts that defy reasonable assumptions stay
  inline in the root; the model cannot recognize a trigger for what it does not know.
- Declarations instead of procedures. Teach the approach that generalizes, with concrete output
  templates where the format must hold.
- An incoherent unit. Too narrow forces several skills to load for one task, risking overhead and
  conflicting instructions; too broad never triggers precisely.

## Severity grading under multi-model

Not every strict line is a violation. Grade recipe findings by audience.

- A strict gate with a judgment escape hatch (`unless trivial`, edge-case discretion, scoped to
  fragile work) is compliant. Flag only gates with no way out.
- A prescriptive fragile sequence with a validation loop is expected. Flag only itineraries on work
  that tolerates variation.
- A missing checklist, default, template, or gotcha is a finding at the same severity as a bloat
  finding. Under-specification fails weaker models the way over-specification fails stronger ones.
