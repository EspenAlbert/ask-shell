# run_and_wait

<!-- === DO_NOT_EDIT: pkg-ext run_and_wait_def === -->
## function: run_and_wait
- [source](../../ask_shell/_internal/_run.py#L486)
> **Since:** 0.3.0

```python
def run_and_wait(script: ShellConfig | str, timeout: float | None = None, *, allow_non_zero_exit: bool | None = None, ansi_content: bool | None = None, attempts: int | None = None, cwd: str | Path | None = None, env: dict[str, str] | None = None, extra_popen_kwargs: dict | None = None, is_binary_call: bool | None = None, message_callbacks: list[Callable[[ask_shell._internal.events.ShellRunBefore | ask_shell._internal.events.ShellRunPOpenStarted | ask_shell._internal.events.ShellRunStdStarted | ask_shell._internal.events.ShellRunStdReadError | ask_shell._internal.events.ShellRunStdOutput | ask_shell._internal.events.ShellRunRetryAttempt | ask_shell._internal.events.ShellRunAfter], bool]] | None = None, print_prefix: str | None = None, run_log_stem_prefix: str | None = None, run_output_dir: Path | None = None, settings: AskShellSettings | None = None, should_retry: Callable[[<class 'ask_shell._internal.models.ShellRun'>], bool] | None = None, skip_binary_check: bool | None = None, skip_progress_output: bool | None = None, skip_html_log_files: bool | None = None, include_log_time: bool | None = None, skip_os_env: bool | None = None, user_input: bool | None = None, terminal_width: int | None = None, skip_interactive_check: bool | None = None) -> ShellRun:
    ...
```
<!-- === OK_EDIT: pkg-ext run_and_wait_def === -->

<!-- === DO_NOT_EDIT: pkg-ext run_and_wait_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | param 'message_callbacks' type: list[Callable[[typing.Union[ask_shell._internal.events.ShellRunBefore, ask_shell._internal.events.ShellRunPOpenStarted, ask_shell._internal.events.ShellRunStdStarted, ask_shell._internal.events.ShellRunStdReadError, ask_shell._internal.events.ShellRunStdOutput, ask_shell._internal.events.ShellRunRetryAttempt, ask_shell._internal.events.ShellRunAfter]], bool]] | None -> list[Callable[[ask_shell._internal.events.ShellRunBefore | ask_shell._internal.events.ShellRunPOpenStarted | ask_shell._internal.events.ShellRunStdStarted | ask_shell._internal.events.ShellRunStdReadError | ask_shell._internal.events.ShellRunStdOutput | ask_shell._internal.events.ShellRunRetryAttempt | ask_shell._internal.events.ShellRunAfter], bool]] | None |
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext run_and_wait_changes === -->