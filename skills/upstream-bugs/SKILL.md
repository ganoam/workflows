---
name: upstream-bugs
description: Workflow for when a build or sim failure might be a bug in the tool (compiler, simulator, linter) rather than in the project.
generated: true
allowed-tools:
  - read
  - grep
  - glob
---

Read `deps/workflows/recipes/upstream-bugs.md`, the repo's pinned checkout, and follow it end to end; if that submodule is absent, read `recipes/upstream-bugs.md` at the plugin root instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
