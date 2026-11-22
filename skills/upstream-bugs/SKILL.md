---
name: upstream-bugs
description: Workflow for when a build or sim failure might be a bug in the tool (compiler, simulator, linter) rather than in the project.
generated: true
---

Read `~/workspaceconfig/deps/workflows/recipes/upstream-bugs.md` and follow it end to end; if that checkout is absent, read `deps/workflows/recipes/upstream-bugs.md` in this repo, then `../workflows/recipes/upstream-bugs.md`; if none exists, warn the user and prompt them to clone the workflows repo.
A `recipes/upstream-bugs.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
