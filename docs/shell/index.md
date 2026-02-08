<!-- === DO_NOT_EDIT: pkg-ext header === -->
# shell

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`ShellConfig`](#shellconfig_def)
- [`ShellError`](#shellerror_def)
- [`ShellRun`](#shellrun_def)
- [`handle_interrupt_wait`](#handle_interrupt_wait_def)
- [`kill`](#kill_def)
- [`kill_all_runs`](#kill_all_runs_def)
- [`run`](#run_def)
- [`run_and_wait`](#run_and_wait_def)
- [`run_error`](#run_error_def)
- [`run_pool`](#run_pool_def)
- [`stop_runs_and_pool`](#stop_runs_and_pool_def)
- [`wait_on_ok_errors`](#wait_on_ok_errors_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext shellconfig_def === -->
<a id="shellconfig_def"></a>

### class: `ShellConfig`
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

| Field | Type | Default | Since | Description |
|---|---|---|---|---|
| shell_input | `str` | - | 0.3.0 | - |
| env | `dict[str, str]` | `...` | 0.3.0 | - |
| extra_popen_kwargs | `dict` | `...` | 0.3.0 | - |
| allow_non_zero_exit | `bool` | `False` | 0.3.0 | - |
| skip_os_env | `bool` | `False` | 0.3.0 | - |
| skip_binary_check | `bool` | `False` | 0.3.0 | - |
| skip_interactive_check | `bool` | `False` | 0.3.0 | - |
| cwd | `Path` | `None` | 0.3.0 | Set to Path.cwd() if not provided |
| user_input | `bool` | `False` | 0.3.0 | - |
| attempts | `int` | `1` | 0.3.0 | - |
| should_retry | `Callable[[<class 'ask_shell._internal.models.ShellRun'>], bool]` | `<function always_retry>` | 0.3.0 | - |
| print_prefix | `str` | `None` | 0.3.0 | Use cwd+binary_name+first_arg if not provided |
| include_log_time | `bool` | `False` | 0.3.0 | - |
| ansi_content | `bool` | `None` | 0.3.0 | Inferred if not provided |
| run_output_dir | `Path | None` | `None` | 0.3.0 | Directory to store run logs, defaults to settings.run_logs /{XX}_{self.exec_name} |
| run_log_stem_prefix | `str` | `''` | 0.3.0 | Prefix for run log stem |
| skip_html_log_files | `bool` | `False` | 0.3.0 | Skip HTML log files, by default dumps HTML logs to support viewing colored output in browsers |
| skip_progress_output | `bool` | `False` | 0.3.0 | Skip transitive std out/err output, useful for large outputs that are not needed in the logs when running parallel scripts |
| terminal_width | `int | None` | `999` | 0.3.0 | - |
| is_binary_call | `bool` | `None` | 0.3.0 | Inferred if not provided |
| settings | `AskShellSettings` | `...` | 0.3.0 | - |
| message_callbacks | `list[Callable[[typing.Union[ask_shell._internal.events.ShellRunBefore, ask_shell._internal.events.ShellRunPOpenStarted, ask_shell._internal.events.ShellRunStdStarted, ask_shell._internal.events.ShellRunStdReadError, ask_shell._internal.events.ShellRunStdOutput, ask_shell._internal.events.ShellRunRetryAttempt, ask_shell._internal.events.ShellRunAfter]], bool | None]]` | `...` | 0.3.0 | Callbacks for run messages, useful for custom handling of stdout/stderr |

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext shellconfig_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellerror_def === -->
<a id="shellerror_def"></a>

### exception: `ShellError`
- [source](../../ask_shell/_internal/models.py#L484)
> **Since:** 0.3.0

```python
class ShellError(Exception):
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext shellerror_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellrun_def === -->
<a id="shellrun_def"></a>

### class: `ShellRun`
- [source](../../ask_shell/_internal/models.py#L269)
> **Since:** 0.3.0

```python
class ShellRun:
    config: ShellConfig
    p_open: Popen | None = None
    current_attempt: int = 1
```

Stores dynamic behavior. Only created by this file never outside.

Args:
    _start_flag: Future[ShellRun]: Flag that is set when the run has both p_open and stdout/stderr reading started. During multiple attempts, only the 1st attempt will call it.

| Field | Type | Default | Since |
|---|---|---|---|
| config | `ShellConfig` | - | 0.3.0 |
| p_open | `Popen | None` | `None` | 0.3.0 |
| current_attempt | `int` | `1` | 0.3.0 |

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext shellrun_def === -->
<!-- === DO_NOT_EDIT: pkg-ext handle_interrupt_wait_def === -->
<a id="handle_interrupt_wait_def"></a>

### class: `handle_interrupt_wait`
- [source](../../ask_shell/_internal/_run.py#L140)
> **Since:** 0.3.0

```python
class handle_interrupt_wait:
    interrupt_message: str
    immediate_kill: bool = False
```

| Field | Type | Default | Since |
|---|---|---|---|
| interrupt_message | `str` | - | 0.3.0 |
| immediate_kill | `bool` | `False` | 0.3.0 |

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext handle_interrupt_wait_def === -->
<!-- === DO_NOT_EDIT: pkg-ext kill_def === -->
<a id="kill_def"></a>

### function: `kill`
- [source](../../ask_shell/_internal/_run.py#L72)
> **Since:** 0.3.0

```python
def kill(run: ShellRun, immediate: bool = False, reason: str = '', abort_timeout: float = 3.0):
    ...
```

https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext kill_def === -->
<!-- === DO_NOT_EDIT: pkg-ext kill_all_runs_def === -->
<a id="kill_all_runs_def"></a>

### function: `kill_all_runs`
- [source](../../ask_shell/_internal/_run.py#L105)
> **Since:** 0.3.0

```python
def kill_all_runs(immediate: bool = False, reason: str = '', abort_timeout: float = 3.0, *, skip_retry: bool = False):
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext kill_all_runs_def === -->
<!-- === DO_NOT_EDIT: pkg-ext run_def === -->
<a id="run_def"></a>

### function: `run`
- [source](../../ask_shell/_internal/_run.py#L428)
> **Since:** 0.3.0

```python
def run(config: ShellConfig | str, *, allow_non_zero_exit: bool | None = None, ansi_content: bool | None = None, attempts: int | None = None, cwd: str | Path | None = None, env: dict[str, str] | None = None, extra_popen_kwargs: dict | None = None, is_binary_call: bool | None = None, message_callbacks: list[Callable[[typing.Union[ask_shell._internal.events.ShellRunBefore, ask_shell._internal.events.ShellRunPOpenStarted, ask_shell._internal.events.ShellRunStdStarted, ask_shell._internal.events.ShellRunStdReadError, ask_shell._internal.events.ShellRunStdOutput, ask_shell._internal.events.ShellRunRetryAttempt, ask_shell._internal.events.ShellRunAfter]], bool]] | None = None, print_prefix: str | None = None, run_log_stem_prefix: str | None = None, run_output_dir: Path | None = None, settings: AskShellSettings | None = None, should_retry: Callable[[<class 'ask_shell._internal.models.ShellRun'>], bool] | None = None, skip_binary_check: bool | None = None, skip_html_log_files: bool | None = None, skip_progress_output: bool | None = None, include_log_time: bool | None = None, skip_os_env: bool | None = None, start_timeout: float | None = None, terminal_width: int | None = None, skip_interactive_check: bool | None = None) -> ShellRun:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext run_def === -->
<!-- === DO_NOT_EDIT: pkg-ext run_and_wait_def === -->
<a id="run_and_wait_def"></a>

### function: `run_and_wait`
- [source](../../ask_shell/_internal/_run.py#L486)
> **Since:** 0.3.0

```python
def run_and_wait(script: ShellConfig | str, timeout: float | None = None, *, allow_non_zero_exit: bool | None = None, ansi_content: bool | None = None, attempts: int | None = None, cwd: str | Path | None = None, env: dict[str, str] | None = None, extra_popen_kwargs: dict | None = None, is_binary_call: bool | None = None, message_callbacks: list[Callable[[typing.Union[ask_shell._internal.events.ShellRunBefore, ask_shell._internal.events.ShellRunPOpenStarted, ask_shell._internal.events.ShellRunStdStarted, ask_shell._internal.events.ShellRunStdReadError, ask_shell._internal.events.ShellRunStdOutput, ask_shell._internal.events.ShellRunRetryAttempt, ask_shell._internal.events.ShellRunAfter]], bool]] | None = None, print_prefix: str | None = None, run_log_stem_prefix: str | None = None, run_output_dir: Path | None = None, settings: AskShellSettings | None = None, should_retry: Callable[[<class 'ask_shell._internal.models.ShellRun'>], bool] | None = None, skip_binary_check: bool | None = None, skip_progress_output: bool | None = None, skip_html_log_files: bool | None = None, include_log_time: bool | None = None, skip_os_env: bool | None = None, user_input: bool | None = None, terminal_width: int | None = None, skip_interactive_check: bool | None = None) -> ShellRun:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext run_and_wait_def === -->
<!-- === DO_NOT_EDIT: pkg-ext run_error_def === -->
<a id="run_error_def"></a>

### function: `run_error`
- [source](../../ask_shell/_internal/_run.py#L545)
> **Since:** 0.3.0

```python
def run_error(run: ShellRun, timeout: float | None = 1) -> BaseException | None:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext run_error_def === -->
<!-- === DO_NOT_EDIT: pkg-ext run_pool_def === -->
<a id="run_pool_def"></a>

### class: `run_pool`
- [source](../../ask_shell/_internal/run_pool.py#L25)
> **Since:** 0.3.0

```python
class run_pool:
    task_name: str
    total: int = 0
    max_concurrent_submits: int = 4
    threads_used_per_submit: int = 5
    sleep_time: float = 1
    sleep_callback: Callable[[], Any] | None = None
    exit_wait_timeout: float | None = None
    pool: ThreadPoolExecutor = ...
```

| Field | Type | Default | Since |
|---|---|---|---|
| task_name | `str` | - | 0.3.0 |
| total | `int` | `0` | 0.3.0 |
| max_concurrent_submits | `int` | `4` | 0.3.0 |
| threads_used_per_submit | `int` | `5` | 0.3.0 |
| sleep_time | `float` | `1` | 0.3.0 |
| sleep_callback | `Callable[[], Any] | None` | `None` | 0.3.0 |
| exit_wait_timeout | `float | None` | `None` | 0.3.0 |
| pool | `ThreadPoolExecutor` | `...` | 0.3.0 |

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext run_pool_def === -->
<!-- === DO_NOT_EDIT: pkg-ext stop_runs_and_pool_def === -->
<a id="stop_runs_and_pool_def"></a>

### function: `stop_runs_and_pool`
- [source](../../ask_shell/_internal/_run.py#L132)
> **Since:** 0.3.0

```python
def stop_runs_and_pool(reason: str = 'atexit', immediate: bool = False):
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext stop_runs_and_pool_def === -->
<!-- === DO_NOT_EDIT: pkg-ext wait_on_ok_errors_def === -->
<a id="wait_on_ok_errors_def"></a>

### function: `wait_on_ok_errors`
- [source](../../ask_shell/_internal/_run.py#L552)
> **Since:** 0.3.0

```python
def wait_on_ok_errors(*runs, timeout: float | None = None, skip_kill_timeouts: bool = False) -> tuple[list[ShellRun], list[tuple[BaseException, ShellRun]]]:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext wait_on_ok_errors_def === -->