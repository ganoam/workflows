#!/usr/bin/env python3
# Agent-generated.
"""Exercise em-dash-reminder.py against a table of edit cases.

== Intent ==

The unicode-dash check is trivial; the spaced `--` surrogate check
is the part with real scope decisions (doc files checked wholesale,
comment parts elsewhere). A case table pins down which shapes
remind and which stay silent, so a regression shows as a diff
line, not a silent hole.

== Method ==

Each case is (file_path, key, text, expected): the hook is invoked
as a subprocess exactly as the dispatcher invokes it, with the
same JSON payload shape on stdin (`key` is `new_string` for edits,
`content` for writes; `file_path` is omitted when None). Expected
is 'remind' or 'silent': a JSON `hookSpecificOutput` object on
stdout counts as remind, empty stdout as silent.

== Caveats ==

- Tests the check, not the wiring: run-event.py dispatch and the
  hooks.json matcher are exercised separately.
- The doc/comment heuristics are approximations by design; the
  table encodes the accepted false-positive shapes (e.g. `--` in a
  doc-file code snippet still reminds).

Usage: test-em-dash-reminder.py   (exit 1 on any mismatch)
"""

import json
import os
import subprocess
import sys

# ------------------------------------------------------------------
# Case table: (file_path, payload key, applied text) -> expected.
# Keep shapes that were ever decided or ever went wrong.
# ------------------------------------------------------------------

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    os.pardir, 'em-dash-reminder.py')

CASES = [
    # Unicode dashes remind in any file type, code included.
    ('x.md', 'new_string', 'an em-dash — in prose', 'remind'),
    ('x.sh', 'new_string', 'echo "–"', 'remind'),
    ('x.py', 'new_string', '# en-dash – in comment', 'remind'),
    # Doc files: the spaced surrogate reminds wholesale, even inside
    # what looks like a code snippet (accepted false positive).
    ('DEVLOG.md', 'new_string', 'corrected -- it never pushes', 'remind'),
    ('notes.txt', 'new_string', 'word -- aside', 'remind'),
    ('x.rst', 'new_string', 'word -- aside', 'remind'),
    ('README', 'new_string', 'text -- aside', 'remind'),
    ('x.md', 'new_string', 'run: git checkout -- f', 'remind'),
    # Unspaced '--' never flags, even in docs.
    ('x.md', 'new_string', 'flags --dry-run and 1.0--2.0', 'silent'),
    # Code files: surrogate reminds only inside a comment.
    ('x.sh', 'new_string', '# must sit on it -- see the guard', 'remind'),
    ('x.sh', 'new_string', 'git checkout -- file', 'silent'),
    ('x.sh', 'new_string', 'grep -- "$pat" f  # end-of-options ok', 'silent'),
    ('x.c', 'new_string', '// note -- aside', 'remind'),
    ('x.c', 'new_string', 'printf("a -- b")', 'silent'),
    ('x.py', 'new_string', 's = "a -- b"', 'silent'),
    # Extensionless files take the comment rule (scripts are code).
    ('backlight', 'new_string', '# note -- aside', 'remind'),
    ('backlight', 'new_string', 'volume --toggle', 'silent'),
    # No file_path falls back to the comment rule.
    (None, 'new_string', 'prose -- aside', 'silent'),
    # Writes carry `content`; same check applies.
    ('x.md', 'content', 'para -- aside', 'remind'),
    ('x.sh', 'content', 'git checkout -- f', 'silent'),
    # Clean text stays silent.
    ('x.md', 'new_string', 'a plain change, no dashes', 'silent'),
]


# ------------------------------------------------------------------
# Run each case through the hook, report mismatches
# ------------------------------------------------------------------

def verdict(path, key, text):
    ti = {key: text}
    if path is not None:
        ti['file_path'] = path
    payload = json.dumps({'tool_input': ti})
    out = subprocess.run(['python3', HOOK], input=payload,
                         capture_output=True, text=True).stdout.strip()
    if not out:
        return 'silent'
    try:
        return 'remind' if 'hookSpecificOutput' in json.loads(out) \
            else 'error'
    except json.JSONDecodeError:
        return 'error'


def main():
    fails = 0
    for path, key, text, want in CASES:
        got = verdict(path, key, text)
        mark = 'ok  ' if got == want else 'FAIL'
        if got != want:
            fails += 1
        print(f'{mark} want={want:6} got={got:6}  {path}:{text[:40]}')
    print(f'\n{len(CASES)} cases, {fails} failure(s)')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
