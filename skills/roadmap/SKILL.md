---
name: roadmap
description: Suggested structure for a repo's ROADMAP.md, distilled from the hw-commons and workflows roadmaps.
generated: true
---

Read `~/workspaceconfig/deps/workflows/recipes/roadmap.md` and follow it end to end; if that checkout is absent, read `deps/workflows/recipes/roadmap.md` in this repo, then `../workflows/recipes/roadmap.md`; if none exists, warn the user and prompt them to clone the workflows repo.
A `recipes/roadmap.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
