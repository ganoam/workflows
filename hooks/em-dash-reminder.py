#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Remind about the no-em-dashes prose rule when an edit introduces one.

== Intent ==

MdStyle.md forbids em/en-dashes in prose, comments, and generated
text; the rule is binding but was skipped in practice, so the
post-edit hook surfaces it mechanically at the point of change.

== Method ==

Reads the hook event JSON on stdin, extracts the text the tool just
applied (edit: `new_string`, write: `content`), and counts unicode
dashes (em, en, horizontal bar). Any hit prints a
`hookSpecificOutput.additionalContext` reminder naming the rule and
the allowed replacements. Checking applied text rather than
blocking keeps the check cheap and leaves justified deviations to
the reviewer.

== Caveats ==

- A reminder, not a gate: MdStyle.md permits justified deviation
  (verbatim quotes, upstream material).
- `--` and ASCII '-' are not flagged; they are legitimate in code
  and CLI text.
- Notebook edits and exec-side writes sit outside the matcher.

Usage: invoked by hooks.json (PostToolUse, matcher edit|write);
stdin is the hook event JSON.
"""

import json
import sys

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

DASHES = '—–―'      # em-dash, en-dash, horizontal bar


# ------------------------------------------------------------------
# Check: count dashes in the applied text, remind on any hit
# ------------------------------------------------------------------

def main():
    data = json.load(sys.stdin)
    ti = data.get('tool_input', {})
    # edit carries `new_string`, write carries `content`; the hook
    # only inspects what was added, never the surrounding file.
    text = ti.get('new_string') or ti.get('content') or ''
    n = sum(text.count(d) for d in DASHES)
    if n:
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PostToolUse',
            'additionalContext': (
                f'{n} em/en-dash(es) in the applied text. MdStyle.md '
                'forbids them in prose, comments, and generated text: '
                'use a comma, colon, period, or parentheses instead. '
                'Justified deviations (verbatim quotes, upstream '
                'material) may stay if stated.')}}))


if __name__ == '__main__':
    main()
