# Azure DevOps PR mechanics

Check which integration is available first: an MCP integration for Azure Repos PR creation or
editing when one is configured, else the `az` CLI. The `az` CLI is not installed in this
environment, so every CLI claim below is unverified: confirm against `az repos pr create --help` and
`az repos pr update --help` before running anything.

- Existence check (unverified): run `git branch --show-current` for the current branch, then list
  PRs for it (check `az repos pr list --help` for a source branch filter) before assuming a number.
  A missing PR is an empty result, not a reason to guess an id. Default target is the repo default
  branch unless the user named one.
- Create (unverified):
  `az repos pr create --source-branch <branch> --target-branch <base> --title <title> --description <body>`,
  plus `--organization` and `--project` when outside the default context. For long bodies, check
  whether the installed version accepts a file input; otherwise pass the text inline. Confirm
  whether the installed version supports a draft flag (check `az repos pr create --help` for
  `--draft`) and use it for a draft PR, omit it for a ready public PR.
- Update (unverified): `az repos pr update --id <id> --title ... --description ...`. This is the
  path when a PR already exists for the branch: set both title and description from the approved
  draft.
- Rendering (unverified): Azure DevOps PR markdown is CommonMark-based with narrower Mermaid support
  than GitHub. Prefer ASCII call trees and `diff` blocks; use a fenced `mermaid` block only after
  confirming it renders in the target project, and stay inside `sequenceDiagram` or `graph` only.
  Never the `::: mermaid` container syntax.
- Every diagram needs a one-sentence lead-in that still reads when the diagram does not render, such
  as in `git log` or email.
- Images for before/after tables (unverified): CLI attachment upload is awkward here; prefer the web
  UI drag-and-drop, then reference the resulting URLs in the description.
- Markdown only, no HTML artifacts.
- Complete with the squash merge strategy and keep the description as the merge commit message; the
  Related ticket link goes last so it survives.
