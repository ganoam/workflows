# Uniform agent setup for a repo

Set up the shared agent workflow in a repo: submodule, AGENTS.md, hooks, local skills, plus the one-time machine plugin install.
The single source for this setup; other repos' docs point here.
Two repo types carry no pin of their own: a dependency repo is onboarded through the parent's sibling checkout (see "Dependency repo"), a stand-alone non-project repo through the machine checkout `~/workspaceconfig/deps/workflows` (see "Stand-alone repo").

## Architecture

- This repo is a Devin plugin (`skills/` + `.devin-plugin/`) and a docs submodule at the same time.
  They play different roles: the plugin provides discovery (skill list, injected AGENTS.md); the repo's `deps/workflows` checkout is the canonical content: each repo pins the workflow version it follows, and plugin files are only the fallback when the submodule is absent.
- A dependency repo without its own pin follows the parent's `deps/workflows` through the sibling path `../workflows`.
- A stand-alone repo without any pin follows the machine checkout `~/workspaceconfig/deps/workflows`.
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

1. Add the submodule: `git submodule add git@github.com:ganoam/workflows deps/workflows`
2. Create a minimal `AGENTS.md`: point at `deps/workflows/agents/rules.md` and `workflow.md`, plus `deps/workflows/recipes/` and `tricks/`; then add only repo-specific deltas.
   Template lives in this repo's `agents/`.
3. If the repo uses the public/private workflow: `.gitprivate`, hooks via `deps/scripts/git-util/setup-git-hooks.sh` (see `git-privacy.md`).
4. If the repo has its own `recipes/` directory: run `/workflows:generate-skills` once to generate `.devin/skills/` wrappers.
   Re-run when local recipes change.

## Agent procedure: onboarding a consumer repo

When asked to set up this workflow in a repo, follow these steps.
Two rules shape everything: **no state-changing git commands**, prepare them and hand them to the owner (`git submodule add`, hook install, commits).
And **preserve existing local content**: an `AGENTS.md` that already exists holds project knowledge; fold it into the template, never overwrite it.

1. **Survey.**
   Check what already exists: `deps/workflows/` (submodule?), `AGENTS.md`, `recipes/` (project-local recipes), `.gitprivate` (public/private split?), `deps/scripts` (hooks source), README/docs that reveal project specifics.
   Also read `git log --oneline -10` for commit style and recent activity.
   **Version drift**: if `deps/workflows` exists, compare its pinned commit date (`git -C deps/workflows log -1 --format=%ci`) with the installed plugin's copy.
   The repo's pin is canonical: flag it to the owner if the plugin looks newer, since injected skills and pinned docs would then disagree.
2. **Submodule.**
   If `deps/workflows` is absent, hand the owner: `git submodule add git@github.com:ganoam/workflows deps/workflows` then `git submodule update --init deps/workflows`.
   Wait for it: later steps read `agents/template.md` from that checkout.
3. **AGENTS.md.**
   - Absent: copy `deps/workflows/agents/template.md` and fill every `<...>` slot from what the survey found.
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
It still follows the shared workflow through the sibling checkout: the parent's `deps/workflows`, seen from the dep's root as `../workflows`.

- `AGENTS.md`: copy `agents/template.md`, but point the preamble at `../workflows/` instead of `deps/workflows/`.
  State the fallback chain explicitly: if `../workflows` is absent (standalone checkout), use `~/workspaceconfig/deps/workflows`; if that is absent too, the injected plugin copies of `rules.md` and `workflow.md` apply.
- Submodule step: skipped by definition.
- Privacy: unchanged.
  If the dep uses the public/private split, wire `.gitprivate` and hooks in the dep's own repo; the hooks source resolves by sibling convention too (`git-util/` inside the dep itself for `scripts`, `../scripts/git-util/` for other deps).
- Local skills: if the dep has `recipes/`, generate `.devin/skills/` wrappers there as usual.
- Owner hand-offs: no submodule commands; the remaining ones are commits inside the dep repo itself.

**Agent procedure variant.**
Onboarding a dep repo follows the consumer procedure above with these deltas: in the survey, verify `../workflows` exists (else `~/workspaceconfig/deps/workflows`) and read the binding docs from there; skip the submodule step entirely; in the AGENTS.md step, write the sibling-path preamble plus the fallback chain; privacy, local skills, and reporting are unchanged, with hooks and commit commands scoped to the dep repo.

## Stand-alone repo: no build, no dependencies

A stand-alone repo that builds nothing and has no dependencies (notes, dotfiles, misc collections) carries no `deps/workflows` submodule: there is no project to pin a version against.
It still follows the shared workflow through the machine checkout `~/workspaceconfig/deps/workflows`.

- `AGENTS.md`: copy `agents/template.md`, but point the preamble at `~/workspaceconfig/deps/workflows/` instead of `deps/workflows/`.
  Fallback: if that checkout is absent, the injected plugin copies of `rules.md` and `workflow.md` apply.
- Submodule step: skipped.
- Privacy, local skills, owner hand-offs: as for a dependency repo (no submodule commands; commits inside the repo itself).

**Agent procedure variant.**
Onboarding a stand-alone repo follows the consumer procedure with these deltas: in the survey, verify `~/workspaceconfig/deps/workflows` exists and read the binding docs from there.
If it is absent, do nothing and alert the user: no `AGENTS.md`, no partial setup.
Skip the submodule step; in the AGENTS.md step, write the machine-checkout preamble; privacy, local skills, and reporting are unchanged.

## Ongoing

- Shared recipes change: edit the recipe, re-run generation in the workflows repo so its `skills/` stay in sync, commit there.
- New repo-local convention: goes in that repo's `AGENTS.md`, not here.
- Rules conflict: `rules.md` wins, always; recipes may restrict, never permit.
