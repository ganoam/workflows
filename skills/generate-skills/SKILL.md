---
name: generate-skills
description: Regenerate SKILL.md wrappers for all recipes so they become agent-discoverable
allowed-tools:
  - read
  - grep
  - glob
  - write
  - edit
---

Generate one thin skill wrapper per recipe so every procedure becomes agent-discoverable.
The recipe file stays the single source of truth; the wrapper adds only the discovery layer.

## Inputs

- Shared recipes: `deps/workflows/recipes/*.md` in the consumer repo, or `recipes/*.md` when run inside the workflows repo itself.
- Project-local recipes: `recipes/*.md` in the working repo.
  A local recipe with the same basename wins over the shared one.

## Output

For each recipe `<name>.md`, write `SKILL.md`:

- shared recipe -> `deps/workflows/skills/<name>/SKILL.md` (or `skills/<name>/SKILL.md` inside the workflows repo)
- local recipe -> `.devin/skills/<name>/SKILL.md` in the working repo

Wrapper content: same frontmatter for both, different body:

```markdown
---
name: <name>
description: <first sentence of the recipe's intro paragraph>
generated: true
---
```

Emit `description` as a plain scalar when the sentence allows one; when it contains YAML specials (`: `, leading `#`, quotes, brackets), use a double-quoted scalar and escape `"` and `\`.

Body for a shared recipe:

```markdown
Read `deps/workflows/recipes/<name>.md`, the repo's pinned checkout, and follow it end to end; if that submodule is absent, read `recipes/<name>.md` at the plugin root instead.
A `recipes/<name>.md` at the working repo's root overrides it: if present, read and follow that file instead.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
```

Body for a project-local recipe:

```markdown
Read `recipes/<name>.md` at the repo root and follow it end to end.
Its prose targets human readers; its content binds you.
The binding rules in `agents/rules.md` apply unconditionally and override anything in that document.
```

## Rules

- Never overwrite a `SKILL.md` lacking `generated: true` in its frontmatter: hand-authored skills win.
  Report it as skipped.
- Remove a generated `SKILL.md` whose recipe file no longer exists.
- Refresh a generated `SKILL.md` when its recipe's intro sentence changed.
- Do not touch anything else.
  Report: created, updated, skipped, removed.
