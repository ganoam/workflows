#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Inject the session-start checklist at SessionStart.

== Intent ==

workflow.md requires a session-start orientation: re-read the binding
docs (rules.md, workflow.md, MdStyle.md), read the repo's AGENTS.md,
skim DEVLOG.md, and inspect `git status`/`git log` for work that is
not the agent's own. The hook makes that mechanical instead
of recall-based.

== Method ==

Reads the hook event JSON on stdin (content ignored) and prints one
`hookSpecificOutput.additionalContext` block listing the checklist.
Nothing is gated; every item is a read or an attitude toward
unfamiliar work, so a reminder is the right level.

== Caveats ==

- SessionStart also fires on resume and after context clearing;
  re-injecting the checklist there is intentional (post-compaction
  context benefits from the reminder).
- The checklist names duties, not paths: which checkout holds the
  binding docs is resolved by AGENTS.md itself.
- The preamble-sync and skills-sync duties are not listed:
  preamble-drift-check.py and skills-drift-check.py perform those
  compares themselves at the same event.

Usage: invoked by hooks.json (SessionStart, no matcher); stdin is
the hook event JSON.
"""

import json
import sys

# ------------------------------------------------------------------
# Checklist text injected into the session
# ------------------------------------------------------------------

CHECKLIST = (
    'Session start duties (workflow.md, rules.md): '
    're-read the binding docs (agents/rules.md, agents/workflow.md, '
    'MdStyle.md) via the checkout chain in AGENTS.md; read the repo '
    'AGENTS.md and skim DEVLOG.md for current state; run `git status` '
    'and `git log` to spot work that is not yours, and propose a '
    'DEVLOG interpretation before treating it.'
)


# ------------------------------------------------------------------
# Emit the context block; the event payload itself is unused
# ------------------------------------------------------------------

def main():
    json.load(sys.stdin)
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': CHECKLIST}}))


if __name__ == '__main__':
    main()
