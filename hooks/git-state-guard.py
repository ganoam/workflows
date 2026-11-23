#!/usr/bin/env python3
# Agent-generated; human reviewed.
r"""Block state-changing git commands at PreToolUse.

== Intent ==

agents/rules.md reserves repository state and refs for the user:
the agent never commits, pushes, checks out, fetches, rebases,
tags, branches, or otherwise moves the repo. Read-only git
(status, log, diff, queries) stays allowed. The hook makes the
rule mechanical instead of recall-based.

== Method ==

Reads the hook event JSON on stdin, extracts `tool_input.command`,
and scans it for git invocations. Two checks:

  1. Directly mutating verbs (RW list: commit, push, checkout,
     fetch, pull, reset, merge, clone, ...).
  2. Sub-command verbs (SUB list): stash/branch/tag/remote/config/
     reflog/submodule/worktree, judged per sub-command against a
     read-only allow-list (e.g. `stash list` passes, `stash` writes
     are blocked; `branch -v` passes, `branch foo` is blocked).

The anchor `(?:^|[;&|(]+\s*)` keeps `echo 'git commit'` and similar
quoted mentions from firing.

== Caveats ==

- Commands mentioning /tmp are exempt entirely: rules.md grants the
  agent git experiments in its own /tmp scratch dirs.
- `config` walks its full argument tail: flags are skipped together
  with the arguments they take, so a write cannot hide behind a
  value-consuming flag (`--default x --add key val` still blocks).
  Unknown flag shapes over-block reads rather than pass writes.
- Stricter than a minimal reading: fetch/pull are blocked because
  they move remote-tracking refs, and refs belong to the user.

Usage: invoked by hooks.json (PreToolUse, matcher ^exec$); stdin is
the hook event JSON. Blocked commands emit {"decision": "block"}.
"""

import json
import re
import sys

# ------------------------------------------------------------------
# Command classification
# ------------------------------------------------------------------

# git invocation prefix: command start (or after a separator), then
# any mix of global options and their values before the verb.
G = r'(?:^|[;&|(]+\s*)git(?:\s+(?:-{1,2}[\w-]+(?:=\S+)?)(?:\s+\S+)?)*\s+'

# Verbs that always mutate repo state or refs.
RW = (r'(add|am|apply|bisect|checkout|cherry-pick|clean|clone|commit|'
      r'fetch|init|merge|mv|pull|push|rebase|reset|restore|revert|rm|'
      r'switch|update-index)\b')

# Verbs whose read/write nature depends on the sub-command
# (config is not here; its flags take a varying number of
# arguments, so a fixed capture window cannot judge it).
# The capture excludes shell separators: a plain \S+ would glue
# a trailing `;` onto the token (`branch --list;` is a read).
SUB = (r'(stash|branch|tag|remote|reflog|submodule|worktree)'
       r'(?:\s+([^\s;&|()]+))?')

# `config` gets its own match carrying the whole argument tail:
# some of its flags take an argument and some take none, so the
# key/value boundary can only be found by walking the tokens.
CFG = r'config\b([^;&|]*)'

# Read-only sub-commands per verb: branch/tag/remote/etc. with no
# argument or with a listed flag stay allowed.
RO = {
    'stash': {'list', 'show'},
    'reflog': {None, 'show'},
    'submodule': {None, 'status'},
    'worktree': {'list'},
    'remote': {None, '-v', '--verbose', 'show', 'get-url'},
    'branch': {None, '-l', '--list', '-v', '-vv', '-a', '-r',
               '--show-current', '--contains', '--merged',
               '--no-merged', '--points-at'},
    'tag': {None, '-l', '--list', '-n', '--contains', '--points-at',
            '--merged', '--sort', '--format'},
}

# `config` read verbs: reaching one settles the call as a read.
CFG_RO = {'-l', '--list', '--get', '--get-all', '--get-regexp',
          '--show-scope', '--show-origin', '--name-only'}

# `config` flags that take one argument: file selectors and
# value-taking modifiers. Neither read nor write themselves; the
# verdict waits for the token after the argument.
CFG_SKIP = {'-f', '--file', '--blob', '--type', '--default',
            '--value', '--fixed-value'}

# `config` flags that take no argument: scope selectors and
# modifiers, consumed, judgment moves to the next token.
CFG_SKIP0 = {'--local', '--global', '--system', '--worktree',
             '--includes', '--no-includes', '--null', '-z'}


def config_write(tail):
    """True if a `git config` argument tail writes config.

    Walks the tokens: read verbs settle it as a read, flags are
    skipped together with the arguments they take, the first bare
    token is the key (a read when nothing follows), the second bare
    token is the value (a write). Any other flag shape blocks,
    since unknown write flags cannot be distinguished.
    """
    toks = tail.split()
    i = 0
    seen_key = False
    while i < len(toks):
        t = toks[i]
        if t in CFG_RO:
            return False                     # a read verb settles it
        if t in CFG_SKIP:
            i += 2                           # flag plus its argument
            continue
        if t in CFG_SKIP0:
            i += 1                           # flag alone
            continue
        if t.startswith('-'):
            return True                      # unknown flag -> block
        if seen_key:
            return True                      # second bare token -> value -> write
        seen_key = True
        i += 1
    return False                             # key alone (or nothing) -> read


def blocked(c):
    """True if the command contains a state-changing git invocation."""
    sub = re.search(G + SUB, c)          # finds stash/branch/tag/remote/reflog/submodule/worktree
    cfg = re.search(G + CFG, c)          # finds git config, carrying its arg tail
    bad = bool(re.search(G + RW, c))     # finds commit/push/checkout/fetch/... (always mutating)

    if not bad and cfg:                  # no direct verb, but a config call: walk its args
        bad = config_write(cfg.group(1))
    if not bad and sub:                  # still clean: judge the sub-verb against its read-only list
        bad = sub.group(2) not in RO[sub.group(1)]
    return bad


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
            'reason': ('Blocked: agents never change repository state '
                       'or refs (agents/rules.md). Read-only git is '
                       'allowed; hand state-changing commands to the '
                       'user. Commands touching /tmp are exempt (agent '
                       'scratch space).')}))


if __name__ == '__main__':
    main()
