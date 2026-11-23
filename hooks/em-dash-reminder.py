#!/usr/bin/env python3
# Agent-generated; human reviewed.
"""Remind about the no-em-dashes prose rule when an edit introduces one.

== Intent ==

MdStyle.md forbids em/en-dashes in prose, comments, and generated
text; the rule is binding but was skipped in practice, so the
post-edit hook surfaces it mechanically at the point of change.

== Method ==

Reads the hook event JSON on stdin, extracts the text the tool just
applied (edit: `new_string`, write: `content`), and counts unicode
dashes (em, en, horizontal bar) plus the spaced ASCII surrogate
` -- `. The surrogate only counts where it reads as prose: anywhere
in document files (`.md`/`.rst`/`.adoc`/`.txt` and doc-named files),
and inside comments (`#`, `//`) elsewhere, so `--flag`, `x--`, and
the `--` end-of-options marker in code never trip it. Any hit
prints a `hookSpecificOutput.additionalContext` reminder naming the
rule and the allowed replacements. Checking applied text rather
than blocking keeps the check cheap and leaves justified deviations
to the reviewer.

== Caveats ==

- A reminder, not a gate: MdStyle.md permits justified deviation
  (verbatim quotes, upstream material).
- Unspaced `--` is never flagged: CLI flags, decrements, and ranges
  are legitimate in code and CLI text.
- The comment-part test is a first-`#`/`//` scan, not a lexer:
  leaders inside strings can misattribute code as comment.
- Doc files are checked wholesale: a `--` inside a fenced code
  example still draws the reminder.
- Notebook edits and exec-side writes sit outside the matcher.

Usage: invoked by hooks.json (PostToolUse, matcher edit|write);
stdin is the hook event JSON.
"""

import json
import os
import sys

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

DASHES = '—–―'      # em-dash, en-dash, horizontal bar
SURROGATE = ' -- '  # spaced ASCII stand-in for an em-dash
DOC_EXT = {'.md', '.markdown', '.rst', '.adoc', '.asciidoc', '.txt'}
DOC_NAMES = {'readme', 'changelog', 'devlog', 'backlog', 'roadmap',
             'todo', 'notes', 'agents'}
COMMENT_LEADERS = ('#', '//')


# ------------------------------------------------------------------
# Scope: the surrogate counts as prose in doc files, inside comments
# elsewhere.
# ------------------------------------------------------------------

def is_doc(path):
    stem, ext = os.path.splitext(os.path.basename(path).lower())
    return ext in DOC_EXT or stem in DOC_NAMES


def comment_part(line):
    """Text from the first comment leader, '' when the line has none."""
    idx = min((line.find(c) for c in COMMENT_LEADERS if line.find(c) >= 0),
              default=-1)
    return line[idx:] if idx >= 0 else ''


def surrogates(text, doc):
    # spaced-surrogate hits: whole lines in docs, comment parts elsewhere
    if doc:
        return text.count(SURROGATE)
    return sum(comment_part(l).count(SURROGATE) for l in text.splitlines())


# ------------------------------------------------------------------
# Check: count dashes in the applied text, remind on any hit
# ------------------------------------------------------------------

def main():
    data = json.load(sys.stdin)
    ti = data.get('tool_input', {})
    # edit carries `new_string`, write carries `content`; the hook
    # only inspects what was added, never the surrounding file.
    text = ti.get('new_string') or ti.get('content') or ''
    n = sum(text.count(d) for d in DASHES)
    n += surrogates(text, is_doc(ti.get('file_path') or ''))
    if n:
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PostToolUse',
            'additionalContext': (
                f'{n} em/en-dash(es) or " -- " surrogate(s) in the '
                'applied text. MdStyle.md forbids them in prose, '
                'comments, and generated text: use a comma, colon, '
                'period, or parentheses instead. Justified deviations '
                '(verbatim quotes, upstream material) may stay if '
                'stated.')}}))


if __name__ == '__main__':
    main()
