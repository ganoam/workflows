#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Block external actions via the gh CLI at PreToolUse.

== Intent ==

agents/rules.md: the agent never files, sends, posts, or publishes
anything; it produces drafts and the user submits. For the GitHub
CLI this is mechanically checkable, so the hook blocks every
mutating `gh` invocation.

== Method ==

Reads the hook event JSON on stdin, extracts `tool_input.command`,
and applies three checks, all anchored to command position so
quoted mentions like `echo "gh pr create"` stay silent:

  1. `gh <object> <verb>` where the verb is on a write list
     (create/edit/close/merge/delete/review/...) across the gh
     objects that carry mutations (pr, issue, release, repo, gist,
     workflow, label, project, ruleset, secret, variable, run,
     cache).
  2. `gh api`: blocked when the call carries a non-GET method
     (--method/-X POST|PUT|PATCH|DELETE) or -f/-F fields.
  3. `gh auth`: blocked wholesale; it is also the credential path
     (`gh auth token` would leak the token into context).

Read verbs (view, list, diff, status, checks, search, watch) and
plain `gh api` GET pass untouched.

== Caveats ==

- Other channels stay rule-only: `curl`, `mail`, `ssh`, and direct
  network writes are too broad to regex safely (a POST to a local
  test server is legitimate).
- The verb list is a snapshot of gh's write surface; a newly added
  mutating sub-command is blocked by neither this hook nor the
  regex until the list is extended.

Usage: invoked by hooks.json (PreToolUse, matcher ^exec$); stdin is
the hook event JSON. Blocked commands emit {"decision": "block"}.
"""

import json
import re
import sys

# ------------------------------------------------------------------
# Command classification
# ------------------------------------------------------------------

# gh invocation prefix: command start (or after a separator), then
# any mix of global options and their values before the object.
G = (r'(?:^|[;&|(]+\s*)gh(?:\s+(?:-{1,2}[\w-]+(?:=\S+)?)'
     r'(?:\s+\S+)?)*\s+')

# <object> <write-verb> pairs that mutate remote state.
W = (r'(pr|issue|release|repo|gist|workflow|label|project|ruleset|'
     r'secret|variable|run|cache)\s+'
     r'(create|edit|close|reopen|merge|comment|delete|review|ready|'
     r'lock|unlock|pin|unpin|transfer|upload|publish|run|dispatch|'
     r'rerun|enable|disable|set|set-default|fork|archive|unarchive|'
     r'rename|sync|checkout|adopt|clear|link|unlink|mark-|copy)\b')

# Non-GET detection inside an `api` call: explicit method flags or
# field parameters (-f/-F imply a write request).
API_WRITE = (r'(--method[=\s]|-X)[=\s]*["\x27]?'
             r'(POST|PUT|PATCH|DELETE)\b|-[fF]\s')


def blocked(c):
    """True if the command contains a mutating gh invocation."""
    api = re.search(G + r'api\b[^;&|]*', c)
    return bool(re.search(G + W, c)
                or re.search(G + r'auth\b', c)
                or (api and re.search(API_WRITE, api.group(0))))


# ------------------------------------------------------------------
# Emit a block decision on a hit, silence otherwise
# ------------------------------------------------------------------

def main():
    c = json.load(sys.stdin).get('tool_input', {}).get('command', '')
    if blocked(c):
        print(json.dumps({
            'decision': 'block',
            'reason': ('Blocked: agents never file, send, post, or '
                       'publish anything (agents/rules.md); the agent '
                       'produces drafts, the user submits. Read-only '
                       'gh queries are allowed.')}))


if __name__ == '__main__':
    main()
