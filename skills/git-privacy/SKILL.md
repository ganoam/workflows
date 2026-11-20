---
name: git-privacy
description: Workflow for repos that are mostly public but carry private files that must never reach the public remote.
generated: true
allowed-tools:
  - read
  - grep
  - glob
---

Read `deps/workflows/recipes/git-privacy.md`, the repo's pinned checkout, and follow it end to end; if that submodule is absent, read `recipes/git-privacy.md` at the plugin root instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
