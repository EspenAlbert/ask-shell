<!-- === DO_NOT_EDIT: pkg-ext header === -->
# console

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`RemoveLivePart`](#removelivepart_def)
- [`add_renderable`](#add_renderable_def)
- [`configure_logging`](#configure_logging_def)
- [`get_live_console`](#get_live_console_def)
- [`interactive_shell`](#interactive_shell_def)
- [`log_to_live`](#log_to_live_def)
- [`new_task`](#new_task_def)
- [`print_to_live`](#print_to_live_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext removelivepart_def === -->
<a id="removelivepart_def"></a>

### class: `RemoveLivePart`
- [source](../../ask_shell/_internal/rich_live.py#L148)
> **Since:** 0.3.0

```python
class RemoveLivePart:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext removelivepart_def === -->
<!-- === DO_NOT_EDIT: pkg-ext add_renderable_def === -->
<a id="add_renderable_def"></a>

### function: `add_renderable`
- [source](../../ask_shell/_internal/rich_live.py#L152)
> **Since:** 0.3.0

```python
def add_renderable(renderable: ConsoleRenderable | RichCast | str, *, order: int = 0, name: str = '') -> RemoveLivePart:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext add_renderable_def === -->
<!-- === DO_NOT_EDIT: pkg-ext configure_logging_def === -->
<a id="configure_logging_def"></a>

### function: `configure_logging`
- [source](../../ask_shell/_internal/typer_command.py#L133)
> **Since:** 0.3.0

```python
def configure_logging(app: Typer, *, settings: AskShellSettings | None = None, app_pretty_exceptions_enable: bool = False, app_pretty_exceptions_show_locals: bool = False, skip_except_hook: bool = False, use_app_name_command_for_logs: bool = True, render_rich_error_on_sys_exit: bool = False) -> Handler:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext configure_logging_def === -->
<!-- === DO_NOT_EDIT: pkg-ext get_live_console_def === -->
<a id="get_live_console_def"></a>

### function: `get_live_console`
- [source](../../ask_shell/_internal/rich_live.py#L170)
> **Since:** 0.3.0

```python
def get_live_console() -> Console:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext get_live_console_def === -->
<!-- === DO_NOT_EDIT: pkg-ext interactive_shell_def === -->
<a id="interactive_shell_def"></a>

### function: `interactive_shell`
- [source](../../ask_shell/_internal/_run_env.py#L27)
> **Since:** 0.3.0

```python
def interactive_shell() -> bool:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext interactive_shell_def === -->
<!-- === DO_NOT_EDIT: pkg-ext log_to_live_def === -->
<a id="log_to_live_def"></a>

### function: `log_to_live`
- [source](../../ask_shell/_internal/rich_live.py#L210)
> **Since:** 0.3.0

```python
def log_to_live(*objects, sep: str = ' ', end: str = '\n', style: str | Style | None = None, justify: Literal[default, left, center, right, full] | None = None, emoji: bool | None = None, markup: bool | None = None, highlight: bool | None = None, log_locals: bool = False, _stack_offset: int = 1) -> None:
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext log_to_live_def === -->
<!-- === DO_NOT_EDIT: pkg-ext new_task_def === -->
<a id="new_task_def"></a>

### class: `new_task`
- [source](../../ask_shell/_internal/rich_progress.py#L153)
> **Since:** 0.3.0

```python
class new_task:
    description: str
    total: float = 1
    visible: bool = True
    task_fields: dict = ...
    log_after_remove: bool = True
    log_updates: bool = False
    manager: ProgressManager = ...
    completed: float = 0.0
```

| Field | Type | Default | Since |
|---|---|---|---|
| description | `str` | - | 0.3.0 |
| total | `float` | `1` | 0.3.0 |
| visible | `bool` | `True` | 0.3.0 |
| task_fields | `dict` | `...` | 0.3.0 |
| log_after_remove | `bool` | `True` | 0.3.0 |
| log_updates | `bool` | `False` | 0.3.0 |
| manager | `ProgressManager` | `...` | 0.3.0 |
| completed | `float` | `0.0` | 0.3.0 |

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext new_task_def === -->
<!-- === DO_NOT_EDIT: pkg-ext print_to_live_def === -->
<a id="print_to_live_def"></a>

### function: `print_to_live`
- [source](../../ask_shell/_internal/rich_live.py#L174)
> **Since:** 0.3.0

```python
def print_to_live(*objects, sep: str = ' ', end: str = '\n', style: str | Style | None = None, justify: Literal[default, left, center, right, full] | None = None, overflow: Literal[fold, crop, ellipsis, ignore] | None = None, no_wrap: bool | None = None, emoji: bool | None = None, markup: bool | None = None, highlight: bool | None = None, width: int | None = None, height: int | None = None, crop: bool = True, soft_wrap: bool | None = None, new_line_start: bool = False):
    ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext print_to_live_def === -->