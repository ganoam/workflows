# Roadmap

Agent-maintained; human reviewed.
Goal: one install gives every project the same agent workflow (binding rules, operating conventions, discoverable recipes) with minimal per-repo setup.
Procedure doc: `recipes/agent-setup.md`; maintenance doc: `MAINTAINING.md`.

The repo evolves by need rather than by plan: sections accumulate as workstreams emerge, order is historical, and item checkboxes carry the status.

## Foundation docs

Shared conventions distilled from the `hw-commons` sessions and reviewed by the owner.

- [x] `agents/rules.md` (binding, precedence clause) and `agents/workflow.md` (second tier).
- [ ] `recipes/`: left open on purpose; evolves naturally as repeated procedures emerge, no target list.
  Contents live in the directory itself.
- [x] `tricks/` populated; `README.md`, `DEVLOG.md`, `MAINTAINING.md`.

## Plugin packaging

The repo doubles as a Devin plugin: discovery (skill list, injected root `AGENTS.md`) on top of the docs.

- [x] `.devin-plugin/plugin.json` manifest.
- [x] Plugin-root `AGENTS.md`: thin pointer establishing rules.md > workflow.md > consumer AGENTS.md precedence.
- [x] `skills/` wrappers per shared recipe + `generate-skills` generator (`generated: true` marker, prune/skip rules).
- [x] `agents/template.md` consumer `AGENTS.md` template.
- [x] Restrict-never-permit convention in `workflow.md`.
- [ ] Install test: `devin plugins install --local`, verify `/workflows:*` skills list and rules inject.

## Consistency model

One machine checkout as the canonical copy for every agent; the plugin ships discovery only.
Pivoted 2026-11-22 from the per-repo pin model described by the struck items: each consumer's `deps/workflows` used to be the canonical content (repos pinned the workflow version they followed); now `~/workspaceconfig/deps/workflows` is canonical and repo-local checkouts are the fallback tier.

- ~~[x] Canonical-pin rule: consumer `deps/workflows` checkout is the content; plugin files are fallback when the submodule is absent.~~
- ~~[x] Wrappers and injected `AGENTS.md` resolve `deps/workflows/` first; shared vs. local wrapper bodies distinguished.~~
- ~~[x] Drift check in `agent-setup` survey step.~~
- [x] `~/workspaceconfig/deps/workflows` is the single canonical checkout; `deps/workflows` in the working repo and `../workflows` are fallbacks; absent all three, the agent warns and prompts to clone.
- [x] Wrappers and injected `AGENTS.md` resolve the checkout chain; shared vs. local wrapper bodies distinguished.
- [x] Checkout-chain verification in the `agent-setup` survey step.
- [x] Re-read instruction in injected `AGENTS.md`: checkout edits take effect mid-session.
- [x] Standing duties in injected `AGENTS.md`: README accurate, DEVLOG per task, propose recipes/tricks.
- [x] `rules.md` edit-approval rule: verbatim inline diff, one approval per edit.

## Rollout

Apply `recipes/agent-setup.md` per repo; hw-commons is the pilot.

- [x] `hw-commons`: `AGENTS.md` from template, project-local deltas preserved.
- [ ] `hw-commons`: run `generate-skills` -> `.devin/skills/` for local recipes (untracked or private, owner's call); README getting-started line for plugin install.
- [ ] Remaining consumer repos (list kept private): submodule + template `AGENTS.md` + hooks each.

## Hardening

Optional strengthening work; items land when they land.

- [ ] `permissions.deny` on skills (block exec for doc procedures).
- [x] Plugin `hooks.json` for git guards: documented fail-open today; `deps/scripts` hooks stay the real backstop; revisit when hardened.
- [ ] Consumer README boilerplate line with the plugin install command.
- [x] Em-dash consistency: `rules.md` forbids em-dashes in generated text, but this repo's own docs and the `generate-skills` wrapper template still use them.
  Sweep docs and template, or declare generated wrappers exempt.
- [x] Sentence-per-line sweep of this repo's prose docs (`agents/`, `recipes/`, `tricks/`, `README`/`DEVLOG`/`MAINTAINING`/`ROADMAP`) per the new `rules.md` style rule; timing is the owner's call.

## Notes and open decisions

- Root `AGENTS.md` carries the injected pointer rather than a `rules/` triggered file: settled, revisit only if rule injection proves insufficient.
- `workflow.md` is read-on-demand per the pointer (keeps injected context light); `rules.md` points at it.
- `MdStyle.md` is bound by a `rules.md` pointer; proposed-rule candidates were dropped as document-specific.
- Generated `skills/` wrappers are committed so the plugin is complete out of the box; regenerate via `generate-skills`, never hand-edit.
- ~~Plugin + submodule are both kept: plugin for mechanics, submodule for browsable docs, stable paths, and the version pin.~~
- Plugin + machine checkout are both kept after the 2026-11-22 pivot: plugin for mechanics (skills, hooks, injected pointer), `~/workspaceconfig/deps/workflows` as the canonical content; repo-local `deps/workflows` stays as the fallback tier.
