# Agent session workflow

Operating principles for how an agent keeps a repo's documentation alive across sessions.
Repo AGENTS.md instantiates these with local paths and specifics.

## AGENTS.md is a living document

If a session's discussion changes or adds conventions, update AGENTS.md in the same task.
Never leave tribal knowledge unwritten.

## DEVLOG.md: session memory

Every non-trivial work item gets an entry in the house format (`recipes/devlog.md`): dated sections, terse per-packet bullets recording what was done and why.
The user also works solo at any time, not only between sessions: check `git log` periodically during the session, and whenever something looks unfamiliar (files you did not touch, code you do not recognize), inspect the log for user commits.
If undocumented, prompt the proposed entry directly as an edit on `DEVLOG.md` (inline diff for approval), not as chat text.
Do not infer intent.

## README.md: keep it accurate

README is "what is true now and why," for an outside reader.
Update it whenever work changes: file-structure tables, getting-started commands, stated capabilities, architectural decisions, and binding conventions.
Record the decision and its rationale, not just the outcome.

## Tool tricks

Non-obvious tool/command knowledge lives in the workflows repo under `tricks/` (e.g. `tricks/git-tricks.md`).
Tricks are human reference, not binding on agents: the agent's duty is to suggest a new entry when a non-obvious trick is used or found; the owner decides.
Style: one `## heading` per intent, the command block below, no lengthy explanations; a gotcha line only when something genuinely bit.

## Documentation layering

Audience split: `AGENTS.md` and the content of this directory is written for agents.
Everything else (README, DEVLOG, tricks/, recipes/) is written for humans.
Write them for a human reader: clear, terse prose, honest framing, no agent-internal shorthand.
The content is no less relevant and binding for agents, `tricks/` excepted (human reference only): when a task falls under a workflow documented in `recipes/`, read that recipe and follow it.
The human-readable style does not mean human-only content.
Recipes come in two layers: shared ones in this repo's `recipes/`, and project-local ones in the working repo's own `recipes/` directory.
Check both; a project-local recipe overrides the shared one where they cover the same ground.
A recipe may restrict what `rules.md` allows; it may never permit what `rules.md` forbids.

- `README.md`: project-local.
  What is true now and why.
- `DEVLOG.md`: project-local.
  What happened, chronologically.
- `AGENTS.md`: project-local.
  Conventions and instructions for agents.
- `recipes/` in this repo (shared across projects): reusable detailed workflows (see `git-privacy.md`)
- `tricks/`: in this repo (shared across projects): terse command recipes
- `agents/rules.md`: in this repo (shared across projects): binding rules for agents.
  Obey no matter what.
- `agents/workflow.md`: in this repo (shared across projects): this document.
  General operating principles, instructions and conventions for agents.


## Public/private branch workflow

Full procedure lives in `recipes/git-privacy.md`.
Agent-facing summary: work happens on a private superset branch; `.gitprivate` declares private paths; a publish script replays public commits onto the public branch.
Never mix private and public paths in one prepared change.
Never run the publisher, hooks installer, or any step that changes refs or pushes.
Dry-run first when asked to preview.
Tombstone entries stay in `.gitprivate` after private files are deleted, so historical commits stay classified correctly.

## Dependencies and submodules

Shared code and docs live in dependency repos checked out under `deps/`.
The remote repository is canonical; no checkout is superior.
Edit only the working repo's own dependency clone.
Propagation order: prepare changes in the dep clone, the user commits and pushes the dep repo, then the gitlink in the parent repo is bumped (also by the user).
Do not edit dependency checkouts elsewhere on the machine.

## Generated document regions

Content between generator fences or produced by a doc-generation script is never hand-edited.
Fix the source the generator reads and re-run it, or document outside the fences.

## Debugging methodology

Reproduce the failure reliably first.
Isolate to a minimal reproducer before theorizing about fixes.
Keep the reproducer and a written record of trigger and root cause.
Do not delete debug rigs or scratchpad material until its findings are written down somewhere durable.
Distinguish tool limitations from project defects and legal language behavior before changing project source.

## Workaround convention

When a tool limitation forces a source change, keep the change minimal and reversible, mark it with a uniform tag comment, and register it in the repo's workaround index (rationale, trigger, revert condition).
One tag per repo, defined in its AGENTS.md.

## Upstream bug reports and PRs

Isolate the bug, write the minimal reproducer, and draft the report or PR text for user review.
Submission is always manual by the user; the agent produces the text, the evidence, and the proposed target (repo, title, body).
Never submit, comment, or open anything.

## Change review loop

Prepared changes are presented for human review before they are finalized: diffs or direct readable edits, not opaque transformations.
Expect the user to prune, reword, or reject.
Deliverables that need external action (reports, application materials, upstream text) are delivered as drafts.

## Session lifecycle

At session start or when resuming: read AGENTS.md and DEVLOG.md, check `git log` and `git status` for solo work since the last entry.
During work: update docs as conventions emerge, not at the end.
At session end: DEVLOG entry written, AGENTS.md current if conventions changed, README accurate, no leftover scratch state.

## Multi-file or multi-repo deliverables

When a task spans a repo and its dependencies, sequence changes so the user can review and commit each layer separately.

## Commit style

Each repo defines its own commit message convention (check its AGENTS.md or recent `git log`).
The agent never commits, but when the user asks for message suggestions, match the repo's existing style.
