#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Block the write tool when the target file already exists.

== Intent ==

agents/rules.md: existing files are edited, never rewritten — the
change is presented as an edit with an inline diff for approval.
A full-file `write` on an existing path bypasses that approval and
is also how the destructive-overwrite class reaches files without
a shell command, so the hook blocks it at the tool boundary.

== Method ==

Reads the hook event JSON on stdin, extracts `tool_input.file_path`,
and checks whether the path already exists as a file. A hit emits
{"decision": "block"} telling the agent to go through the edit
tool; a genuinely intended complete rewrite is the user's to apply.

== Caveats ==

- A new file (no existing path) always passes; nothing else about
  the write is judged.
- Path is taken verbatim from tool_input; the tool resolves it
  against the project dir, and so does os.path.isfile when the
  hook's cwd is the project dir (it is: hook commands run there).

Usage: invoked by hooks.json (PreToolUse, matcher ^write$); stdin
is the hook event JSON.
"""

import json
import os
import sys

# ------------------------------------------------------------------
# Check: does the target already exist as a file?
# ------------------------------------------------------------------

def main():
    p = json.load(sys.stdin).get('tool_input', {}).get('file_path', '')
    if os.path.isfile(p):
        print(json.dumps({
            'decision': 'block',
            'reason': ('Blocked: the file already exists '
                       '(agents/rules.md: existing files are edited, '
                       'never rewritten). Present the change via the '
                       'edit tool inline diff; if a complete rewrite '
                       'is genuinely intended, the user applies it.')}))


if __name__ == '__main__':
    main()
