---
name: git-privacy
description: Workflow for repos that are mostly public but carry private files (docs, notes, tooling state) that must never reach the public remote.
generated: true
---

Read `~/workspaceconfig/deps/workflows/recipes/git-privacy.md` and follow it end to end; if that checkout is absent, read `deps/workflows/recipes/git-privacy.md` in this repo, then `../workflows/recipes/git-privacy.md`; if none exists, warn the user and prompt them to clone the workflows repo.
A `recipes/git-privacy.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
