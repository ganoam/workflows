# Linux tricks

Agent-generated.

## /dev/pts: pty slave nodes

devpts is the virtual filesystem behind pseudo-terminals.
Opening `/dev/ptmx` allocates a pty pair: master on the returned fd, slave node at `/dev/pts/<n>`.
Every interactive session owns one: shells, ssh, tmux panes, `script`, `expect`.

```shell
tty              # your shell's slave node, e.g. /dev/pts/3
ls -l /dev/pts   # one node per live pty, plus ptmx
ps -t pts/3      # processes on that terminal
```

devpts instances are per-userns: a container bind-mounting the host's `/dev/pts` sees its nodes but cannot allocate from it (`EACCES` on `/dev/ptmx`).

## /dev/shm: POSIX shared memory as files

tmpfs at `/dev/shm` where `shm_open()` objects appear as plain files: memory pages, no disk.
Used for zero-copy IPC by browsers (chromium/QtWebEngine renderers), PipeWire/PulseAudio, some databases.

```shell
ls /dev/shm    # live shm objects
df -h /dev/shm # tmpfs size (default: half of RAM)
```

Containers without a real mount leave an empty placeholder dir; apps that statfs or size-check shm misbehave on it: mount a tmpfs (`bwrap --tmpfs /dev/shm`, docker's `--shm-size`).
