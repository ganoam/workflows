#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Check .devin/skills/ wrappers against the repo's recipes/.

== Intent ==

Every repo-local recipe gets a generated SKILL.md wrapper under
`.devin/skills/` so it becomes agent-discoverable (the
generate-skills procedure). Keeping that directory in sync is a
session-start duty; this hook performs the compare itself and
only speaks up on drift, same contract as preamble-drift-check.py.

== Method ==

The working repo is $DEVIN_PROJECT_DIR. Left side: `recipes/*.md`
basenames, plus each recipe's first intro sentence, which is what
the wrapper's `description:` field must carry. Right side:
`.devin/skills/<name>/SKILL.md` frontmatter. Three drift shapes:

- missing:  recipe with no generated wrapper
- stale:    generated wrapper whose description differs from the
            recipe's current first sentence
- orphaned: generated wrapper whose recipe file is gone

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
- A drift flag costs a regenerate proposal, never a rewrite:
  flagging is the safe direction.

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
    """name -> path for each recipes/*.md in the working repo."""
    base = os.path.join(project, 'recipes')
    out = {}
    if os.path.isdir(base):
        for fn in sorted(os.listdir(base)):
            if fn.endswith('.md'):
                out[fn[:-3]] = os.path.join(base, fn)
    return out


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


def wrappers(project):
    """name -> (generated, description) per .devin/skills/*/SKILL.md."""
    base = os.path.join(project, '.devin', 'skills')
    out = {}
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        path = os.path.join(base, name, 'SKILL.md')
        if not os.path.isfile(path):
            continue
        try:
            text = open(path, encoding='utf-8').read()
        except OSError:
            continue
        gen = re.search(r'^generated:\s*true\s*$', text, re.M) \
            is not None
        m = re.search(r'^description:\s*(.*)$', text, re.M)
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
    wraps = {n: v for n, v in wrappers(project).items() if v[0]}
    if not recs and not wraps:
        return
    missing = sorted(n for n in recs if n not in wraps)
    orphans = sorted(n for n in wraps if n not in recs)
    stale = sorted(n for n in recs if n in wraps
                   and wraps[n][1] != first_sentence(recs[n]))
    if not (missing or orphans or stale):
        return
    parts = []
    if missing:
        parts.append('missing wrappers for: ' + ', '.join(missing))
    if stale:
        parts.append('stale descriptions: ' + ', '.join(stale))
    if orphans:
        parts.append('orphaned wrappers: ' + ', '.join(orphans))
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': (
            '.devin/skills/ drifted from recipes/ (skills-sync '
            'duty): ' + '; '.join(parts) + '. Re-run the '
            'generate-skills procedure and present the wrapper '
            'diffs for approval.')}}))


if __name__ == '__main__':
    main()
