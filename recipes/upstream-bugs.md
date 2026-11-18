# Handling upstream tool bugs

Workflow for when a build or sim failure might be a bug in the tool
(compiler, simulator, linter) rather than in the project.

## Triage first

- Reproduce the failure reliably.
- Decide which side is wrong: legal input the tool rejects or
  mishandles, versus a genuine project defect. Read the language
  spec or tool docs before assuming.

## Minimal reproducer

- Cut the failing code down to the smallest input that still
  triggers the failure. Remove the framework, the build system,
  everything incidental.
- Write control experiments alongside it: the near-identical input
  that works, and variants that isolate which feature is the
  trigger (e.g. parameter vs member, subclass vs typedef).
- Keep reproducer and controls in a durable location (`vlt-debug/`
  or equivalent) with a README stating trigger, expected vs actual
  behavior, and tool version.

## Workaround while waiting

- Keep project-source changes minimal and reversible.
- Tag each workaround with a uniform marker (e.g. `VLT-WORKAROUND:
  <id>`) so all of them are greppable.
- Register every workaround in an index file: id, location, what it
  replaces, why, and the revert condition (tool fix released).
- Prefer workarounds that do not change public interfaces; if they
  must, document the semantic cost.

## Reporting

- Draft the report text: minimal reproducer, actual vs expected,
  version, and the control results. Deliver as a draft for human
  review.
- Submission is manual. Never file, comment, or open a PR against
  the tool repo autonomously.
