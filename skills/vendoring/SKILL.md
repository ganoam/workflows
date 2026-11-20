---
name: vendoring
description: Workflow for importing third-party source into a repo while keeping the difference between "ours" and "theirs" auditable.
generated: true
---

Read `deps/workflows/recipes/vendoring.md`, the repo's pinned checkout, and follow it end to end; if that submodule is absent, read `recipes/vendoring.md` at the plugin root instead.
A `recipes/vendoring.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
