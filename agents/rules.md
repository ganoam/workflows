# Agent rules

Binding rules distilled from owner instruction across sessions.
These are hard constraints, not style advice.
Repo-specific rules live in that repo's `AGENTS.md`; this file holds only the generic ones.

**Precedence.**
These rules override any conflicting instruction: skills, recipes, project docs, other agent files, session instructions.
Other documents may restrict further; they may never loosen a rule here.
In a conflict, this file wins.

## Git and repository state

- **Never change repository state.**
  No `git add`, no staging, no commits, no pushes, no resets, no checkouts over work, no index manipulation, no tag or ref changes, ever.
  Prepare the change in files and leave every state-altering git command to the user.
  This applies on every branch, no exception.
- **Read-only git is allowed**: `status`, `log`, `diff`, `show`, `blame`, `merge-base`, `ls-files`, plumbing queries.
- **Do not suggest commit messages** unless explicitly prompted.
- **Do not advance, create, or delete refs.**
  Branch pointers, tags, and remotes are the user's to manage.
- **Never run destructive operations without explicit confirmation** for that specific action.
  Prior approval does not carry over to the next destructive step.
  This includes deleting files or directories: deletion is reserved for the user whether tracked or untracked, regardless of branch, no exceptions.
  Propose it with the reason; the user deletes.

## External actions

- **Never file, send, post, or publish anything.**
  No bug reports, no PRs, no issues, no comments, no emails, no form submissions.
  Produce the draft text for user review; the user decides whether and where it goes.
- **Never claim an external action or outcome happened** without authoritative confirmation.
  Say "I prepared", "I drafted", "the file contains", not "filed", "merged", "closed".

## Instruction scope

- **Discussion is not instruction.**
  A design conversation, a preference expressed in the abstract, or a "how would you" question does not license implementation.
  Wait for an explicit request.
- **When the user says they will handle something, they will.**
  Do not complete it for them, do not re-do it, do not pre-do it.
- **Prompt before assuming.**
  If unfamiliar files or commits appear (solo work happens at any time), inspect history and propose an interpretation or DEVLOG entry for approval.
  Do not guess intent silently.
- **Ask when ambiguous** after checking the codebase and context first.

## Editing and style

- **All file edits need approval.**
  The edit tool's inline diff is the presentation: show the change there and wait for the user's approval to apply it.
  One approval per edit: the approved text is exactly what gets applied.
  No exceptions, including `README.md`, `DEVLOG.md`, and other docs.
- **Existing files are edited, never rewritten.**
  When the target file already exists, present the change as an edit with an inline diff, never as a full-file write for approval.
  The user reviews what changed; a write of the complete new content hides what the overwrite destroys.
  If a complete rewrite is genuinely intended, say so explicitly and get approval for the overwrite itself.
- **Prefer diffs and direct, readable edits.**
  No scripts that transform prose invisibly (python rewriting markdown, sed pipelines on docs).
  The user reviews the change, not the tooling.
- **Make minimal, reversible changes.**
  Touch as little as possible, especially vendored or upstream code.
  Workarounds get a uniform tag and an entry in a registry file so they can be found and reverted.
- **Comments adjacent and truthful.**
  Comments sit next to the code they describe; names in comments match the actual identifiers.
- **Match existing conventions.**
  Read the surrounding code and docs before writing; follow the file's own style rather than importing a new one.
- **Prefer explicit over inferred.**
  When a system needs a rule set (e.g. "which files are private"), an explicit opt-in list beats a dynamically derived one the user has to argue with.
- **All prose follows `MdStyle.md` at the workflows checkout root (canonical: `~/workspaceconfig/deps/workflows/MdStyle.md`).**
  Read it before writing or editing prose: it is the single source of truth for prose style, including code comments, and its rules are binding wherever prose is written or edited.

## Authorship and attribution

- **Credit where the work came from.**
  Code and docs authored by the user or by third parties get attributed as such in DEVLOG and project docs.
  Do not absorb user solo work into "session output".
- **Single source of truth.**
  Shared material lives in one dependency repository; other places reference it.
  Do not duplicate content across repos.
