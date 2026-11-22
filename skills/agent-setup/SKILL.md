---
name: agent-setup
description: "Set up the shared agent workflow in a repo: AGENTS.md, an optional fallback checkout, hooks, local skills, plus the one-time machine plugin install."
generated: true
---

Read `~/workspaceconfig/deps/workflows/recipes/agent-setup.md` and follow it end to end; if that checkout is absent, read `deps/workflows/recipes/agent-setup.md` in this repo, then `../workflows/recipes/agent-setup.md`; if none exists, warn the user and prompt them to clone the workflows repo.
A `recipes/agent-setup.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
