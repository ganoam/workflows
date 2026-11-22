# Uniform agent setup for a repo

Set up the shared agent workflow in a repo: AGENTS.md, an optional fallback checkout, hooks, local skills, plus the one-time machine plugin install.
The single source for this setup; other repos' docs point here.

## Architecture

- This repo is a Devin plugin (`skills/` + `.devin-plugin/`) and a docs checkout at the same time.
  They play different roles: the plugin provides discovery (skill list, injected AGENTS.md, hooks); `~/workspaceconfig/deps/workflows` is the single canonical checkout every agent on the machine follows.
- Binding docs resolve through one chain: `~/workspaceconfig/deps/workflows`, then `deps/workflows` in the working repo, then `../workflows` for dependency checkouts; absent all three the agent warns the owner and prompts to clone.
  Plugin files are transport, not a content source.
- A repo-local `deps/workflows` submodule is the fallback tier: it keeps the repo self-contained on machines without `~/workspaceconfig` (the path for people not using the owner's workspace layout).
- `agents/rules.md` is injected as always-on context and overrides anything else: skills, recipes, project docs, session instructions.
- `agents/workflow.md` is the second tier: operating guidelines that bind unless `rules.md` or the user says otherwise.
- `recipes/*.md` here are human-canonical.
  Each has a generated `skills/<name>/SKILL.md` wrapper so agents discover them mechanically; the wrapper defers to the recipe file.
- A project may add its own `recipes/` directory; local overrides shared on overlap.

## One-time, per machine

```
devin plugins install ganoam/workflows
```

(`devin plugins install --local <checkout>` while authoring, links the working copy.)
This installs the rules and all generated skills; slash commands appear as `/workflows:<skill>`.

## Per repo

1. Create `AGENTS.md` from this repo's `agents/template.md`: canonical preamble verbatim, repo-local deltas only.
2. Optional fallback checkout: `git submodule add git@github.com:ganoam/workflows deps/workflows`, so machines without `~/workspaceconfig` still resolve the docs.
3. Add the canonical README entry:

   ```markdown
   This repo uses the shared ganoam agent workflow; binding docs resolve from `~/workspaceconfig/deps/workflows`, falling back to `deps/workflows` in this repo.
   Install the plugin once per machine for skills and hooks: `devin plugins install ganoam/workflows`.
   ```

4. If the repo uses the public/private workflow: `.gitprivate`, hooks via `deps/scripts/git-util/setup-git-hooks.sh` (see `git-privacy.md`).
5. If the repo has its own `recipes/` directory: run `/workflows:generate-skills` once to generate `.devin/skills/` wrappers.
   Re-run when local recipes change.

## Agent procedure: onboarding a consumer repo

When asked to set up this workflow in a repo, follow these steps.
Two rules shape everything: **no state-changing git commands**, prepare them and hand them to the owner (`git submodule add`, hook install, commits).
And **preserve existing local content**: an `AGENTS.md` that already exists holds project knowledge; fold it into the template, never overwrite it.

1. **Survey.**
   Check what already exists: `~/workspaceconfig/deps/workflows` (canonical checkout present?), `deps/workflows/` (repo-local fallback?), `AGENTS.md`, `recipes/` (project-local recipes), `.gitprivate` (public/private split?), `deps/scripts` (hooks source), README/docs that reveal project specifics.
   Also read `git log --oneline -10` for commit style and recent activity.
   **Checkout chain**: the canonical checkout is `~/workspaceconfig/deps/workflows`; if it is absent and the repo has no local `deps/workflows` either, warn the owner and prompt them to clone (the submodule command from step 2 is the repo-local option).
2. **Fallback checkout.**
   Optional but recommended: if `deps/workflows` is absent, hand the owner `git submodule add git@github.com:ganoam/workflows deps/workflows` then `git submodule update --init deps/workflows`.
   If no checkout on the chain exists at all, wait for one: later steps read `agents/template.md` from it.
3. **AGENTS.md.**
   - Absent: copy `agents/template.md` from the resolved checkout and fill every `<...>` slot from what the survey found.
     Ask the owner for anything you can't infer (project intent, build commands).
   - Present: restructure it into template shape, add the pointer preamble (rules.md, workflow.md, recipes/, tricks/), move all existing local content into the matching template sections (Repo-specific rules, Layout, Toolchain and build, Current state), delete content that merely restates shared rules (that's what the pointers are for).
     Show the owner a diff before rewriting the file.
4. **Privacy.**
   If the repo has `.gitprivate` or uses a public/private split: follow `git-privacy.md`, check the `.gitprivate` list covers the files this setup adds (AGENTS.md is commonly private; the plugin docs are public).
   Hand the owner the hooks command: `deps/scripts/git-util/setup-git-hooks.sh` (needs the `deps/scripts` submodule, another submodule command to hand over if absent).
5. **Local skills.**
   If the repo has a `recipes/` directory, follow the `generate-skills` procedure to emit `.devin/skills/<name>/` wrappers.
   These stay untracked or go to the private mirror, the owner's call, not yours.
6. **Report.**
   Summarize: what exists now, the exact commands the owner must run (submodule, hooks, commits), and propose a DEVLOG entry per `workflow.md`.
   Do not commit anything.

## Dependency repo: no own submodule

A repo that is only ever worked on as a dependency of another repo (e.g. `deps/scripts` inside a consumer checkout) does not get a `deps/workflows` submodule of its own.
It resolves the standard checkout chain; the sibling `../workflows` leg covers its case when `~/workspaceconfig` is absent.

- `AGENTS.md`: copy `agents/template.md` unchanged; the canonical preamble is identical for all repo types.
- Fallback-checkout step: skipped by definition.
- Privacy: unchanged.
  If the dep uses the public/private split, wire `.gitprivate` and hooks in the dep's own repo; the hooks source resolves by sibling convention too (`git-util/` inside the dep itself for `scripts`, `../scripts/git-util/` for other deps).
- Local skills: if the dep has `recipes/`, generate `.devin/skills/` wrappers there as usual.
- Owner hand-offs: no submodule commands; the remaining ones are commits inside the dep repo itself.

**Agent procedure variant.**
Onboarding a dep repo follows the consumer procedure above with these deltas: in the survey, verify a checkout exists on the chain (`~/workspaceconfig/deps/workflows`, else `../workflows`) and read the binding docs from there; skip the fallback-checkout step entirely; privacy, local skills, and reporting are unchanged, with hooks and commit commands scoped to the dep repo.

## Stand-alone repo: no build, no dependencies

A stand-alone repo that builds nothing and has no dependencies (notes, dotfiles, misc collections) carries no `deps/workflows` submodule.
It follows the shared workflow through `~/workspaceconfig/deps/workflows`, the chain's first leg.

- `AGENTS.md`: copy `agents/template.md` unchanged; the canonical preamble is identical for all repo types.
- Fallback-checkout step: skipped.
- Privacy, local skills, owner hand-offs: as for a dependency repo (no submodule commands; commits inside the repo itself).

**Agent procedure variant.**
Onboarding a stand-alone repo follows the consumer procedure with these deltas: in the survey, verify `~/workspaceconfig/deps/workflows` exists and read the binding docs from there.
If it is absent, do nothing and alert the user: no `AGENTS.md`, no partial setup.
Skip the fallback-checkout step; privacy, local skills, and reporting are unchanged.

## Ongoing

- Shared recipes change: edit the recipe, re-run generation in the workflows repo so its `skills/` stay in sync, commit there.
- New repo-local convention: goes in that repo's `AGENTS.md`, not here.
- `AGENTS.md` preamble drift: the canonical block lives in `agents/template.md` (verbatim, identical for all repo types); consumer copies are synced per the `rules.md` duty whenever the checkout changes.
- Rules conflict: `rules.md` wins, always; recipes may restrict, never permit.
