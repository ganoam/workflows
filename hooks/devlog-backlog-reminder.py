#!/usr/bin/env python3
"""Remind to check BACKLOG.md after a DEVLOG.md edit.

== Intent ==

rules.md makes BACKLOG.md a maintained document: a deferred item
lands when its change is committed, and its removal is proposed in
the same task. DEVLOG entries are exactly where landing gets
recorded, so an edit to a DEVLOG.md is the right moment to surface
the check mechanically.

== Method ==

Reads the hook event JSON on stdin, extracts `tool_input.file_path`,
and prints `hookSpecificOutput.additionalContext` when the touched
file is a DEVLOG.md (any directory depth). All other files stay
silent. A reminder, not a gate: whether an item actually landed is
the agent's judgment.

== Caveats ==

- Fires on every DEVLOG.md edit, including entries that log no
  landed backlog work; the reminder text is phrased as a check.
- The matcher also covers `write` so a new DEVLOG.md is caught;
  basename matching (`endswith`) keeps it depth-agnostic.

Usage: invoked by hooks.json (PostToolUse, matcher ^(edit|write)$);
stdin is the hook event JSON.
"""

import json
import sys

# ------------------------------------------------------------------
# Emit the reminder when a DEVLOG.md was touched
# ------------------------------------------------------------------

def main():
    p = json.load(sys.stdin).get('tool_input', {}).get('file_path', '')
    if p.endswith('DEVLOG.md'):
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PostToolUse',
            'additionalContext': (
                'A DEVLOG entry was just written. Check the repo '
                'BACKLOG.md: if the logged work landed a deferred '
                'item, propose its removal in the same task.')}}))


if __name__ == '__main__':
    main()
