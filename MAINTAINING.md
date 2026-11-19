# Maintaining and extending the workflows plugin

Human-facing guide. Binding rules for agents live in `agents/`; this
file is about mechanics: how the pieces fit and what to do when you
change them.

## Structure

```
workflows/
├── .devin-plugin/plugin.json   # plugin manifest (name: workflows)
├── AGENTS.md                   # plugin rule injected every session:
│                               #   rules.md > workflow.md > consumer AGENTS.md
├── agents/
│   ├── rules.md                # binding rules, tier 1 — never loosened
│   ├── workflow.md             # binding operating workflow, tier 2
│   └── template.md             # consumer-repo AGENTS.md template
├── recipes/                    # shared procedures (human-readable, binding)
├── tricks/                     # terse command knowledge, human reference
├── skills/                     # SKILL.md wrappers — one per recipe,
│                               #   plus generate-skills (the generator)
├── README.md                   # what this repo is (directory map)
├── PLAN.md                   # the buildout plan / status
├── DEVLOG.md                 # chronology
└── MAINTAINING.md              # this file
```

The discovery layer (`skills/`) is thin generated wrappers over
`recipes/` — the recipe file is always the single source of truth; the
SKILL.md adds frontmatter (name, description trigger) and a pointer.

## Binding hierarchy (invariants)

1. `agents/rules.md` overrides everything: recipes, project docs,
   session instructions.
2. `agents/workflow.md` sits directly below `rules.md`.
3. Recipes and SKILL.md bodies may **restrict** rules further, never
   permit what a rule forbids. If a recipe needs an exception, that's a
   bug in the recipe — or an explicit human decision, not document
   authority.
4. Consumer-repo `AGENTS.md` and `recipes/` layer on top; they can
   restrict, never loosen `rules.md`.

## Common tasks

### Add a shared recipe

1. Write `recipes/<name>.md` — human prose, intro first sentence states
   when to apply it (it becomes the skill trigger).
2. Run `/workflows:generate-skills` in a consumer repo, or hand-write
   `skills/<name>/SKILL.md` matching the generated format.
3. Commit both files in this repo; bump the plugin version in
   `plugin.json` if desired.

### Edit a recipe

Edit the recipe file only. Re-run `generate-skills` to refresh the
wrapper if the intro sentence changed — wrappers are marked
`generated: true` and regenerated mechanically; never hand-edit them
(hand-author a separate skill instead, it won't be clobbered).

### Edit the rules

`rules.md`/`workflow.md` changes take effect immediately in any session
whose repo carries the `deps/workflows` checkout — the injected plugin
AGENTS.md is only a pointer, and it instructs agents to re-read both
files at the start of each task. In repos without the submodule,
changes apply on the next session once the plugin copy is updated
(`--local` installs are live-linked, so immediately there too).
Follow the hierarchy above: rules tighten, never silently loosen; recipe
conflicts get fixed in the recipe.

### Add a project-local recipe

In the consumer repo: `recipes/<name>.md`, then run
`/workflows:generate-skills` — it writes `.devin/skills/<name>/` in the
consumer (untracked or private-committed, your choice). A same-named
local recipe shadows the shared one.

### Onboard a new repo

Follow `recipes/agent-setup.md`: submodule this repo to `deps/workflows`,
write `AGENTS.md` from `agents/template.md` (repo-local section only),
optionally install privacy hooks, run `generate-skills` if it has local
recipes.

### Remove a recipe

Delete `recipes/<name>.md`; `generate-skills` prunes the generated
wrapper. Commit the deletion of both.

## Gotchas

- Plugin install is per-machine (`devin plugins install`), not recorded
  in consumer repos. The `deps/workflows` submodule is the canonical
  content anyway: each repo pins the workflow version it follows and
  plugin files are the fallback when the submodule is absent.
- Git-installed plugins snapshot at install time; `--local` links the
  checkout live. Use `--local` while iterating.
- Git hooks (`deps/scripts` per consumer) are the real backstop for
  privacy rules — plugin `hooks.json` is documented fail-open; don't
  move the guardrail there yet.
