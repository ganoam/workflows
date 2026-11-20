# Managing shared dependencies as submodules

Workflow for code and docs shared across repos (scripts, agent workflows, vendored libraries).

## Model

- Shared material lives in its own repository, checked out as a submodule under `deps/<name>` in each consumer repo.
- The remote repository is canonical.
  No checkout is superior to another; a consumer's `deps/` clone and any other clone on the machine are equals.
- The parent repo pins the dependency by gitlink commit.
  Bumping the pin is a normal commit in the parent.

## Editing

- Edit only the working repo's own `deps/` clone.
  Never edit a dependency's checkout that lives inside a different consumer repo.

## Gotchas

- Sparse checkout state is per clone and not committed.
  Prefer a full submodule under `deps/` over sparse tricks.
- If a dep clone shows a dirty diff, reconcile by committing from the clone and pushing, or by checking out the canonical ref; do not leave parallel uncommitted copies in two checkouts.
