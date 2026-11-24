#!/usr/bin/env python3
# Agent-generated.
"""Exercise skills-drift-check.py against fabricated repo layouts.

== Intent ==

The check is a three-way compare (missing / stale / orphaned);
each shape plus the silent cases gets a row, so a regression shows
as a diff line rather than a session that quietly stops checking.

== Method ==

Each case is (label, recipes, devin_skills, shared_skills,
expected): dicts of basename -> file content written under a temp
project dir (`recipes/<n>.md`, `.devin/skills/<n>/SKILL.md`, and
`skills/<n>/SKILL.md` for the workflows repo's own layout); the
hook runs as a subprocess with DEVIN_PROJECT_DIR pointed at it and
an empty JSON payload on stdin, exactly as the dispatcher invokes
it. Expected is 'remind' or 'silent': a JSON `hookSpecificOutput`
object on stdout counts as remind, empty stdout as silent.

== Caveats ==

- Tests the check, not the wiring: run-event.py dispatch and the
  hooks.json matcher are exercised separately.
- Helpers build recipe text in house shape (title, mark line,
  intro); the quote helper mirrors generate-skills' escaping.

Usage: test-skills-drift-check.py   (exit 1 on any mismatch)
"""

import json
import os
import subprocess
import sys
import tempfile

# ------------------------------------------------------------------
# Fixtures: house-shaped recipe and wrapper text
# ------------------------------------------------------------------

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    os.pardir, 'skills-drift-check.py')

INTRO = 'Do the thing carefully.'
QUOTED = 'Verify the "fresh Ubuntu" claim.'


def recipe(intro=INTRO, mark=True):
    mark_line = 'Agent-generated.\n' if mark else ''
    return f'# T\n\n{mark_line}{intro}\nRest of the paragraph.\n'


def skill(desc=INTRO, generated=True):
    g = 'generated: true\n' if generated else ''
    return f'---\nname: x\ndescription: {desc}\n{g}---\n\nbody\n'


def esc(s):
    """generate-skills' double-quoted scalar form of s."""
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def index(*names):
    """A recipes/README.md: index rows linking each given name."""
    rows = ''.join(f'| [{n}.md]({n}.md) | x |\n' for n in names)
    return '# Recipes index\n\n| File | Contents |\n|---|---|\n' \
        + rows


# (label, recipes, .devin/skills, skills/, expected)
CASES = [
    # No recipes dir: duty is conditional, stays silent.
    ('no recipes dir', {}, {}, {}, 'silent'),
    # Recipe with no wrapper at all.
    ('no .devin dir', {'a': recipe()}, {}, {}, 'remind'),
    # In-sync pair, plain scalar.
    ('synced plain', {'a': recipe()}, {'a': skill()}, {}, 'silent'),
    # In-sync pair where the generator had to quote the sentence.
    ('synced quoted', {'a': recipe(QUOTED)},
     {'a': skill(esc(QUOTED))}, {}, 'silent'),
    # Recipe intro moved on after the wrapper was generated.
    ('stale description', {'a': recipe('Do it differently now.')},
     {'a': skill()}, {}, 'remind'),
    # Recipe without a mark line still extracts its intro.
    ('markless recipe', {'a': recipe(mark=False)},
     {'a': skill()}, {}, 'silent'),
    # Generated wrapper whose recipe was deleted.
    ('orphaned wrapper', {}, {'a': skill()}, {}, 'remind'),
    # Hand-authored wrapper without a recipe is never flagged.
    ('hand-authored', {}, {'a': skill(generated=False)}, {},
     'silent'),
    # A `generated: true` string inside the body (e.g. a fenced
    # frontmatter example) does not mark the wrapper generated.
    ('mark in body only', {},
     {'a': skill(generated=False)
      + 'wrappers carry `generated: true`:\n\ngenerated: true\n'},
     {}, 'silent'),
    # One of two recipes lacks a wrapper.
    ('one missing', {'a': recipe(), 'b': recipe()},
     {'a': skill()}, {}, 'remind'),
    # Wrapper dir without SKILL.md counts as missing.
    ('empty wrapper dir', {'a': recipe()}, {'b': ''}, {}, 'remind'),
    # README.md is the index, never a recipe: alone it stays silent.
    ('README not a recipe', {'README': index()}, {}, {}, 'silent'),
    # Index present and covering every recipe.
    ('index synced', {'a': recipe(), 'README': index('a')},
     {'a': skill()}, {}, 'silent'),
    # Recipe without an index row.
    ('index row missing', {'a': recipe(), 'b': recipe(),
                           'README': index('a')},
     {'a': skill(), 'b': skill()}, {}, 'remind'),
    # Index row naming a file that no longer exists.
    ('index stale row', {'a': recipe(), 'README': index('a', 'b')},
     {'a': skill()}, {}, 'remind'),
    # Workflows-repo layout: shared wrappers live at skills/.
    ('workflows layout', {'a': recipe()}, {}, {'a': skill()},
     'silent'),
    # Same layout, a recipe missing its shared wrapper still flags.
    ('workflows missing', {'a': recipe(), 'b': recipe()}, {},
     {'a': skill()}, 'remind'),
]


# ------------------------------------------------------------------
# Run each case through the hook, report mismatches
# ------------------------------------------------------------------

def put(proj, root, name, text):
    path = os.path.join(proj, root, name, 'SKILL.md')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if text != '':
        open(path, 'w', encoding='utf-8').write(text)


def verdict(recipes, devin_skills, shared_skills):
    with tempfile.TemporaryDirectory() as proj:
        for name, text in recipes.items():
            path = os.path.join(proj, 'recipes', name + '.md')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w', encoding='utf-8').write(text)
        for name, text in devin_skills.items():
            put(proj, os.path.join('.devin', 'skills'), name, text)
        for name, text in shared_skills.items():
            put(proj, 'skills', name, text)
        env = dict(os.environ, DEVIN_PROJECT_DIR=proj)
        out = subprocess.run(['python3', HOOK], input='{}',
                             capture_output=True, text=True,
                             env=env).stdout.strip()
    if not out:
        return 'silent'
    try:
        return 'remind' if 'hookSpecificOutput' in json.loads(out) \
            else 'error'
    except json.JSONDecodeError:
        return 'error'


def main():
    fails = 0
    for label, recipes, devin, shared, want in CASES:
        got = verdict(recipes, devin, shared)
        mark = 'ok  ' if got == want else 'FAIL'
        if got != want:
            fails += 1
        print(f'{mark} want={want:6} got={got:6}  {label}')
    print(f'\n{len(CASES)} cases, {fails} failure(s)')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
