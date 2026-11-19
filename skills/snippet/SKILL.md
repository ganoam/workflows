---
name: snippet
description: End-of-workday digest across all checked-out repos.
generated: true
allowed-tools:
  - read
  - grep
  - glob
---

Read `deps/workflows/recipes/snippet.md` — the repo's pinned
checkout — and follow it end to end; if that submodule is absent,
read `recipes/snippet.md` at the plugin root instead. Its prose
targets human readers; its content binds you. The binding rules in
`agents/rules.md` apply unconditionally and override anything in that
document.
