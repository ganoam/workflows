---
name: snippet
description: End-of-workday digest across all checked-out repos.
generated: true
---

Read `~/workspaceconfig/deps/workflows/recipes/snippet.md` and follow it end to end; if that checkout is absent, read `deps/workflows/recipes/snippet.md` in this repo, then `../workflows/recipes/snippet.md`; if none exists, warn the user and prompt them to clone the workflows repo.
A `recipes/snippet.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
