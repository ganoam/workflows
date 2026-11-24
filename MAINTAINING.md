# Maintaining and extending the workflows plugin

Agent-maintained; human reviewed.
Human-facing guide.
Binding rules for agents live in `agents/`; this file is about mechanics: how the pieces fit and what to do when you change them.

## Structure

```
workflows/
├── .devin-plugin/plugin.json   # plugin manifest (name: workflows)
├── hooks.json                  # plugin lifecycle hooks (table below)
├── hooks/                      # file-based hook scripts referenced
│                               #   from hooks.json (self-documenting)
├── AGENTS.md                   # plugin rule injected every session:
│                               #   rules.md > workflow.md > MdStyle.md > consumer AGENTS.md
├── agents/
│   ├── rules.md                # binding rules, tier 1, never loosened
│   ├── workflow.md             # binding operating workflow, tier 2
│   └── template.md             # consumer-repo AGENTS.md template
├── recipes/                    # shared procedures (human-readable, binding)
├── tricks/                     # terse command knowledge, human reference
├── skills/                     # SKILL.md wrappers, one per recipe,
│                               #   plus generate-skills (the generator)
├── README.md                   # what this repo is (directory map)
├── ROADMAP.md                # the buildout plan / status
├── DEVLOG.md                 # chronology
├── MAINTAINING.md            # this file
└── MdStyle.md                # prose style guide
```

The discovery layer (`skills/`) is thin generated wrappers over `recipes/`: the recipe file is always the single source of truth; the SKILL.md adds frontmatter (name, description trigger) and a pointer.

## Binding hierarchy (invariants)

1. `agents/rules.md` overrides everything: recipes, project docs, session instructions.
2. `agents/workflow.md` sits directly below `rules.md`.
   `MdStyle.md` sits at the same tier: `AGENTS.md` lists it as a binding document and `rules.md` delegates prose style to it.
3. Recipes and SKILL.md bodies may **restrict** rules further, never permit what a rule forbids.
   If a recipe needs an exception, that's a bug in the recipe, or an explicit human decision, not document authority.
4. Consumer-repo `AGENTS.md` and `recipes/` layer on top; they can restrict, never loosen `rules.md`.

## Common tasks

### Add a shared recipe

1. Write `recipes/<name>.md`: human prose, intro first sentence states when to apply it (it becomes the skill trigger).
2. Run `/workflows:generate-skills` in a consumer repo, or hand-write `skills/<name>/SKILL.md` matching the generated format.
3. Add the `recipes/README.md` index row.
4. Commit all three files in this repo; bump the plugin version in `plugin.json` if desired.

### Edit a recipe

