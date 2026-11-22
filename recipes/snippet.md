# Daily snippet: cross-repo work digest

End-of-workday digest across all checked-out repos.
Scan every `DEVLOG.md` for entries dated today, consolidate them into terse per-repo bullets, and append one dated section to `~/code/notes/snippets.md`.
The same scan maintains `~/code/notes/era-digest.md`, the coarse record of substantial work starting and completing across projects, and keeps `~/code/notes/backlog.md` synced, a terse overall list of open per-project backlog items.
Entry style follows `devlog.md`; this recipe only defines the scan, grouping, and output.

## Inputs

- Scan roots: `~/code` (one level deep) plus `~/workspaceconfig`, which lives outside the `~/code` tree.
  Each checkout is `~/code/<repo>`; dependency checkouts sit at `~/code/<repo>/deps/<dep>` (and `~/workspaceconfig/deps/<dep>`).
  The roots and the output path are the owner's layout; adapt per machine.
- Sources: `DEVLOG.md` at each repo root and at each `deps/<dep>` root that has one; `BACKLOG.md` at each root that has one, for the overall backlog sync.
- State check: `git status --porcelain` (plus `git diff --stat` where detail helps) per repo, for uncommitted work the logs cannot see.
- Outputs: `~/code/notes/snippets.md` for the daily digest, `~/code/notes/era-digest.md` for the era digest, `~/code/notes/backlog.md` for the overall backlog.

## Procedure

1. Glob `~/code/*/DEVLOG.md`, `~/code/*/deps/*/DEVLOG.md`, `~/workspaceconfig/DEVLOG.md`, and `~/workspaceconfig/deps/*/DEVLOG.md`.
2. Collect sections whose heading carries today's date.
   Repos and deps with no same-day section are skipped entirely.
3. Write one dated section grouped per repo: a `### <repo>` heading, then the day's bullets trimmed to intent and outcome.
   A dependency's entries get their own `### <dep>` heading (`### <repo>/deps/<dep>` when the name alone is ambiguous).
4. Append the section at the bottom of `snippets.md`, newest at the bottom like DEVLOG.
   If today's section already exists, merge new bullets into it instead of duplicating.
5. Every repo in the scan gets its working state checked: a dirty `git status` adds an `uncommitted:` bullet under its `### <repo>` section, summarizing change classes (staged, modified, untracked) with counts and top-level paths, never a full file list.
   A repo skipped by the no-same-day rule but showing uncommitted changes still gets flagged, one trailing line naming it, so uncommitted-only work is not invisible.
   Uncommitted state feeds no DEVLOG fills: there are no commits to interpret.
6. Every repo's `BACKLOG.md` is read and its open items mirrored into `~/code/notes/backlog.md`: `## <repo>` sections where a project has several items, flat `- <repo>: <summary>` lines for single-item projects.
   Before writing the items, give each project a `last:` line summarizing its most recent work.
   Order tracked files by mtime (`git ls-files` + `stat`, or `find` on the worktree), take the recently-touched cluster, and infer the work from the paths.
   The DEVLOG may corroborate but is not the source.
   The file is regenerated wholesale on each run: per-project backlogs are the source of truth, so landed items disappear automatically and no manual pruning is needed.
   Deps get the same `<dep>` or `<repo>/deps/<dep>` naming as digest sections.
7. Every `DEVLOG gap` found during the scan feeds back to the source repo: draft a DEVLOG entry from the uncovered commits and propose it to the user.
   Proposed bullets carry a `snippet:` prefix marking them as end-of-day digest inferences, parallel to `owner:`.
   Entries land only with user approval; the digest never edits a DEVLOG silently.
   A dated section that already exists takes the new bullets directly; a new section is created only when none covers the work's date, its heading inferred from the devlog's own convention (usually a one-line summary of the work).
   The heading itself carries no snippet mark; the `snippet:` prefixes on the bullets do that.

## Style

- `devlog.md` conventions apply: terse bullets, intent plus outcome, identifiers only where they carry meaning, no hashes or file lists.
- Compress rather than copy: a reader skims the day, they do not re-read each log.
- Each dated section opens with a one-liner summarizing all of the day's work across repos.
- `owner:` marks in source entries are preserved as-is.
- A repo's same-day `git log` is always checked against its DEVLOG coverage.
  Commits with no coverage, whether the day's section is missing entirely or just incomplete, get a `DEVLOG gap` marker followed by bullets summarizing what the log shows; intent is not invented.
- Dates follow the work, not the run: DEVLOG-sourced bullets keep their section's date, gap-summary bullets take the commit's author date, and "same-day" for the log check is judged on that author date.
  Material belonging to another day is prefixed with its real date rather than silently absorbed into today's section.
- `BACKLOG.md` is invisible to all other documents (`rules.md` BACKLOG bullet): never record that work was a queued backlog item, in `snippets.md`, `era-digest.md`, or the `snippet:` fills.
  The overall `notes/backlog.md` is the stated exception: it exists to track open items, so mirroring them there is the point, not provenance in a chronology.
- `uncommitted:` bullets describe working state at scan time and carry no date prefix.

## Overall backlog

`~/code/notes/backlog.md` is the cross-repo view of deferred work: every open item from every per-project `BACKLOG.md`, one line each as `- <repo>: <one-line summary>`.
Each project carries a `last:` line before its items, a short summary of what was worked on most recently, inferred from file timestamps rather than the DEVLOG (which may lag or omit the work), so the file reads as state plus queue.
It is a mirror, not a document of its own: per-project backlogs are the source of truth, so the file is regenerated wholesale on each digest run rather than maintained by hand.
Items are grouped under `## <repo>` headings where several belong to one project; single-item projects can keep a flat list.
There is no dating and no chronology: the file always shows what is open now, nothing else.

## Era digest

`era-digest.md` is the longer horizon: substantial work starting or completing across projects, kept deliberately coarser than the daily bullets.
The same scan maintains it: whenever the day's material, gap fills included, shows a substantial work stream starting or completing in any project, propose an entry for approval.
One line per event carrying the work's real date; new projects, major features or phases, and large landings qualify, routine upkeep does not.
Entries group under an era heading when a period has a recognizable theme; otherwise they keep a plain dated chronology, newest at the bottom.
Era headings are never duplicated: a new entry merges into an existing era when its theme already has one.
