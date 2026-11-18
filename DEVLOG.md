# Devlog

Chronology of work on this repository.

## Repo setup and agent docs consolidation (Nov 18)

- Repository created as the shared home for reusable workflow
  documentation, consumed as `deps/workflows` in consumer repos.
- `agents/rules.md`, `agents/workflow.md`, and `recipes/` distilled
  from a multi-week `hw-commons` session that mixed two kinds of
  work: OpenTitan-style UVM-on-Verilator bring-up and upstream bug
  triage, and design of the public/private git publishing workflow
  (`.gitprivate`, hooks, `publish.sh`).
- `agents/rules.md` reviewed and confirmed binding by the owner;
  it now carries the generic constraints (no repo-state changes,
  no external actions, discussion is not instruction, style and
  attribution rules).
- `agents/workflow.md` extended with operating sections: doc
  layering, deps/submodule propagation, generated regions,
  debugging methodology, workaround convention, upstream reports,
  review loop, session lifecycle, commit style. Owner-reviewed and
  in effect.
- `recipes/` seeded and owner-reviewed: `git-privacy.md` (moved from
  the scripts repo), `deps-management`, `upstream-bugs`,
  `vendoring`. `dv-library-extraction` and `uvm-on-verilator`
  relocated to `hw-commons/recipes/` as project-local recipes;
  `figure-pipeline` dropped.
- README attribution/import-history work in `hw-commons` informed
  `vendoring.md`: three import modes (filtered merge, submodule,
  plain copy) with the editing discipline scoped to copyright-level
  "Modifications by" marking on merged code.
- `tricks/` migration from `workspaceconfig` handled manually by
  the owner.
