<!--
description: Mount a dynamic Rich renderable in ask-shell's live region with add_renderable, plus an apply-live demo with CI heartbeats
-->
# add_renderable

`add_renderable` mounts any [Rich renderable](https://rich.readthedocs.io/en/stable/protocol.html) inside ask-shell's global `Live` region and returns a `RemoveLivePart` callable to detach it. Use it for status that should stay pinned while shell runs progress, instead of [`print_to_live`](../../console/index.md#print_to_live_def) (which lives in scrollback) or [`new_task`](../../console/index.md#new_task_def) (which renders a `rich.progress.Progress` bar).

The live region is a sorted `Group` of all attached parts. Each part has a `name` (used for stable sort and removal) and an `order` (vertical placement; shell-run progress uses `-100`, so any non-negative `order` stays below it).

## Dynamic renderable via `__rich_console__`

The cheapest way to get live updates is to implement [`__rich_console__`](https://rich.readthedocs.io/en/stable/protocol.html#console-render) on a small class that reads mutable state. Rich's auto-refresh thread re-invokes the method ~4 times per second while the live region is up, so updates from any thread show without calling a refresh helper yourself.

```python
from io import StringIO

from rich.console import Console
from rich.text import Text


class JobStatus:
    def __init__(self) -> None:
        self.done = 0
        self.in_flight = 0
        self.elapsed_s = 0.0

    def __rich_console__(self, console, options):
        yield Text(f"refresh: {self.done} complete, {self.in_flight} in progress ({self.elapsed_s:.0f}s)")


status = JobStatus()
status.done = 5
status.in_flight = 3
status.elapsed_s = 12.0

probe = Console(file=StringIO(), width=80, color_system=None, legacy_windows=False)
probe.print(status)
print(probe.file.getvalue().strip())
#> refresh: 5 complete, 3 in progress (12s)
```

The example renders against a captured console so it can be tested without a real terminal. In production code you would pass the same instance to `add_renderable` (see below).

## Wiring it into the live region

Pass the instance once, then mutate its fields from any thread. The 4 Hz auto-refresh picks up the new state. Always release the part in a `finally` so a crash does not leave the live region pinned.

```python test="skip"
from ask_shell.console import add_renderable


class JobStatus: ...  # as above


status = JobStatus()
remove = add_renderable(status, name="job-status", order=10)
try:
    # mutate status.done / status.in_flight from your event loop;
    # Rich re-renders automatically on its 4 Hz tick
    ...
finally:
    remove(print_after_removing=True)
```

`remove(print_after_removing=True)` flushes one final render into scrollback before detaching, which is useful for converting a transient status into a permanent log entry.

## Apply-live demo (`terraform apply -json`)

The `apply-live` CLI demonstrates the same pattern tfdo uses for streaming Terraform output: a Typer app with [`configure_logging`](../../console/index.md#configure_logging_def), a shell run with `skip_progress_output=True`, and an NDJSON handler wired through `message_callbacks`.

The demo lives at `examples/apply_live/`:

- `workspace/` holds four chained `time_sleep` resources (`create_duration = "5s"`, each depends on the previous). A fresh `terraform apply -json -auto-approve` takes ~20s as resources are created one after another.
- The CLI always runs `terraform init -input=false` first so a clean checkout works in CI without a separate init step.
- Re-run after the first apply is a no-op and finishes quickly. Run `terraform destroy -auto-approve` in `workspace/` to reset state.

Run from the ask-shell repo (`code/ask-shell/`):

```sh
just apply-live
```

Locally you should see a pinned `refresh · N done · M running · …` line above the shell progress row. In CI the panel is invisible; the handler emits `logger.info` heartbeats every five seconds instead:

```sh
CI=true just apply-live
```

The handler is a minimal copy of tfdo's plan stream path (no tfdo import):

```python test="skip"
from pathlib import Path

from ask_shell.shell import run_and_wait
from apply_live.stream_handler import PlanStreamHandler, plan_stream_callback

handler = PlanStreamHandler()
callback = plan_stream_callback(handler)
workspace = Path("code/ask-shell/examples/apply_live/workspace")
run = run_and_wait(
    "terraform apply -json -auto-approve",
    cwd=workspace,
    allow_non_zero_exit=True,
    skip_progress_output=True,
    message_callbacks=[callback],
)
handler.flush()
print(run.exit_code)
#> 0
```

## When to pick which API

- **`add_renderable`**: dynamic status that must stay visible while shell commands and tasks update. Disappears with the live region when no parts remain (`transient=True`).
- **`print_to_live` / `log_to_live`**: one-shot lines that belong in scrollback (warnings, phase changes, diagnostics).
- **`new_task`**: discrete units of work with a progress bar, elapsed timer, and an automatic `INFO` log on completion.

Mixing them is normal. A typical pattern keeps a `add_renderable` panel for live counters, calls `print_to_live` once per diagnostic, and lets ask-shell's own `_RunState` manage the per-process `new_task`.

## CI and non-TTY rendering

[`interactive_shell()`](../../console/index.md#interactive_shell_def) returns `False` when any of these are true:

- `CI=true` in the environment.
- `TERM` is `dumb` or `unknown`.
- `stdout` is not a TTY.
- The process runs under pytest.
- The process runs inside a container.

When the console is not interactive, Rich's `Live.process_renderables` does not append the live render and `Live.refresh` is a no-op on non-terminals. That means **`add_renderable` content is invisible in CI logs**. What still reaches the log stream:

- `print_to_live(...)` and `log_to_live(...)` write through `console.print()` directly to stdout, no live overlay involved.
- `logger.info(...)` wired by `configure_logging(...)` emits through `RichHandler` onto the same console.
- `new_task` completion: `log_task_done` calls `logger.info`, so the `Running: '...' completed in Ns` line appears even in CI.

### Avoiding frozen GitHub Actions logs

GitHub Actions streams a step's log by line. A long shell command whose only signal is an `add_renderable` panel produces no stdout, so the step appears stalled until it exits. Mitigations, in order of impact:

- **Set `PYTHONUNBUFFERED=1`** in the workflow `env`. Without it, Python falls back to block buffering when stdout is not a TTY and short bursts of output may sit in the buffer for minutes.
- **Terminal width in CI**: when `interactive_shell()` is false, ask-shell uses `ASK_SHELL_TERMINAL_WIDTH` and `ASK_SHELL_TERMINAL_HEIGHT` (defaults `120` and `40`) for the shared Rich console. Rich ignores a lone `width`; both must be set.
- **Mirror the dynamic state into `print_to_live` or `logger.info`** on a heartbeat (every few seconds). The renderable still drives the local UX; the heartbeat keeps the CI stream alive. The apply-live demo uses `logger.info("refresh: N complete, M in progress (…)")` when `interactive_shell()` is false.
- **Set `log_updates=True` on `new_task`** when you want every `task.update(...)` call to emit a log line.
- **Set `include_log_time=True` on `ShellConfig`** so each captured shell line carries a `[hh:mm:ss]` prefix. Stalls become easier to spot in CI output.
- **Pass `skip_progress_output=True` to `run_and_wait`** for verbose commands like `terraform plan -json`. The shell-run progress collapses to `"..."`, which keeps the live region short on local runs and stops Rich's cursor positioning from drifting out of the viewport.

To reproduce CI semantics locally without pushing a workflow: `CI=true just apply-live` from `code/ask-shell/`. `interactive_shell()` flips to `False` and the rendering path matches the GitHub runner.
