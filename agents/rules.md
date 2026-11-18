# Agent working rules

Binding rules for agent sessions in any repo. Repo AGENTS.md files may
add rules; they may not weaken these.

- **Never change repo state via git.** No `git add`, no staging, no
  commits, no pushes, no resets, no index manipulation — ever. Prepare
  the change and leave every state-altering git command to the user.
  Read-only git (`status`, `log`, `diff`, `show`) is fine. Do not even
  suggest commit messages unless prompted.
- **Never file, post, or publish anything externally.** Bug reports,
  PRs, comments, emails, applications: drafts for review only. The
  user sends.
- **Discussion is not instruction.** If the user argues a design or
  wording point, do not implement it until explicitly asked.
- **The user edits files mid-session.** If a file differs from your
  earlier read, check for user edits before assuming your operation
  failed.
- **Destructive operations need explicit confirmation.** Deleting
  files you did not create, resets, branch deletion, worktree removal:
  describe what you will run and wait.
