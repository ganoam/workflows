# DEVLOG entry format

House format for `DEVLOG.md` chronology entries; apply when writing new entries or reworking old ones.
The file itself stays project-local.

## When to write

`agents/workflow.md` owns the duty: an entry per non-trivial work packet, including owner solo work discovered via `git log`.
A packet is written up alongside the work itself: the entry is prepared in the same working tree and committed with the change, while uncommitted in-progress work is staged in `BACKLOG.md`'s `## In flight` section.
This file only defines what an entry looks like.

## Format

- One section per session or coherent work period: `## <YYYY-MM-DD or range>: <short theme>`.
  Newest at the bottom.
- Terse bullets, one per work packet: what was done and the intent behind it, plus the outcome where it isn't obvious from the statement.
- Keep identifiers only where they carry meaning for a reader reconstructing events (a path, a branch name, a config key).
  Commit hashes, file lists, and command transcripts belong to `git log`, not here.
- `BACKLOG.md` is invisible to all other documents (`rules.md` BACKLOG bullet): the chronology describes the work and its outcome, never that the item was queued, and the same holds for every derived log (snippets, era digest).

## Attribution

A section may mix agent and owner work.
Mark owner solo work so it is not absorbed into session output: an `owner:` prefix on the bullet, or a short separate paragraph when several bullets are his.
Entries inferred by the end-of-day digest (`recipes/snippet.md`) rather than recorded by their author carry a `snippet:` prefix.

## Example

```
## 2026-11-19: agent workflow + git privacy setup

- Adopted the shared agent workflow (`deps/workflows` submodule): agent rules, recipes, and tricks get one pinned source shared across repos; the Devin plugin symlinks this checkout, so injected skills and pinned docs can't drift.
- Moved repo tricks into `deps/workflows/tricks/` (single shared home).
- Set up public/private publishing so private files never reach the public remote: `private` superset branch + private mirror, `.gitprivate` declares private paths, pre-commit/pre-push guards live in `deps/scripts/git-hooks` activated via `core.hooksPath`.
- Restructured `AGENTS.md` onto the shared template (pointer preamble, repo-specific deltas only).
```
