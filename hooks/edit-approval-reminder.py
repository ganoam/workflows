#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Remind before every file edit that edits need approval first.

== Intent ==

rules.md requires explicit user approval for every file edit: the
change is presented as an inline diff or draft and only the
approved text is applied. This hook re-injects that rule on every
edit and write call, because the failure it guards against is
judgmental: expanding a narrow instruction into an unapproved
design and applying it in one burst. A per-call reminder is the
strongest mechanical backstop available for a property (user
approval) that the event payload cannot carry.

== Method ==

Unconditional: every PreToolUse event on `edit` or `write` emits
the reminder as `hookSpecificOutput.additionalContext`. It never
blocks: approval status is conversation state the payload does not
carry, so no mechanical verdict is possible.

== Caveats ==

- Fires on every edit and write call, including ones the user just
  approved; the noise is the price of the reminder.
- A reminder is not a gate: it can be ignored. rules.md remains
  authoritative.

Usage: invoked by hooks.json (PreToolUse, matcher `^(edit|write)$`);
stdin is the hook event JSON.
"""

import json
import sys


def main():
    json.load(sys.stdin)
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'additionalContext': (
            'Edit rule (agents/rules.md): every file edit '
            'unconditionally requires explicit user approval before '
            'it is applied. Show the change first and apply only '
            'the approved text; do not expand a narrow instruction '
            'into an unapproved design.')}}))


if __name__ == '__main__':
    main()