Edit the recipe file only.
Re-run `generate-skills` to refresh the wrapper if the intro sentence changed: wrappers are marked `generated: true` and regenerated mechanically; never hand-edit them (hand-author a separate skill instead, it won't be clobbered).

### Edit the rules

`rules.md`/`workflow.md` changes take effect immediately in any session on a machine with the canonical `~/workspaceconfig/deps/workflows` checkout: the injected plugin AGENTS.md is only a pointer, and it instructs agents to re-read both files at the start of each task.
On machines resolving through the `deps/workflows` or `../workflows` fallbacks, changes apply once that checkout is updated.
Follow the hierarchy above: rules tighten, never silently loosen; recipe conflicts get fixed in the recipe.

### Add a project-local recipe

In the consumer repo: `recipes/<name>.md`, then run `/workflows:generate-skills`; it writes `.devin/skills/<name>/` in the consumer (untracked or private-committed, your choice).
A same-named local recipe shadows the shared one.

### Onboard a new repo

Follow `recipes/agent-setup.md`: submodule this repo to `deps/workflows`, write `AGENTS.md` from `agents/template.md` (repo-local section only), optionally install privacy hooks, run `generate-skills` if it has local recipes.

### Remove a recipe

Delete `recipes/<name>.md`; `generate-skills` prunes the generated wrapper.
Drop its `recipes/README.md` index row; commit the deletion of all three.

## Hooks

`hooks.json` at the plugin root registers lifecycle hooks wherever the plugin is installed.
It carries no scripting: one entry per (event, matcher) group resolves `hooks/run-event.py` through a candidate-path chain (canonical `~/workspaceconfig/deps/workflows` first, then consumer `deps/workflows/`, dep-checkout sibling `../workflows`, this repo) and hands it a dispatch key.
`run-event.py` holds the `DISPATCH` table mapping each key to its `hooks/*.py` scripts, feeds the event payload to each, and merges their outputs (first `decision` wins, `additionalContext` strings join).
Adding a hook is a self-documenting script under `hooks/` (style: `deps/scripts/bin/verify-format-diff.py`) plus one `DISPATCH` line — `hooks.json` stays untouched.
A case-table test under `hooks/tests/` goes with it (`test-<hook>.py`, same interface: JSON payload on stdin, verdict off stdout, exit 1 on mismatch).
The `id` in the table below is the script path; `run-event.py`'s table links it to its group.
Plugin hooks are best-effort and fail open: `agents/rules.md` remains the guarantee, hooks are the reminder or backstop.

| id | event | matcher | enforces | behavior |
|---|---|---|---|---|
| `hooks/git-state-guard.py` | `PreToolUse` | `^exec$` | `rules.md` repo-state and ref rules | Blocks state-changing `git` verbs, ref/index plumbing, and history/storage rewrites; read-only forms and `/tmp` commands pass. `config` and `symbolic-ref` argument tails are walked, so writes past the flag/refname prefix block while read forms pass. |
| `hooks/devlog-backlog-reminder.py` | `PostToolUse` | `^(edit\|write)$` | `rules.md` BACKLOG duty | On `DEVLOG.md` edits, injects a reminder to prune landed (committed) backlog items. |
| `hooks/devlog-readme-check.py` | `PostToolUse` | `^(edit\|write)$` | `AGENTS.md` README-accuracy duty | On `DEVLOG.md` edits, injects a conditional check: logged work that changed what README documents gets a same-task update proposal. A reminder, not a semantic verdict. |
| `hooks/devlog-roadmap-check.py` | `PostToolUse` | `^(edit\|write)$` | `AGENTS.md` ROADMAP-currency duty | On `DEVLOG.md` edits, injects a conditional check: logged work that landed a roadmap item gets checked off or re-statused in the same task. Silent where no ROADMAP exists (the duty itself is conditional). |
| `hooks/external-action-guard.py` | `PreToolUse` | `^exec$` | `rules.md` external-actions rules | Blocks mutating `gh` subcommands, non-GET `gh api`, and all `gh auth`; read verbs pass. `curl`/`mail`/`ssh` stay rule-only. |
| `hooks/destructive-cmd-guard.py` | `PreToolUse` | `^exec$` | `rules.md` destructive-ops and edit-approval rules | Blocks deletion primitives and commands that overwrite, append to, or in-place-modify existing files (stat-checked: `>`/`>>`, `tee`, `mv`/`cp` over files, `sed`/`perl -i`); creating new files and `/tmp` pass. Stricter than the rule: confirmed destructive ops are blocked too, the user runs them. Interpreter writes (`python -c`) and `rsync --delete`-style dir effects are not caught. |
| `hooks/write-overwrite-guard.py` | `PreToolUse` | `^write$` | `rules.md` edits-never-rewrites rule | Blocks `write` when the target file exists; the change goes through `edit` or the user applies the rewrite. |
| `hooks/edit-approval-reminder.py` | `PreToolUse` | `^(edit\|write)$` | `rules.md` edit-approval rule | Injects the approval rule on every edit/write call; a reminder, not a gate: approval status is conversation state the payload cannot carry, so no mechanical verdict exists. |
| `hooks/em-dash-reminder.py` | `PostToolUse` | `^(edit\|write)$` | `MdStyle.md` no-em-dashes | Counts unicode dashes in the applied edit/write text and injects the rule + allowed replacements; a reminder, not a gate (justified deviations permitted). |
| `hooks/session-start-reminder.py` | `SessionStart` | none | `workflow.md` session-start duties | Injects the session-start checklist: re-read binding docs, read repo `AGENTS.md`/`DEVLOG.md`, check `git status`/`git log` for unfamiliar work. Re-fires on resume/clear by design. The preamble-sync and skills-sync duties are deliberately not listed: `preamble-drift-check.py` and `skills-drift-check.py` perform those compares. |
| `hooks/preamble-drift-check.py` | `SessionStart` | none | `rules.md` preamble-sync duty | Performs the compare the duty asks for: repo `AGENTS.md` preamble vs the `<Canonical preamble:` block in `agents/template.md`, pointer paths masked; injects a drift verdict only when they differ. Files without the canonical opener are out of scope (exempts this repo's own plugin AGENTS.md). |
| `hooks/skills-drift-check.py` | `SessionStart` | none | skills-sync + `recipes/README.md` index duties | Compares `recipes/*.md` (minus `README.md`, the index) to generated wrappers (`.devin/skills/` in consumers, `skills/` in this repo); injects a proposal on missing, stale-description, or orphaned wrappers, and on uncovered or dead index rows where a `recipes/README.md` exists. Hand-authored wrappers skipped; silent where no `recipes/` exists. |
| `hooks/session-end-reminder.py` | `Stop` | none | `workflow.md` session-end duties | Injects a conditional session-end check: DEVLOG entry prepared alongside the work for a shared commit, AGENTS/README/ROADMAP currency, BACKLOG maintenance (`## In flight` staging plus pruning landed items). Never blocks (block-on-Stop can loop); fires on mid-session pauses too, so the check is phrased conditionally. |

## Gotchas

- Plugin install is per-machine (`devin plugins install --local <checkout>`), not recorded in consumer repos; the git-URL form is a snapshot and not recommended.
  Content canonicality lives with `~/workspaceconfig/deps/workflows`: the plugin ships discovery only, and repo-local `deps/workflows` checkouts are the fallback tier.
- Git-installed plugins snapshot at install time; `--local` links the checkout live, which is the only recommended mode.
- Git hooks (`deps/scripts` per consumer) are the real backstop for privacy rules: plugin `hooks.json` is documented fail-open; don't move the guardrail there yet.
