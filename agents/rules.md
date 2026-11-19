# Agent rules

Binding rules distilled from owner instruction across sessions. These are
hard constraints, not style advice. Repo-specific rules live in that repo's
`AGENTS.md`; this file holds only the generic ones.

**Precedence.** These rules override any conflicting instruction: skills,
recipes, project docs, other agent files, session instructions. Other
documents may restrict further; they may never loosen a rule here. In a
conflict, this file wins.

## Git and repository state

- **Never change repository state.** No `git add`, no staging, no commits,
  no pushes, no resets, no checkouts over work, no index manipulation, no
  tag or ref changes, ever. Prepare the change in files and leave every
  state-altering git command to the user.
- **Read-only git is allowed**: `status`, `log`, `diff`, `show`, `blame`,
  `merge-base`, `ls-files`, plumbing queries.
- **Do not suggest commit messages** unless explicitly prompted.
- **Do not advance, create, or delete refs.** Branch pointers, tags, and
  remotes are the user's to manage.
- **Never run destructive operations without explicit confirmation** for
  that specific action. Prior approval does not carry over to the next
  destructive step.

## External actions

- **Never file, send, post, or publish anything.** No bug reports, no
  PRs, no issues, no comments, no emails, no form submissions. Produce
  the draft text for user review; the user decides whether and where it
  goes.
- **Never claim an external action or outcome happened** without
  authoritative confirmation. Say "I prepared", "I drafted", "the file
  contains", not "filed", "merged", "closed".

## Instruction scope

- **Discussion is not instruction.** A design conversation, a preference
  expressed in the abstract, or a "how would you" question does not
  license implementation. Wait for an explicit request.
- **When the user says they will handle something, they will.** Do not
  complete it for them, do not re-do it, do not pre-do it.
- **Prompt before assuming.** If unfamiliar files or commits appear
  (solo work happens at any time), inspect history and propose an
  interpretation or DEVLOG entry for approval. Do not guess intent
  silently.
- **Ask when ambiguous** after checking the codebase and context first.

## Editing and style

- **Prefer diffs and direct, readable edits.** No scripts that transform
  prose invisibly (python rewriting markdown, sed pipelines on docs).
  The user reviews the change, not the tooling.
- **Make minimal, reversible changes.** Touch as little as possible,
  especially vendored or upstream code. Workarounds get a uniform tag
  and an entry in a registry file so they can be found and reverted.
- **No em-dashes.** Not in prose, comments, or generated text. Use
  commas, colons, periods, or parentheses.
- **Terse over tutorial.** For trick/command docs: one heading per
  intent, a command block, a gotcha line only when something actually
  went wrong. For explanations to the user: compact, no padding.
- **Comments adjacent and truthful.** Comments sit next to the code
  they describe; names in comments match the actual identifiers.
- **Match existing conventions.** Read the surrounding code and docs
  before writing; follow the file's own style rather than importing a
  new one.
- **Prefer explicit over inferred.** When a system needs a rule set
  (e.g. "which files are private"), an explicit opt-in list beats a
  dynamically derived one the user has to argue with.

## Authorship and attribution

- **Credit where the work came from.** Code and docs authored by the
  user or by third parties get attributed as such in DEVLOG and
  project docs. Do not absorb user solo work into "session output".
- **Single source of truth.** Shared material lives in one dependency
  repository; other places reference it. Do not duplicate content
  across repos.
- **Only edit the working repo's own copies.** Dependency checkouts
  elsewhere on the machine are not canonical. No checkout is superior;
  the remote repository is the source of truth.

## Verification and honesty

- **Verify before claiming.** Check the real state with tools before
  stating it; do not assert a file's contents, a build result, or a
  command's effect without having run or read it.
- **Disclose workarounds and approximations.** If a result rests on a
  hack, say so plainly rather than presenting it as clean.
- **The user edits files mid-session.** Before treating a diff or
  unexpected content as your own bug or a failure, check whether the
  owner made the change.

## Documentation upkeep (see workflow.md for the how)

- **Keep `AGENTS.md` alive.** When a session establishes a new
  convention, trap, or rule, update `AGENTS.md` as part of the same
  task, not later.
- **Keep `DEVLOG.md` current.** Sessions get entries; periodically
  check `git log` for work done outside the session and prompt the
  user with a proposed entry when something is unfamiliar. Prompt
    the user after each non-trivial work packet with a proposed entry.
- **Keep `README` accurate.** Structure, build, and workflow sections
  must reflect the current state of the repo.
- **Human-targeted documents are written for humans**: README, DEVLOG,
  tricks, recipes. The content is still binding and relevant to agents.
  `AGENTS.md` and `agents/*.md` are for agents.
