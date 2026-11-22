#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Remind to check ROADMAP.md after a DEVLOG.md edit.

== Intent ==

AGENTS.md makes ROADMAP currency a standing duty where a roadmap
exists: items get checked off and statuses adjusted in the same
task that lands them. A DEVLOG entry records the completed work
packet, so the edit that writes it is the right moment to ask
whether a roadmap item just landed.

== Method ==

Reads the hook event JSON on stdin, extracts `tool_input.file_path`,
and prints `hookSpecificOutput.additionalContext` when the touched
file is a DEVLOG.md (any directory depth). The check is conditional
by phrasing: nothing is proposed when the repo has no roadmap or
the logged work does not touch it.

== Caveats ==

- A reminder, not a verdict: whether a logged item matches a
  roadmap entry is the agent's judgment.
- Fires on every DEVLOG.md edit; repos without a ROADMAP.md simply
  skip the check (the duty itself is "where one exists").
- Pairs with devlog-backlog-reminder.py and devlog-readme-check.py
  in the same dispatch group; the dispatcher merges their contexts.

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
                'ROADMAP.md where one exists: if the logged work '
                'landed a roadmap item, check it off or adjust its '
                'status in the same task.')}}))


if __name__ == '__main__':
    main()
