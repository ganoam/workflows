#!/usr/bin/env python3
"""Exercise git-state-guard.py against a table of command cases.

== Intent ==

The guard's classification logic is regex- and token-walk-based and
has shipped at least one real bypass (a write hiding behind a
value-taking config flag). A case table keeps the expected verdict
for every shape that has ever been decided, so a regression shows
as a diff line, not a silent hole.

== Method ==

Each case is (command, expected) where expected is 'block' or
'pass'. The hook is invoked as a subprocess exactly as the
dispatcher invokes it: the same JSON payload shape on stdin, the
verdict read off stdout. A 'block' verdict is recognized by a
`"decision": "block"` object; anything else (including silence)
counts as pass.

== Caveats ==

- Tests the classification, not the wiring: run-event.py dispatch
  and the hooks.json resolver are exercised separately.
- /tmp cases pass `cd`-style commands through DEVIN_PROJECT_DIR
  like the hook sees them; the exemption is on the command text.

Usage: test-git-state-guard.py   (exit 1 on any mismatch)
"""

import json
import os
import subprocess
import sys

# ------------------------------------------------------------------
# Case table: command -> expected verdict.
# Keep shapes that were ever decided or ever went wrong.
# ------------------------------------------------------------------

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    os.pardir, 'git-state-guard.py')

CASES = [
    # Directly mutating verbs: always block.
    ('git commit -m x', 'block'),
    ('git push', 'block'),
    ('git checkout -b x', 'block'),
    ('git fetch', 'block'),
    ('git pull', 'block'),
    ('git merge b', 'block'),
    ('git clone u', 'block'),
    ('git init', 'block'),
    ('git submodule update', 'block'),
    ('git tag v1', 'block'),
    ('git branch new', 'block'),
    ('git stash', 'block'),
    ('git stash pop', 'block'),
    ('git remote add o u', 'block'),
    ('git worktree add w', 'block'),
    ('git rebase main', 'block'),
    ('git rebase -i main', 'block'),
    ('git reset --hard', 'block'),
    ('git restore f', 'block'),
    ('git revert c', 'block'),
    ('git switch x', 'block'),
    ('git clean -fd', 'block'),
    # Read-only forms: pass.
    ('git status', 'pass'),
    ('git log --oneline', 'pass'),
    ('git diff HEAD', 'pass'),
    ('git show c', 'pass'),
    ('git stash list', 'pass'),
    ('git branch -v', 'pass'),
    ('git tag -l', 'pass'),
    ('git remote -v', 'pass'),
    ('git remote show o', 'pass'),
    ('git reflog', 'pass'),
    ('git reflog show', 'pass'),
    ('git submodule status', 'pass'),
    ('git worktree list', 'pass'),
    # config: reads pass, writes block, and a write cannot hide
    # behind flags that take arguments.
    ('git config', 'pass'),
    ('git config user.name', 'pass'),
    ('git config -l', 'pass'),
    ('git config --get user.name', 'pass'),
    ('git config --global user.name', 'pass'),
    ('git config --global -l', 'pass'),
    ('git config -f alt.conf user.name', 'pass'),
    ('git config --type bool user.name', 'pass'),
    ('git config --includes --get user.name', 'pass'),
    ('git config --default x user.name', 'pass'),
    ('git config user.name x', 'block'),
    ('git config user.name x y z', 'block'),
    ('git config --global user.email x@y', 'block'),
    ('git config --local key val', 'block'),
    ('git config -f alt.conf key val', 'block'),
    ('git config --type bool key val', 'block'),
    ('git config --default false --add user.x y', 'block'),
    ('git config --unset x', 'block'),
    ('git config --global --worktree user.name x', 'block'),
    ('git -C repo config user.name x', 'block'),
    # /tmp is agent scratch space: exempt entirely.
    ('git -C /tmp/x commit -m y', 'pass'),
    ('cd /tmp/x && git init', 'pass'),
    # Non-git commands and quoted mentions never fire.
    ('ls -la', 'pass'),
    ('echo "git commit"', 'pass'),
    ('gh pr view 1', 'pass'),
]


# ------------------------------------------------------------------
# Run each case through the hook, report mismatches
# ------------------------------------------------------------------

def verdict(cmd):
    payload = json.dumps({'tool_input': {'command': cmd}})
    out = subprocess.run(['python3', HOOK], input=payload,
                         capture_output=True, text=True).stdout.strip()
    if not out:
        return 'pass'
    try:
        return 'block' if json.loads(out).get('decision') == 'block' \
            else 'pass'
    except json.JSONDecodeError:
        return 'error'


def main():
    fails = 0
    for cmd, want in CASES:
        got = verdict(cmd)
        mark = 'ok  ' if got == want else 'FAIL'
        if got != want:
            fails += 1
        print(f'{mark} want={want:5} got={got:5}  {cmd}')
    print(f'\n{len(CASES)} cases, {fails} failure(s)')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
