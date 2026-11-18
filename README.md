# workflows

Shared working conventions, reusable procedures, and tool knowledge
for my projects. Consumed as a git submodule (conventionally at
`deps/workflows`) so every project reads and contributes to one copy.

## Layout

- `agents/` — documents written for AI agents: binding rules and
  operating workflow that apply across repos. A project's `AGENTS.md`
  points here and holds only repo-specific deltas.
- `recipes/` — reusable detailed workflows written for humans:
  how a class of task is done end to end (importing upstream code,
  handling tool bugs, managing shared dependencies, the public/private
  branch model). Project-local `recipes/` directories may layer on
  top and override.
- `tricks/` — terse command references: one heading per intent, a
  command block, a gotcha line only where something actually bit.

## Conventions

Audience and upkeep rules live in `agents/workflow.md`; binding
behavioral rules in `agents/rules.md`. Everything outside `agents/`
is written for human readers but its content binds agents too.
