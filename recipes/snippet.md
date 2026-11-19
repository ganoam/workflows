# Daily snippet: cross-repo work digest

End-of-workday digest across all checked-out repos.
Scan every `DEVLOG.md` for entries dated today, consolidate them
into terse per-repo bullets, and append one dated section to
`~/code/notes/snippets.md`.
Entry style follows `devlog.md`; this recipe only defines the scan,
grouping, and output.

## Inputs

- Scan roots: `~/code` (one level deep) plus `~/workspaceconfig`,
  which lives outside the `~/code` tree.
  Each checkout is `~/code/<repo>`; dependency checkouts sit at
  `~/code/<repo>/deps/<dep>` (and `~/workspaceconfig/deps/<dep>`).
  The roots and the output path are the owner's layout; adapt per
  machine.
- Sources: `DEVLOG.md` at each repo root and at each `deps/<dep>`
  root that has one.
- Output: `~/code/notes/snippets.md`.

## Procedure

1. Glob `~/code/*/DEVLOG.md`, `~/code/*/deps/*/DEVLOG.md`,
   `~/workspaceconfig/DEVLOG.md`, and
   `~/workspaceconfig/deps/*/DEVLOG.md`.
2. Collect sections whose heading carries today's date.
   Repos and deps with no same-day section are skipped entirely.
3. Write one dated section grouped per repo: a `### <repo>` heading,
   then the day's bullets trimmed to intent and outcome.
   A dependency's entries get their own `### <dep>` heading
   (`### <repo>/deps/<dep>` when the name alone is ambiguous).
4. Append the section at the bottom of `snippets.md`, newest at the
   bottom like DEVLOG.
   If today's section already exists, merge new bullets into it
   instead of duplicating.

## Style

- `devlog.md` conventions apply: terse bullets, intent plus outcome,
  identifiers only where they carry meaning, no hashes or file
  lists.
- Compress rather than copy: a reader skims the day, they do not
  re-read each log.
- `owner:` marks in source entries are preserved as-is.
- A repo that clearly saw work (`git log` shows same-day commits)
  but has no DEVLOG entry gets a single `DEVLOG gap` bullet, not an
  invented one.
