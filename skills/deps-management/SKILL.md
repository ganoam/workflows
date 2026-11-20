---
name: deps-management
description: Workflow for code and docs shared across repos (scripts, agent workflows, vendored libraries).
generated: true
allowed-tools:
  - read
  - grep
  - glob
---

Read `deps/workflows/recipes/deps-management.md`, the repo's pinned checkout, and follow it end to end; if that submodule is absent, read `recipes/deps-management.md` at the plugin root instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
