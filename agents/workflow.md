# Agent session workflow

Operating principles for how an agent keeps a repo's documentation
alive across sessions. Repo AGENTS.md instantiates these with local
paths and specifics.

## AGENTS.md is a living document

If a session's discussion changes or adds conventions, update
AGENTS.md in the same task. Never leave tribal knowledge unwritten.

## DEVLOG.md: session memory

Every non-trivial work item gets a dated entry: what was done, why,
the trigger/root cause, and where the artifacts live. The user also
works solo at any time, not only between sessions: check `git log`
periodically during the session, and whenever something looks
unfamiliar (files you did not touch, code you do not recognize),
inspect the log for user commits. If undocumented, prompt the user
with a draft entry for approval and update DEVLOG.md. Do not infer
intent.

## README.md: keep it accurate

README is "what is true now and why," for an outside reader. Update it
whenever work changes: file-structure tables, getting-started
commands, stated capabilities, architectural decisions, and binding
conventions. Record the decision and its rationale, not just the
outcome.

## Tool tricks

Non-obvious tool/command knowledge lives in the workflows repo under
`tricks/` (e.g. `tricks/git-tricks.md`). Style: one `## heading` per
intent, the command block below, no lengthy explanations; a gotcha
line only when something genuinely bit.

## Documentation layering

Audience split: `AGENTS.md` is written for agents. Everything else --
README, DEVLOG, tricks/, recipes/ -- is written for humans. Write them
for a human reader: clear prose, honest framing, no agent-internal
shorthand.

- `README.md`: what is true now and why
- `DEVLOG.md`: what happened, chronologically
- `AGENTS.md`: conventions and instructions for agents
- `recipes/` in this repo: reusable workflows (see `git-privacy.md`)
- `tricks/`: terse command recipes
