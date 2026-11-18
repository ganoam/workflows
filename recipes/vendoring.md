# Vendoring upstream code

Workflow for importing third-party source into a repo while keeping
the difference between "ours" and "theirs" auditable.

## Model

- Vendored code keeps its upstream layout, license headers, and
  provenance. Record source repo, commit/version, and import date
  in a manifest or the importing commit message.
- Three import modes, picked per dependency:

| Mode | Mechanism | Use when |
|---|---|---|
| History-preserving filtered merge | `git filter-repo` on an upstream clone, then `git merge --allow-unrelated-histories` | The code is a basis for your own work: you patch it, extend it, maintain local diffs, and it becomes part of your project. Upstream history stays in the DAG for provenance. |
| Submodule | `git submodule add` under `deps/` | A standalone project your work uses: shared libraries, tooling, workflows. It stays its own project. If you own it, modify it in place and push; if not, contribute upstream rather than carrying local diffs. |
| Plain copy | `cp` the files in | Small adopted assets you intend to own outright: a standalone script, a template, a config. No upstream tracking, no intent to merge updates. Attribution and licensing as appropriate. |

- Whichever mode: write down which was chosen and why. Local edits
  on merged or copied code must be greppable (tag + registry, see
  `upstream-bugs.md`); submodule changes happen inside the
  submodule's own history.

## Editing discipline

- Touch vendored files as little as possible. Every local edit is
  a re-import cost and an upstream-diff audit item.
- Local edits must be tagged and indexed the same way as tool
  workarounds (see `upstream-bugs.md`): marker comment plus registry
  entry with rationale and revert condition.
- Keep adaptation layers outside the vendored tree when possible:
  wrapper files, thin subclasses, and build glue in the consumer's
  own directories.

## Attribution

- Maintain an attribution table (path -> upstream project, version,
  license) in project docs. Add rows when vendoring; update on
  re-import.
- Do not strip copyright or license headers. Do not re-license.
