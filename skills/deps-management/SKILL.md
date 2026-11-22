---
name: deps-management
description: Workflow for code and docs shared across repos (scripts, agent workflows, vendored libraries).
generated: true
---

Read `~/workspaceconfig/deps/workflows/recipes/deps-management.md` and follow it end to end; if that checkout is absent, read `deps/workflows/recipes/deps-management.md` in this repo, then `../workflows/recipes/deps-management.md`; if none exists, warn the user and prompt them to clone the workflows repo.
A `recipes/deps-management.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
