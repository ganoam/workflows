# ganoam agent workflow

This plugin ships the shared agent workflow used across the owner's projects.
Three documents are binding, in this order.
Resolve each path through the workflows checkout chain: `~/workspaceconfig/deps/workflows` first (the single canonical checkout for all agents on a machine), then `deps/workflows` in the working repo, then `../workflows` for dependency checkouts.
If none exists, warn the user and prompt them to clone the workflows repo; plugin files are transport, not a content source.

1. `agents/rules.md`: hard rules.
   Read it and obey it unconditionally.
   It overrides anything else: skills, recipes, project docs, session instructions.
2. `agents/workflow.md`: operating guidelines.
   Binding unless `rules.md` or the user says otherwise.
3. `MdStyle.md`: prose style guide.
   Binding wherever prose is written or edited, including code comments; `agents/rules.md` delegates to it.

Re-read all three at the start of every new task or work packet: edits in the canonical checkout take effect immediately, and this file only points at them.

After applying them, layer the working repository's own `AGENTS.md` on top: it holds project-local rules and deltas and wins on project-specific matters, but can never loosen `agents/rules.md`.

Standing duties in every repo:

- Keep `README.md` accurate at all times: it reflects what is true now, so update it in the same task that changes reality.
- Keep the repo's `ROADMAP.md` current where one exists: check off items and adjust statuses in the same task that lands them; superseded plans are struck through with the pivot recorded, never rewritten away (`recipes/roadmap.md`).
- Update `DEVLOG.md` when a task completes, whether the work was yours or the owner's: record the outcome, not just your own edits (entry format: `recipes/devlog.md`).
  Prepare the entry, and any README update the work calls for, alongside the work so they commit together.
- Keep `BACKLOG.md` current where one exists: entries are written by the user or at the user's request only; your duty is maintenance, moving started-but-uncommitted items into `## In flight` and proposing removal in the same task that lands them.
- Suggest new shared `recipes/` and `tricks/` when you notice a repeated procedure or non-obvious tool knowledge worth keeping: propose the entry, the owner decides.

Human-facing docs (`README.md`, `DEVLOG.md`, `recipes/`, `tricks/`) are written for humans; their content still binds you, `tricks/` excepted (reference only, your duty is suggesting new entries).
