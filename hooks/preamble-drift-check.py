#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Compare the repo AGENTS.md preamble against the canonical template.

== Intent ==

rules.md makes the consumer AGENTS.md preamble a verbatim copy of
`agents/template.md`: only the pointer path varies by repo type.
A preamble that differs is drift and gets a sync proposal. The hook
turns that duty into a mechanical verdict: it performs the compare
and only speaks up when the two sides actually differ.

== Method ==

The script lives inside the workflows checkout, so `git rev-parse
--show-toplevel` anchored at `__file__` yields that checkout's root
regardless of the script's depth or which copy the resolver ran;
`agents/template.md` sits under it. The canonical preamble is
everything in the template before the `<Canonical preamble:` marker
note. The consumer preamble is everything in `$DEVIN_PROJECT_DIR/
AGENTS.md` before its first `## ` section. The compare is a byte
compare modulo edge whitespace: the preamble is identical for all
repo types now that the canonical checkout is a single machine
path, so no variation is sanctioned.

A drift hit prints `hookSpecificOutput.additionalContext` naming the
divergence; identical (or absent) preambles produce no output.

== Caveats ==

- Only files containing the canonical "Generic binding rules" line
  are checked; that exempts this repo's own AGENTS.md, which is the
  plugin rules file with a deliberately different preamble.
- Whitespace at the edges is tolerated; every interior difference
  (missing or extra sentences, stale two-doc wording, a renamed
  title, a hand-edited path) is reported as drift, which is the
  safe direction: the human reviewing the sync proposal sees the
  real diff.

Usage: invoked by hooks.json (SessionStart, no matcher); stdin is
the hook event JSON. Requires DEVIN_PROJECT_DIR.
"""

import json
import os
import subprocess
import sys

# ------------------------------------------------------------------
# Extraction and normalization
# ------------------------------------------------------------------

SENTINEL = 'Generic binding rules and operating workflow live in'


def wf_root():
    """The workflows checkout root, wherever this script sits in it."""
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run(
        ['git', '-C', here, 'rev-parse', '--show-toplevel'],
        capture_output=True, text=True)
    return out.stdout.strip() or None


def template_preamble(root):
    """The canonical block: template text up to the marker note."""
    if not root:
        return None
    path = os.path.join(root, 'agents', 'template.md')
    try:
        text = open(path, encoding='utf-8').read()
    except OSError:
        return None
    marker = text.find('<Canonical preamble:')
    if marker < 0:
        return None
    return text[:marker]


def repo_preamble():
    """The consumer preamble: repo AGENTS.md up to its first `## `.

    Returns None when the file is absent or does not carry the
    canonical opener (e.g. the workflows repo's own plugin file),
    which takes it outside this check's scope.
    """
    path = os.path.join(os.environ.get('DEVIN_PROJECT_DIR', '.'),
                        'AGENTS.md')
    try:
        text = open(path, encoding='utf-8').read()
    except OSError:
        return None
    if SENTINEL not in text:
        return None
    cut = text.find('\n## ')
    return text[:cut] if cut >= 0 else text


def norm(text):
    """Drop edge whitespace; the interior compare is exact."""
    return text.strip()


# ------------------------------------------------------------------
# Compare; emit context only on drift
# ------------------------------------------------------------------

def main():
    json.load(sys.stdin)
    canon = template_preamble(wf_root())
    actual = repo_preamble()
    if canon is None or actual is None:
        return
    if norm(canon) != norm(actual):
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'SessionStart',
            'additionalContext': (
                'AGENTS.md preamble drifted from agents/template.md '
                '(rules.md preamble-sync duty): compare the two, then '
                'propose a verbatim sync through the edit-approval '
                'path. Only the workflows pointer path may differ.')}}))


if __name__ == '__main__':
    main()
