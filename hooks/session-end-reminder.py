#!/usr/bin/env python3
"""Inject the session-end checklist at Stop.

== Intent ==

workflow.md requires session-end upkeep: a DEVLOG entry for the
completed work packet, plus currency checks on AGENTS.md, README.md,
ROADMAP.md, and BACKLOG.md. The hook surfaces that checklist at the
last moment the agent can still act on it.

== Method ==

Reads the hook event JSON on stdin (content ignored) and prints one
`hookSpecificOutput.additionalContext` block. It never blocks: the
hook docs warn that blocking Stop can loop (block, continue, stop,
block), and a conditional reminder lets the agent either act on a
real omission or finish cleanly.

== Caveats ==

- Stop can fire mid-session on agent pauses, not only at the end;
  the text is phrased as a conditional check so a pause produces a
  no-op rather than noise.
- The checklist asks for a check, not an action: sessions with no
  completed work legitimately produce nothing.

Usage: invoked by hooks.json (Stop, no matcher); stdin is the hook
event JSON.
"""

import json
import sys

# ------------------------------------------------------------------
# Checklist text injected when the agent stops
# ------------------------------------------------------------------

CHECKLIST = (
    'Session-end check (workflow.md): if this session completed work, '
    'make sure DEVLOG.md records the packet (outcome, not just your '
    'edits), and that AGENTS.md, README.md, ROADMAP.md, and BACKLOG.md '
    'still reflect reality: prune backlog items that landed, check off '
    'roadmap entries, fix stale docs in the same task.'
)


# ------------------------------------------------------------------
# Emit the context block; the event payload itself is unused
# ------------------------------------------------------------------

def main():
    json.load(sys.stdin)
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'Stop',
        'additionalContext': CHECKLIST}}))


if __name__ == '__main__':
    main()
