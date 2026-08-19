---
name: scaffold
description:
  Match the codebase's existing patterns when writing new code. Use when adding something new that
  should fit existing structure, not when editing code that already exists.
---

# Scaffold

Make new code fit the codebase it lands in. Copy the patterns, never the implementation.

## Process

1. Find the reference. The closest existing code doing something like the new task. No sibling? Use
   the closest analog in a neighbouring directory. No analog at all? The convention is yours to set,
   and you flag it as a divergence.
2. Read how it is put together. Where the file lives, how it is named, how it opens and closes,
   imports, exports, types, error handling, tests. What repeats across siblings is convention. What
   changes is the task.
3. Write the new code on the same skeleton. Swap in the new subject, keep the moves.
4. Fill the gaps. Where no existing code covers a choice, take the closest consistent option.
5. Report divergence in one line. If you broke convention on purpose, say which and why.

## What to copy, what to leave

Copy the skeleton: where the file lives, how it is named, how it opens and closes, how it imports
and exports, how it handles errors.

Leave the implementation: the specific logic, data, and handlers. The reference is a template, not a
source to paste.

## Completion

Every convention you found is mirrored in the new code or named as a deliberate divergence. Nothing
in between. If you cannot point to the line in an existing file that a choice came from, the choice
is ungrounded. Fix it or drop it.
