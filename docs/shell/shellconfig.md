# ShellConfig

<!-- === DO_NOT_EDIT: pkg-ext shellconfig_def === -->
## class: ShellConfig
- [source](../../ask_shell/_internal/models.py#L127)
> **Since:** 0.3.0

```python
class ShellConfig(Entity):
    shell_input: str
    env: dict[str, str] = ...
    extra_popen_kwargs: dict = ...
    allow_non_zero_exit: bool = False
    skip_os_env: bool = False
    skip_binary_check: bool = False
    skip_interactive_check: bool = False
    cwd: Path = None
    user_input: bool = False
    attempts: int = 1
    should_retry: Callable[[<class 'ask_shell._internal.models.ShellRun'>], bool] = <function always_retry>
    print_prefix: str = None
    include_log_time: bool = False
    ansi_content: bool = None
    run_output_dir: Path | None = None
    run_log_stem_prefix: str = ''
    skip_html_log_files: bool = False
    skip_progress_output: bool = False
    terminal_width: int | None = 999
    is_binary_call: bool = None
    settings: AskShellSettings = ...
    message_callbacks: list[Callable[[typing.Union[ask_shell._internal.events.ShellRunBefore, ask_shell._internal.events.ShellRunPOpenStarted, ask_shell._internal.events.ShellRunStdStarted, ask_shell._internal.events.ShellRunStdReadError, ask_shell._internal.events.ShellRunStdOutput, ask_shell._internal.events.ShellRunRetryAttempt, ask_shell._internal.events.ShellRunAfter]], bool | None]] = ...
```

>>> ShellConfig("some_script").print_prefix
'some_script'
>>> ShellConfig("some_script some_arg").print_prefix
'some_script some_arg'
>>> ShellConfig("some_script some_arg --option1").print_prefix
'some_script some_arg'
>>> ShellConfig("some_script some_arg", cwd="/some/path/prefix").print_prefix
'prefix some_script some_arg'
>>> ShellConfig("some_script some_arg", cwd="/some/path/prefix", print_prefix="override").print_prefix
'override'
<!-- === OK_EDIT: pkg-ext shellconfig_def === -->

### Fields

| Field | Type | Default | Since | Description |
|---|---|---|---|---|
| shell_input | `str` | - | 0.3.0 | - |
| env | `dict[str, str]` | `...` | 0.3.0 | - |
| extra_popen_kwargs | `dict` | `...` | 0.3.0 | - |
| allow_non_zero_exit | `bool` | `False` | 0.3.0 | - |
| skip_os_env | `bool` | `False` | 0.3.0 | - |
| skip_binary_check | `bool` | `False` | 0.3.0 | - |
| skip_interactive_check | `bool` | `False` | 0.3.0 | - |
| cwd | `Path` | `None` | unreleased | Set to Path.cwd() if not provided |
| user_input | `bool` | `False` | 0.3.0 | - |
| attempts | `int` | `1` | 0.3.0 | - |
| should_retry | `Callable[[<class 'ask_shell._internal.models.ShellRun'>], bool]` | `<function always_retry>` | 0.3.0 | - |
| print_prefix | `str` | `None` | unreleased | Use cwd+binary_name+first_arg if not provided |
| include_log_time | `bool` | `False` | 0.3.0 | - |
| ansi_content | `bool` | `None` | unreleased | Inferred if not provided |
| run_output_dir | `Path | None` | `None` | unreleased | Directory to store run logs, defaults to settings.run_logs /{XX}_{self.exec_name} |
| run_log_stem_prefix | `str` | `''` | 0.3.0 | Prefix for run log stem |
| skip_html_log_files | `bool` | `False` | 0.3.0 | Skip HTML log files, by default dumps HTML logs to support viewing colored output in browsers |
| skip_progress_output | `bool` | `False` | 0.3.0 | Skip transitive std out/err output, useful for large outputs that are not needed in the logs when running parallel scripts |
| terminal_width | `int | None` | `999` | 0.3.0 | - |
| is_binary_call | `bool` | `None` | unreleased | Inferred if not provided |
| settings | `AskShellSettings` | `...` | 0.3.0 | - |
| message_callbacks | `list[Callable[[ask_shell._internal.events.ShellRunBefore | ask_shell._internal.events.ShellRunPOpenStarted | ask_shell._internal.events.ShellRunStdStarted | ask_shell._internal.events.ShellRunStdReadError | ask_shell._internal.events.ShellRunStdOutput | ask_shell._internal.events.ShellRunRetryAttempt | ask_shell._internal.events.ShellRunAfter], bool | None]]` | `...` | 0.3.0 | Callbacks for run messages, useful for custom handling of stdout/stderr |

<!-- === DO_NOT_EDIT: pkg-ext shellconfig_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | field 'print_prefix' default added: None |
| unreleased | field 'is_binary_call' default added: None |
| unreleased | field 'ansi_content' default added: None |
| unreleased | field 'cwd' default added: None |
| unreleased | field 'run_output_dir' default added: None |
| unreleased | added base class 'Entity' |
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext shellconfig_changes === -->