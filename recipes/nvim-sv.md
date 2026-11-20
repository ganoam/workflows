# nvim setup for SystemVerilog work

Editor setup for SystemVerilog projects: LazyVerilog LSP for semantic diagnostics, plus `nvim-lint`'s `fusesoc_verilator` for lint on save.
Written against the owner's layout: `gen_flist.py` lives in `deps/scripts` and `vim.g.fusesoc_target` is the per-repo hook, adapt both per machine.

## LazyVerilog

### lazyverilog.toml (required)

The server walks up from each file to the nearest `lazyverilog.toml`.
No toml means no filelist and no incdirs: lint and compilation stay off and `` `include "uvm_macros.svh" `` / `` `include "dv_macros.svh" `` resolve nowhere, silently.

```toml
[design]
vcode = "vcode.f"          # filelist, relative to this toml

[lint]
enable = true

[format]
enable_format_on_save = true
```

- `[compilation].background_compilation` defaults **false**: no semantic diagnostics unless enabled.
- The plugin sends no `root_dir`/`root_markers`: don't add any.

### Generate vcode.f

```shell
~/workspaceconfig/deps/scripts/bin/gen_flist.py --target=sim toplevels.list > vcode.f
```

`toplevels.list` is one core VLNV per line (`ganoam:dv:stream_reg_sim:0.1`).
The script emits absolute paths plus `+incdir+` lines for UVM/dv headers.
`--cores-root` defaults `.` (repeat for sibling repos) and does not read `~/.config/fusesoc/fusesoc.conf`.

`include` resolves via `+incdir+` only: listing a header as a file doesn't make it includable.

### Debugging

```vim
:LspInfo                     " client attached? (filetype must be systemverilog/verilog)
:LspRestart | :e             " toml created while server ran: misses are cached
:LspLog                      " server-side include/parse errors
:lua vim.print(vim.diagnostic.get(0))  " 'source' field: lazyverilog vs verilator
```

## nvim-lint: fusesoc_verilator

Runs on `BufWritePost` for verilog/systemverilog, in nvim's cwd:

```shell
fusesoc run --no-export --target=lint --setup --build <vim.g.fusesoc_target>
```

`vim.g.fusesoc_target` nil means fusesoc gets no core, hits a usage error, and produces zero diagnostics, silently.

### Set the target: <repo>/.nvim.lua

```lua
vim.g.fusesoc_target = "ganoam:dv:stream_reg_sim:0.1"
```

- **Quote the VLNV**: unquoted is a Lua syntax error and the file never sources.
- `exrc` is on; the file is sourced only when nvim *starts* with cwd at the repo root.
- A content change re-prompts for trust (`:trust`).

### The core needs a lint target

```yaml
targets:
  sim: &sim_target
    toplevel: tb
    filesets: [files_rtl, files_dv]
    default_tool: verilator
  lint:
    <<: *sim_target
```

### Verify

```shell
cd <repo> && fusesoc list-cores | grep ganoam:dv:stream_reg_sim
fusesoc run --no-export --target=lint --setup ganoam:dv:stream_reg_sim:0.1
```

### How output becomes diagnostics

- The linter finds `Entering directory '<build>'` in the output, then parses `*.sarif` there.
- Otherwise it falls back to the regex `%Error:`/`%Warning-CODE: file:lnum:col:` and keeps only lines matching the current buffer.
- `ignore_exitcode = true`: a nonzero exit on lint findings is normal.
- `vim.notify(output)` dumps the full fusesoc output every save: debug spam, remove if annoying.
