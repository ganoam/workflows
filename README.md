# workflows

Shared working conventions, reusable procedures, and tool knowledge
for my projects. Doubles as a Devin plugin (`skills/` +
`.devin-plugin/`): the plugin provides discovery (skill list,
injected root `AGENTS.md`), while each project's `deps/workflows`
checkout is the canonical content — projects pin the workflow
version they follow.

## Layout

- `.devin-plugin/` — plugin manifest.
- `AGENTS.md` — plugin-root rule file injected into every session;
  points at the binding docs and states precedence and standing
  duties.
- `agents/` — documents written for AI agents: binding rules and
  operating workflow that apply across repos, plus `template.md`,
  the consumer-repo `AGENTS.md` template. A project's `AGENTS.md`
  points here and holds only repo-specific deltas.
- `recipes/` — reusable detailed workflows written for humans:
  how a class of task is done end to end (importing upstream code,
  handling tool bugs, managing shared dependencies, the public/private
  branch model, repo onboarding, DEVLOG entry format). Project-local
  `recipes/` directories may layer on top and override.
- `skills/` — one generated `SKILL.md` wrapper per recipe so agents
  discover them mechanically, plus the `generate-skills` generator.
  Thin pointers; the recipe file is the source of truth.
- `tricks/` — terse command references: one heading per intent, a
  command block, a gotcha line only where something actually bit.
- `ROADMAP.md` — the buildout plan and status.
- `MAINTAINING.md` — how to maintain and extend the plugin.
- `MdStyle.md`: prose style guide, binding via the `rules.md`
  pointer; rationale and detail for the doc-related style rules.

## Conventions

Audience and upkeep rules live in `agents/workflow.md`; binding
behavioral rules in `agents/rules.md`. Everything outside `agents/`
is written for human readers but its content binds agents too.
