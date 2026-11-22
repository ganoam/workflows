---
name: devlog
description: House format for `DEVLOG.md` chronology entries; apply when writing new entries or reworking old ones.
generated: true
---

Read `~/workspaceconfig/deps/workflows/recipes/devlog.md` and follow it end to end; if that checkout is absent, read `deps/workflows/recipes/devlog.md` in this repo, then `../workflows/recipes/devlog.md`; if none exists, warn the user and prompt them to clone the workflows repo.
A `recipes/devlog.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
