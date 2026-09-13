---
name: deploy-gate
description: >-
  Deploy services safely. Use when the user asks to deploy.
---

# Deploy Gate

This is a contract. Break it and the work fails.

Run these steps in order.

1. **Freeze.** Announce the freeze. This step is complete when every channel shows the notice.
2. **Ship.** Push the release. This step is complete when the deploy log shows green.
3. **Verify.** Check the dashboards. This step is complete when all graphs look correct.
4. **Announce.** Use the question tool to ask whether to announce now or wait. Loop only if you
   provide revisions.
5. **Handoff.** Use the question tool to ask whether to hand off to on-call or keep watching. Create
   the handoff only on approval.

Never skip to Ship without a Freeze. If the user asks to deploy without one, refuse and say "Let's
freeze first."
