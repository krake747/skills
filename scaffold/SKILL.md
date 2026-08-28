---
name: scaffold
description:
  Match the codebase's existing patterns when writing new code. Use when adding something new that
  should fit existing structure, not when editing code that already exists.
metadata:
  author: "Kevin Kraemer <kraemer.kevin747@gmail.com>"
---

# Scaffold

Make new code fit the codebase it lands in. Copy the patterns, never the implementation.

New code is judged against the code it sits next to. Matching the existing conventions keeps the
diff reviewable. Divergence is a statement: say it out loud and justify it.

## Process

1. Find the reference.

   ```ascii
   Closest existing code doing something like the task?
   ├── Yes → that is the reference
   └── No
       ├── Analog in a neighbouring directory? → closest one is the reference
       └── No analog at all? → the convention is yours to set; flag it as a divergence
   ```

2. Read how it is put together. Where the file lives, how it is named, how it opens and closes,
   imports, exports, types, error handling, tests. What repeats across siblings is convention. What
   changes is the task.
3. Write the new code on the same skeleton. Swap in the new subject, keep the moves. The reference
   is a template, not a source to paste.
4. Fill the gaps. Where no existing code covers a choice, take the closest consistent option.
5. Report divergence in one line. If you broke convention on purpose, say which and why.

## Completion

Every convention you found is mirrored in the new code or named as a deliberate divergence. Nothing
in between. If you cannot point to the line in an existing file that a choice came from, the choice
is ungrounded. Fix it or drop it.
