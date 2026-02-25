<!-- === DO_NOT_EDIT: pkg-ext header === -->
# shell

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [ShellConfig](./shellconfig.md)
- [ShellError](./shellerror.md)
- [`ShellRun`](#shellrun_def)
- [`handle_interrupt_wait`](#handle_interrupt_wait_def)
- [`kill`](#kill_def)
- [`kill_all_runs`](#kill_all_runs_def)
- [run](./run.md)
- [run_and_wait](./run_and_wait.md)
- [`run_error`](#run_error_def)
- [`run_pool`](#run_pool_def)
- [`stop_runs_and_pool`](#stop_runs_and_pool_def)
- [`wait_on_ok_errors`](#wait_on_ok_errors_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

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