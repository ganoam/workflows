#!/usr/bin/env python3
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
AGENTS.md` before its first `## ` section. Before comparing, every
backticked path containing `workflows` is masked on both sides: that
is the one sanctioned variation (deps/workflows vs ../workflows vs
~/workspaceconfig/deps/workflows by repo type).

A drift hit prints `hookSpecificOutput.additionalContext` naming the
divergence; identical (or absent) preambles produce no output.

== Caveats ==

- Only files containing the canonical "Generic binding rules" line
  are checked; that exempts this repo's own AGENTS.md, which is the
  plugin rules file with a deliberately different preamble.
- Whitespace at the edges is tolerated; interior differences
  (missing sentences, extra sentences, stale two-doc wording, a
  renamed title) are all reported as drift.
- A false path variation (a repo type the mask does not cover) would
  surface as drift, which is the safe direction: the human reviewing
  the sync proposal sees the real diff.

Usage: invoked by hooks.json (SessionStart, no matcher); stdin is
the hook event JSON. Requires DEVIN_PROJECT_DIR.
"""

import json
import os
import re
import subprocess
import sys

# ------------------------------------------------------------------
# Extraction and normalization
# ------------------------------------------------------------------

# The one sanctioned preamble variation: the pointer path into the
# workflows checkout, which differs by repo type. Every backticked
# span containing 'workflows' collapses to a fixed token.
WF_PATH = re.compile(r'`[^`]*workflows[^`]*`')
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
    """Mask pointer paths, drop edge whitespace for the compare."""
    return WF_PATH.sub('<WF>', text).strip()


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
