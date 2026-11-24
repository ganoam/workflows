#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Check the repo's recipe index and skill wrappers against recipes/.

== Intent ==

Every recipe gets a generated SKILL.md wrapper so it becomes
agent-discoverable (the generate-skills procedure), and a
`recipes/README.md` index, where one exists, keeps one row per
recipe file. Keeping both in sync is a session-start duty; this
hook performs the compares itself and only speaks up on drift,
same contract as preamble-drift-check.py.

== Method ==

The working repo is $DEVIN_PROJECT_DIR. Left side: `recipes/*.md`
basenames minus `README.md` (the index, never a recipe), plus each
recipe's first intro sentence, which is what the wrapper's
`description:` field must carry. Right side, two surfaces:

- wrappers under `.devin/skills/<name>/SKILL.md` in a consumer
  repo, or `skills/<name>/SKILL.md` inside the workflows repo
  itself (`.devin/skills` wins when both exist)
- first-column links of `recipes/README.md` table rows, checked
  only when that index exists (the duty is conditional)

Drift shapes:

- missing:  recipe with no generated wrapper
- stale:    generated wrapper whose description differs from the
            recipe's current first sentence
- orphaned: generated wrapper whose recipe file is gone
- index:    recipe with no index row, or a row naming a file that
            no longer exists

Wrappers without `generated: true` are hand-authored and skipped
(generate-skills never clobbers them). Drift prints
`hookSpecificOutput.additionalContext`; an in-sync state or no
`recipes/` directory produces no output.

== Caveats ==

- First-sentence extraction assumes the house recipe shape: `# `
  title, optional `Agent-generated`/`Agent-maintained` mark line,
  intro paragraph. Marks are skipped wherever they appear; the
  sentence is cut at the first '. ' so a wrapped intro still
  yields its opening sentence.
- Description unparsing covers only what generate-skills emits:
  plain scalars compare verbatim; double-quoted scalars lose the
  quotes and `\\x` escape pairs collapse to `x` (the generator
  escapes only `"` and `\\`).
- A consumer repo with its own top-level `skills/` directory gets
  it mistaken for a wrapper home when `.devin/skills/` is absent;
  only `generated: true` files can false-orphan there.
- A drift flag costs a proposal, never a rewrite: flagging is the
  safe direction.

Usage: invoked by hooks.json (SessionStart, no matcher); stdin is
the hook event JSON. Requires DEVIN_PROJECT_DIR.
"""

import json
import os
import re
import sys

# ------------------------------------------------------------------
# Extraction: recipe names + first sentences, wrapper frontmatter
# ------------------------------------------------------------------

MARK = re.compile(r'^Agent-(generated|maintained)\b')


def recipes(project):
    """name -> path for each recipes/*.md; README.md is the index."""
    base = os.path.join(project, 'recipes')
    out = {}
    if os.path.isdir(base):
        for fn in sorted(os.listdir(base)):
            if fn.endswith('.md') and fn != 'README.md':
                out[fn[:-3]] = os.path.join(base, fn)
    return out


def index_names(project):
    """Recipe names linked in the first cells of the index's rows.

    Returns None when `recipes/README.md` does not exist: the
    index duty is conditional on the file being there.
    """
    path = os.path.join(project, 'recipes', 'README.md')
    try:
        text = open(path, encoding='utf-8').read()
    except OSError:
        return None
    rows = re.findall(r'^\s*\|[^|\n]*\[[^\]\n]*\]\(([^)\n]+)\)',
                      text, re.M)
    return {os.path.basename(t)[:-3] for t in rows
            if t.endswith('.md')}


def first_sentence(path):
    """First sentence of the recipe's intro paragraph.

    Skips the title, blank lines and provenance marks, collects the
    first paragraph, then cuts at the first '. '.
    """
    try:
        lines = open(path, encoding='utf-8').read().splitlines()
    except OSError:
        return ''
    para, started = [], False
    for ln in lines:
        s = ln.strip()
        if not started:
            if not s or s.startswith('#') or MARK.match(s):
                continue
            started = True
        if not s:
            break
        if MARK.match(s):
            continue
        para.append(s)
    text = ' '.join(para)
    cut = text.find('. ')
    return text[:cut + 1] if cut >= 0 else text


def wrapper_root(project):
    """The directory holding this repo's generated wrappers.

    Consumers keep repo-local wrappers under `.devin/skills/`; the
    workflows repo itself keeps the shared set at `skills/`.
    `.devin/skills` wins when both exist.
    """
    local = os.path.join(project, '.devin', 'skills')
    if os.path.isdir(local):
        return local
    shared = os.path.join(project, 'skills')
    if os.path.isdir(shared):
        return shared
    return local


def frontmatter(text):
    """The file's YAML frontmatter block, or '' when absent.

    Only the leading `---` pair counts: a `generated: true` line
    inside a fenced body example must not mark the file.
    """
    if not text.startswith('---\n'):
        return ''
    end = text.find('\n---', 4)
    return text[4:end] if end >= 0 else ''


def wrappers(base):
    """name -> (generated, description) per <base>/<name>/SKILL.md."""
    out = {}
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        path = os.path.join(base, name, 'SKILL.md')
        if not os.path.isfile(path):
            continue
        try:
            fm = frontmatter(open(path, encoding='utf-8').read())
        except OSError:
            continue
        gen = re.search(r'^generated:\s*true\s*$', fm, re.M) \
            is not None
        m = re.search(r'^description:\s*(.*)$', fm, re.M)
        desc = m.group(1).strip() if m else ''
        if len(desc) >= 2 and desc.startswith('"') \
                and desc.endswith('"'):
            desc = re.sub(r'\\(.)', r'\1', desc[1:-1])
        out[name] = (gen, desc)
    return out


# ------------------------------------------------------------------
# Compare; emit context only on drift
# ------------------------------------------------------------------

def main():
    json.load(sys.stdin)
    project = os.environ.get('DEVIN_PROJECT_DIR', '.')
    recs = recipes(project)
    wraps = {n: v for n, v in wrappers(wrapper_root(project)).items()
             if v[0]}
    index = index_names(project)
    if not recs and not wraps and index is None:
        return
    missing = sorted(n for n in recs if n not in wraps)
    orphans = sorted(n for n in wraps if n not in recs)
    stale = sorted(n for n in recs if n in wraps
                   and wraps[n][1] != first_sentence(recs[n]))
    uncovered = sorted(n for n in recs if index is not None
                       and n not in index)
    dead = sorted(n for n in index or () if n not in recs)
    if not (missing or orphans or stale or uncovered or dead):
        return
    parts = []
    if missing:
        parts.append('missing wrappers for: ' + ', '.join(missing))
    if stale:
        parts.append('stale descriptions: ' + ', '.join(stale))
    if orphans:
        parts.append('orphaned wrappers: ' + ', '.join(orphans))
    if uncovered:
        parts.append('index rows missing for: ' + ', '.join(uncovered))
    if dead:
        parts.append('index rows without recipes: ' + ', '.join(dead))
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': (
            'recipes upkeep drift (skills-sync + index duties): '
            + '; '.join(parts) + '. Re-run the generate-skills '
            'procedure and update recipes/README.md, presenting '
            'the diffs for approval.')}}))


if __name__ == '__main__':
    main()
