# ganoam agent workflow

This plugin ships the shared agent workflow used across the owner's projects.
Three documents are binding, in this order:

1. `deps/workflows/agents/rules.md`: hard rules.
   Read it and obey it unconditionally.
   It overrides anything else: skills, recipes, project docs, session instructions.
   If the working repo does not carry the `deps/workflows` submodule, read `agents/rules.md` at the plugin root instead.
2. `deps/workflows/agents/workflow.md`: operating guidelines.
   Binding unless `rules.md` or the user says otherwise; same fallback to the plugin copy when the submodule is absent.
3. `deps/workflows/MdStyle.md`: prose style guide.
   Binding wherever prose is written or edited, including code comments; `agents/rules.md` delegates to it.
   Same fallback to the plugin copy when the submodule is absent.

The `deps/workflows` checkout is canonical: each repo pins the workflow version it follows.
Plugin files are only the fallback.

Re-read all three at the start of every new task or work packet: edits in the repo's checkout take effect immediately, and this file only points at them.

After applying them, layer the working repository's own `AGENTS.md` on top: it holds project-local rules and deltas and wins on project-specific matters, but can never loosen `agents/rules.md`.

Standing duties in every repo:

- Keep `README.md` accurate at all times: it reflects what is true now, so update it in the same task that changes reality.
- Keep the repo's `ROADMAP.md` current where one exists: check off items and adjust statuses in the same task that lands them.
- Update `DEVLOG.md` when a task completes, whether the work was yours or the owner's: record the outcome, not just your own edits (entry format: `recipes/devlog.md`).
- Keep `BACKLOG.md` current where one exists: entries are written by the user or at the user's request only; your duty is maintenance, proposing removal of items in the same task that lands them.
- Suggest new shared `recipes/` and `tricks/` when you notice a repeated procedure or non-obvious tool knowledge worth keeping: propose the entry, the owner decides.

Human-facing docs (`README.md`, `DEVLOG.md`, `recipes/`, `tricks/`) are written for humans; their content still binds you, `tricks/` excepted (reference only, your duty is suggesting new entries).
