#!/usr/bin/env python3
"""Dispatch a hooks.json event/matcher group to its hook scripts.

== Intent ==

hooks.json should carry no scripting and no wiring knowledge: one
entry per (event, matcher) group resolves this file and hands it a
dispatch key. This table is then the single auditable place where
hooks are registered: adding a hook is a script plus one line here.

== Method ==

Reads the hook event JSON on stdin once, looks up the key in
DISPATCH, and runs each listed script from this directory (located
relative to `__file__`, so whichever workflows checkout copy the
resolver executed supplies its own scripts) with the same payload
re-fed on its stdin.

Outputs are merged: the first `decision` object wins (a block from
any script blocks), and all `hookSpecificOutput.additionalContext`
strings are joined into one context object so several reminders can
coexist in a group.

== Caveats ==

- Scripts that emit neither a decision nor additionalContext are
  silent, and a group where nothing fires produces no output.
- A script's non-JSON stdout (a stray print, a traceback) is
  dropped, not relayed: hook output must stay machine-readable.
- The resolver chain in hooks.json is the only remaining shell in
  the wiring; it exists because the command must locate this file
  before Python can run.

Usage: hooks/run-event.py <dispatch-key> < event JSON on stdin;
keys are defined by DISPATCH below.
"""

import json
import os
import subprocess
import sys

# ------------------------------------------------------------------
# Dispatch table: key -> hook scripts for that event/matcher group.
# The key is the argv name hooks.json uses; the MAINTAINING.md hooks
# table points at the scripts themselves.
# ------------------------------------------------------------------

DISPATCH = {
    'pretooluse-exec': [
        'git-state-guard.py',
        'external-action-guard.py',
        'destructive-cmd-guard.py',
    ],
    'pretooluse-write': [
        'write-overwrite-guard.py',
    ],
    'posttooluse-edit-write': [
        'devlog-backlog-reminder.py',
        'devlog-readme-check.py',
        'devlog-roadmap-check.py',
        'em-dash-reminder.py',
    ],
    'sessionstart': [
        'session-start-reminder.py',
        'preamble-drift-check.py',
    ],
    'stop': [
        'session-end-reminder.py',
    ],
}


# ------------------------------------------------------------------
# Run the group's scripts over the shared payload, merge outputs
# ------------------------------------------------------------------

def run(script_dir, name, payload):
    """One hook script: same stdin payload, JSON object on stdout."""
    out = subprocess.run(
        ['python3', os.path.join(script_dir, name)],
        input=payload, capture_output=True, text=True).stdout.strip()
    if not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def main():
    payload = sys.stdin.read()
    key = sys.argv[1] if len(sys.argv) > 1 else ''
    scripts = DISPATCH.get(key)
    if not scripts:
        return
    script_dir = os.path.dirname(os.path.abspath(__file__))

    blocks, contexts = [], []
    for name in scripts:
        obj = run(script_dir, name, payload)
        if not obj:
            continue
        if obj.get('decision'):
            blocks.append(obj)
        ctx = obj.get('hookSpecificOutput', {}).get('additionalContext')
        if ctx:
            contexts.append(ctx)

    # A block from any script blocks; otherwise all reminders merge
    # into one context object under the payload's own event name.
    if blocks:
        print(json.dumps(blocks[0]))
    elif contexts:
        event = json.loads(payload).get('hook_event_name', '')
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': event,
            'additionalContext': '\n'.join(contexts)}}))


if __name__ == '__main__':
    main()
