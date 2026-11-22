#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Remind to check README.md after a DEVLOG.md edit.

== Intent ==

AGENTS.md makes README accuracy a standing duty: it reflects what
is true now, updated in the same task that changes reality. A
DEVLOG entry is exactly where a completed work packet is recorded,
so the edit that writes it is the right moment to ask whether the
logged work changed what the README documents.

== Method ==

Reads the hook event JSON on stdin, extracts `tool_input.file_path`,
and prints `hookSpecificOutput.additionalContext` when the touched
file is a DEVLOG.md (any directory depth). The check is conditional
by phrasing: the README update is proposed only when the logged
work actually changes what the README documents (layout, install
contract, features, commands).

== Caveats ==

- A reminder, not a verdict: whether the entry contradicts the
  README is semantic and stays the agent's judgment.
- Fires on every DEVLOG.md edit including entries about work that
  cannot touch the README; the conditional phrasing makes it a
  no-op in practice.
- Pairs with devlog-backlog-reminder.py in the same dispatch group;
  the dispatcher merges their contexts.

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
                'README.md: if the logged work changed what it '
                'documents (layout, install contract, features, '
                'commands), propose the README update in the same '
                'task.')}}))


if __name__ == '__main__':
    main()
