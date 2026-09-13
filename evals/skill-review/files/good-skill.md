---
name: log-trimmer
description: >-
  Trim noisy logs before reading them. Use when logs bury the error. Not for changing log output;
  use the logger config for that.
---

# Log Trimmer

Cut noise until the error reads plainly. Keep every line that changes the diagnosis.

## Pointers

- Filters: read `references/filters.md` when a log format needs its own pattern.
- Sampling: read `references/sampling.md` when the log is too large to read whole.

## Completion standard

Finish with the error and its surrounding lines quoted, the filter saved beside the log, and nothing
else changed.
