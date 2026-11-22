#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Block destructive commands at PreToolUse.

== Intent ==

agents/rules.md reserves deletion and destructive operations for
the user, and requires file edits to go through the edit tool's
inline-diff approval. The hook blocks both classes mechanically:

  1. Deletion/destruction primitives (rm, shred, wipe, find
     -delete, dd of=, mkfs, truncate).
  2. Commands that overwrite or in-place-modify an existing file
     outside the approved edit path: `>`/echo redirections, `tee`,
     `mv`/`cp`/`ln`/`rsync`/`install` onto an existing path, and
     `sed -i`/`perl -i`.

Class 2 is what closes the loop a verb blocklist cannot: the same
data dies via truncation and overwrite as via `rm`, and exec-side
writes evade the edit-tool approval the rule requires.

== Method ==

Reads the hook event JSON on stdin, extracts `tool_input.command`,
and resolves targets against the filesystem (`DEVIN_PROJECT_DIR`,
following a leading `cd`). Effect-based checks:

  - Any `>`/`>`/`<n>>`/`&>`/`>>|`-style redirection whose target
    already exists; `>>` append passes (lookbehind on the second
    `>`).
  - mv/cp/ln/rsync/install whose final non-flag token is an
    existing file.
  - tee without -a onto an existing file.
  - Primitive blocklist matched at command position so quoted
    mentions stay silent.

A hit emits {"decision": "block"}; the command goes to the user.

== Caveats ==

- Stricter than the rule on purpose: confirmed destructive ops are
  blocked too, because the hook cannot see conversational
  confirmation. The user runs them.
- Commands mentioning /tmp are exempt (agent scratch space, per
  rules.md).
- Not caught, by design disclosed in MAINTAINING.md: interpreter
  writes (`python -c "os.remove(...)"`), directory-level effects
  (`rsync --delete`), `>` onto an existing *empty* file, and a
  `mv` into an existing directory with a colliding basename.

Usage: invoked by hooks.json (PreToolUse, matcher ^exec$); stdin is
the hook event JSON.
"""

import json
import os
import re
import sys

# ------------------------------------------------------------------
# Command classification
# ------------------------------------------------------------------

# Destruction primitives at command position (after start or a
# separator); sudo prefix allowed. Includes in-place edit flags,
# which rewrite files outside the edit-approval path.
DEST = (r'(?:^|[;&|(]+\s*)(?:sudo\s+)?(rm|shred|wipe)\b'
        r'|\bfind\b[^;&|]*-delete\b'
        r'|\bdd\b[^;&|]*\bof='
        r'|\bmkfs\b|\btruncate\b'
        r'|\bsed\s+--?in-place\b|\bsed\s+-i\S*|\bperl\s+-[a-z]*i')

# Truncating redirection targets: `<fd>>`, `>|`, `&>` etc. The
# lookbehind `(?<!)` on `>` excludes the `>>` append form.
REDIR = r'(?<!>)(?:\d|&)?>\|?(?!>)\s*(\S+)'

# Commands whose last non-flag argument is the overwrite target.
OVERWRITERS = r'\b(mv|cp|ln|rsync|install)\b([^;&|]*)'


def blocked(c):
    """True if the command destroys or overwrites existing content."""
    if re.search(DEST, c):
        return True
    # Resolve targets relative to the project dir, following a
    # leading `cd` when the command starts with one.
    prj = os.environ.get('DEVIN_PROJECT_DIR', '.')
    m = re.search(r'(?:^|[;&|]+\s*)cd\s+(\S+)', c)
    base = m.group(1) if m else prj

    def exists(p):
        return os.path.isfile(os.path.join(base, p))

    if any(exists(t) for t in re.findall(REDIR, c)):
        return True
    for _, args in re.findall(OVERWRITERS, c):
        toks = [t for t in args.split() if not t.startswith('-')]
        if toks and exists(toks[-1]):
            return True
    for args in re.findall(r'\btee\b([^;&|]*)', c):
        toks = [t for t in args.split() if not t.startswith('-')]
        if '-a' not in args.split() and toks and exists(toks[-1]):
            return True
    return False


# ------------------------------------------------------------------
# Emit a block decision on a hit, silence otherwise
# ------------------------------------------------------------------

def main():
    c = json.load(sys.stdin).get('tool_input', {}).get('command', '')
    if '/tmp' in c:
        return
    if blocked(c):
        print(json.dumps({
            'decision': 'block',
            'reason': ('Blocked: the command destroys or overwrites '
                       'existing content outside the approved path '
                       '(agents/rules.md reserves deletion and '
                       'destructive ops for the user, and file edits '
                       'go through the edit tool inline diff). Hand '
                       'the command to the user or use the edit '
                       'tool. Commands touching /tmp are exempt '
                       '(agent scratch space).')}))


if __name__ == '__main__':
    main()
