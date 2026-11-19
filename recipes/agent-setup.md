# Uniform agent setup for a repo

Set up the shared agent workflow in a repo: submodule, AGENTS.md,
hooks, local skills — plus the one-time machine plugin install. The
single source for this setup; other repos' docs point here.

## Architecture

- This repo is a Devin plugin (`skills/` + `.devin-plugin/`) and a
  docs submodule at the same time. They play different roles: the
  plugin provides discovery (skill list, injected AGENTS.md); the
  repo's `deps/workflows` checkout is the canonical content — each
  repo pins the workflow version it follows, and plugin files are
  only the fallback when the submodule is absent.
- `agents/rules.md` is injected as always-on context and overrides
  anything else: skills, recipes, project docs, session instructions.
- `agents/workflow.md` is the second tier: operating guidelines that
  bind unless `rules.md` or the user says otherwise.
- `recipes/*.md` here are human-canonical. Each has a generated
  `skills/<name>/SKILL.md` wrapper so agents discover them
  mechanically; the wrapper defers to the recipe file.
- A project may add its own `recipes/` directory; local overrides
  shared on overlap.

## One-time, per machine

```
devin plugins install ganoam/workflows
```

(`devin plugins install --local <checkout>` while authoring, links
the working copy.) This installs the rules and all generated skills;
slash commands appear as `/workflows:<skill>`.

## Per repo

1. Add the submodule: `git submodule add git@github.com:ganoam/workflows deps/workflows`
2. Create a minimal `AGENTS.md`: point at
   `deps/workflows/agents/rules.md` and `workflow.md`, plus
   `deps/workflows/recipes/` and `tricks/`; then add only
   repo-specific deltas. Template lives in this repo's `agents/`.
3. If the repo uses the public/private workflow: `.gitprivate`,
   hooks via `deps/scripts/git-util/setup-git-hooks.sh` (see
   `git-privacy.md`).
4. If the repo has its own `recipes/` directory: run
   `/workflows:generate-skills` once to generate `.devin/skills/`
   wrappers. Re-run when local recipes change.

## Agent procedure — onboarding a consumer repo

When asked to set up this workflow in a repo, follow these steps. Two
rules shape everything: **no state-changing git commands** — prepare
them and hand them to the owner (`git submodule add`, hook install,
commits). And **preserve existing local content** — an `AGENTS.md`
that already exists holds project knowledge; fold it into the
template, never overwrite it.

1. **Survey.** Check what already exists: `deps/workflows/`
   (submodule?), `AGENTS.md`, `recipes/` (project-local recipes),
   `.gitprivate` (public/private split?), `deps/scripts` (hooks
   source), README/docs that reveal project specifics. Also read
   `git log --oneline -10` for commit style and recent activity.
   **Version drift**: if `deps/workflows` exists, compare its pinned
   commit date (`git -C deps/workflows log -1 --format=%ci`) with the
   installed plugin's copy. The repo's pin is canonical — flag it to
   the owner if the plugin looks newer, since injected skills and
   pinned docs would then disagree.
2. **Submodule.** If `deps/workflows` is absent, hand the owner:
   `git submodule add git@github.com:ganoam/workflows deps/workflows`
   then `git submodule update --init deps/workflows`. Wait for it —
   later steps read `agents/template.md` from that checkout.
3. **AGENTS.md.**
   - Absent: copy `deps/workflows/agents/template.md` and fill every
     `<...>` slot from what the survey found. Ask the owner for
     anything you can't infer (project intent, build commands).
   - Present: restructure it into template shape — add the pointer
     preamble (rules.md, workflow.md, recipes/, tricks/), move all
     existing local content into the matching template sections
     (Repo-specific rules, Layout, Toolchain and build, Current
     state), delete content that merely restates shared rules (that's
     what the pointers are for). Show the owner a diff before
     rewriting the file.
4. **Privacy.** If the repo has `.gitprivate` or uses a
   public/private split: follow `git-privacy.md` — check the
   `.gitprivate` list covers the files this setup adds (AGENTS.md is
   commonly private; the plugin docs are public). Hand the owner the
   hooks command: `deps/scripts/git-util/setup-git-hooks.sh` (needs
   the `deps/scripts` submodule — another submodule command to hand
   over if absent).
5. **Local skills.** If the repo has a `recipes/` directory, follow
   the `generate-skills` procedure to emit `.devin/skills/<name>/`
   wrappers. These stay untracked or go to the private mirror — the
   owner's call, not yours.
6. **Report.** Summarize: what exists now, the exact commands the
   owner must run (submodule, hooks, commits), and propose a DEVLOG
   entry per `workflow.md`. Do not commit anything.

## Ongoing

- Shared recipes change: edit the recipe, re-run generation in the
  workflows repo so its `skills/` stay in sync, commit there.
- New repo-local convention: goes in that repo's `AGENTS.md`, not
  here.
- Rules conflict: `rules.md` wins, always; recipes may restrict,
  never permit.