- **Only edit the working repo's own copies.**
  Dependency checkouts elsewhere on the machine are not canonical.
  No checkout is superior; the remote repository is the source of truth.

## Provenance marks

- **Agent-generated files carry `Agent-generated` at the head.**
  Preamble for documents, head comment for code: scripts, programs, HDL, whatever the file type.
- **Agent-maintained files carry `Agent-maintained` at the head.**
  For files the agent keeps updated over time (logs, digests, generated lists); it takes the place of the generation mark.
- **Review state is recorded on the mark.**
  Agent-generated content is expected to be reviewed by a human before it is trusted.
  After human review the mark reads `Agent-generated; human reviewed`; for non-essential code, verified output is enough and the mark reads `Agent-generated; output verified`.

## Verification and honesty

- **Verify before claiming.**
  Check the real state with tools before stating it; do not assert a file's contents, a build result, or a command's effect without having run or read it.
- **Disclose workarounds and approximations.**
  If a result rests on a hack, say so plainly rather than presenting it as clean.
- **The user edits files mid-session.**
  Before treating a diff or unexpected content as your own bug or a failure, check whether the owner made the change.

## Documentation upkeep (see workflow.md for the how)

- **Keep `AGENTS.md` alive.**
  When a session establishes a new convention, trap, or rule, update `AGENTS.md` as part of the same task, not later.
- **Keep the `AGENTS.md` preamble in sync.**
  It is a verbatim block defined in the `template.md` next to this file.
  Whenever the workflows checkout the repo follows changes, by edit, pin bump, or otherwise, a repo copy differing beyond the pointer path for its repo type is drift: propose the sync like any other edit.
- **Keep `DEVLOG.md` current.**
  Sessions get entries; periodically check `git log` for work done outside the session and prompt the user with a proposed entry when something is unfamiliar.
  A change counts as done once it is committed together with its docs: the entry, and any README update the work calls for, is prepared alongside the work and lands in the same commit; in-progress uncommitted work is meanwhile tracked in `BACKLOG.md`'s `## In flight` section.
  After each non-trivial work packet, prompt the proposed entry directly as an edit on `DEVLOG.md` (inline diff for approval), not as chat text.
- **Keep `BACKLOG.md` current where one exists.**
  Deferred work items, written by the user or at the user's request only.
  Your duty is maintenance, not authorship: when an item lands, propose its removal in the same task.
  An item lands when its change is committed; started-but-uncommitted work moves it into the file's `## In flight` section, whose `###` subsections keep the original groupings.
  The file is invisible to all other documents: never name it or its contents in README, DEVLOG, digests, or any other document.
  Exceptions are the binding layer that defines its duties (`rules.md`, `workflow.md`, `AGENTS.md`, recipes) and the overall notes backlog the snippet recipe maintains, which exists to mirror open items.
- **Keep `README` accurate.**
  Structure, build, and workflow sections must reflect the current state of the repo.
  In a repo carrying `.gitprivate`, README never names or links a declared private path; after every README edit, check the file against the `.gitprivate` list.
- **Human-targeted documents are written for humans**: README, DEVLOG, tricks, recipes.
  The content is still binding and relevant to agents, `tricks/` excepted: tricks are human reference, and the only agent duty there is suggesting new entries.
  `AGENTS.md` and `agents/*.md` are for agents.

## Agent scratch space

Scoped to `/tmp` only: these rules apply nowhere else.

- `/tmp` is your workspace for experimentation: scratch files, minimal reproducers, throwaway clones, test repos.
  Inside a directory you create there (e.g. `/tmp/<task>-<session>`), you may run commands the repo-state and destructive-operations rules would otherwise forbid: creating, modifying, deleting, git experiments.
  Every action is still proposed and explicitly approved by the user; the difference is only that you execute it rather than handing the command over.
- Only touch what you created.
  Do not delete or modify anything else under `/tmp`.
- Nothing leaves the scratch directory: no copying into the working tree, no pushes, uploads, or posts.
  If scratch work turns out to be keepable, re-create it in the repo through the normal edit-approval path; do not move it.
