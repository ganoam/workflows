# AGENTS.md: notes for anyone working in this repo

Generic binding rules and operating workflow live in `~/workspaceconfig/deps/workflows/agents/` (`rules.md`, `workflow.md`) and the prose style guide `~/workspaceconfig/deps/workflows/MdStyle.md`; all apply in full here.
Resolve them through the checkout chain: `~/workspaceconfig/deps/workflows`, then `deps/workflows` in this repo, then `../workflows` for dependency checkouts; if none exists, warn the owner and prompt them to clone the workflows repo.
This file holds only repo-specific guidance.
Keep it current per the shared rules.

<Canonical preamble: everything from the `# AGENTS.md` title through this note's preceding line is copied verbatim into every consumer `AGENTS.md`.
Keep it byte-identical so drift is a string compare; it is identical for all repo types now that the canonical checkout is a single machine path.>

## What this is

<One paragraph: what the project is, who it is for, why it exists.>

## Repo-specific rules

<Only deltas on top of the shared rules. Examples:>

- <e.g. "Minimal changes to vendored files.">
- <e.g. commit style, e.g. `[area] short lowercase summary`>

## Reusable workflows

`deps/workflows/recipes/` documents reusable detailed workflows (resolved through the preamble checkout chain); a project-local `recipes/` directory, if present, layers on top and overrides.
When a task falls under one, read and follow it.

Project-local recipes here: <list or "none yet">

## Layout

<Vendored vs. authored, key directories, submodules and what they provide.>

## Toolchain and build

<Tool paths/versions, build commands, test commands, where artifacts land.>

## Current state and next steps

<What works now, what is next.
Keep short; details live in ROADMAP and DEVLOG.>
