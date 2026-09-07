# GitHub PR mechanics

Check which integration is available first: an MCP integration for GitHub PR creation or editing
when one is configured, else the `gh` CLI. CLI flags verified against `gh` 2.100.0
(`gh pr create --help`, `gh pr edit --help`).

- Existence check: run `git branch --show-current` for the current branch, then
  `gh pr view <branch> --json number,title,url,isDraft,state` (or with no branch argument for the
  current branch), or plain `gh pr status` for an overview. A missing PR prints
  `no pull requests found for branch ...`, not a number to guess. Default base is the repo default
  branch unless the user named one.
- Create: `gh pr create --base <base> --head <branch> --title <title> --body <body>`. Long bodies go
  in a file with `--body-file`. Never `--fill`; the approved draft is the source of truth. For a
  draft PR add `--draft`; for a ready public PR omit it.
- Update: `gh pr edit <number> --title ... --body ...` (or `--body-file ...`). Without body flags
  the body is kept as is. This is the path when a PR already exists for the branch: set both title
  and body from the approved draft.
- Visibility: `gh pr ready <number>` promotes a draft to ready; `gh pr ready --undo <number>`
  converts back to draft when the plan supports it.
- Images and video for before/after tables: `--attach '<file>#<alt text>'` on create or edit. A
  `![alt](./file)` reference already in the body is rewritten to point at the uploaded asset. Up to
  50 files per command. Video renders as a player and takes no alt text.
- Rendering: fenced `mermaid` blocks render in PR bodies. Stay inside `sequenceDiagram` or `graph`
  only (never `flowchart`), simple node labels, no HTML tags, no icons, no LongArrow `---->`. Never
  the `::: mermaid` container syntax.
- Every diagram needs a one-sentence lead-in that still reads when the diagram does not render, such
  as in `git log` or email.
- Markdown only, no HTML artifacts.
- The PR title plus body becomes the squash commit message; the Related ticket link goes last so it
  survives. Reference issues with `Fixes #123` or `Closes #123` in the body only when the user asked
  for auto-close.
