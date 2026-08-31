<!-- === DO_NOT_EDIT: pkg-ext header === -->
# console

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`LivePrintContext`](#liveprintcontext_def)
- [`RemoveLivePart`](#removelivepart_def)
- [`add_renderable`](#add_renderable_def)
- [`configure_logging`](#configure_logging_def)
- [`disable_interactive_shell`](#disable_interactive_shell_def)
- [`get_live_console`](#get_live_console_def)
- [`get_live_print_context`](#get_live_print_context_def)
- [`interactive_shell`](#interactive_shell_def)
- [`live_print_scope`](#live_print_scope_def)
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
- [source](../../ask_shell/_internal/rich_live.py#L158)
> **Since:** 0.3.0

```python
class RemoveLivePart: ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext removelivepart_def === -->
<!-- === DO_NOT_EDIT: pkg-ext add_renderable_def === -->
<a id="add_renderable_def"></a>

### function: `add_renderable`
- [source](../../ask_shell/_internal/rich_live.py#L162)
- [Example: Mount a dynamic Rich renderable in ask-shell's live region with add_renderable, plus an apply-live demo with CI heartbeats](../examples/console/add_renderable.md)
> **Since:** 0.3.0

```python
def add_renderable(
    renderable: ConsoleRenderable | RichCast | str, *, order: int = 0, name: str = ""
) -> RemoveLivePart: ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext add_renderable_def === -->
<!-- === DO_NOT_EDIT: pkg-ext configure_logging_def === -->
<a id="configure_logging_def"></a>

### function: `configure_logging`
- [source](../../ask_shell/_internal/typer_command.py#L169)
> **Since:** 0.3.0

```python
def configure_logging(
    app: Typer,
    *,
    settings: AskShellSettings | None = None,
    app_pretty_exceptions_enable: bool = False,
    app_pretty_exceptions_show_locals: bool = False,
    skip_except_hook: bool = False,
    use_app_name_command_for_logs: bool = True,
    render_rich_error_on_sys_exit: bool = False,
) -> Handler: ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext configure_logging_def === -->
<!-- === DO_NOT_EDIT: pkg-ext get_live_console_def === -->
<a id="get_live_console_def"></a>

### function: `get_live_console`
- [source](../../ask_shell/_internal/rich_live.py#L180)
> **Since:** 0.3.0

```python
def get_live_console() -> Console: ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext get_live_console_def === -->
<!-- === DO_NOT_EDIT: pkg-ext interactive_shell_def === -->
<a id="interactive_shell_def"></a>

### function: `interactive_shell`
- [source](../../ask_shell/_internal/_run_env.py#L28)
> **Since:** 0.3.0

```python
def interactive_shell() -> bool: ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext interactive_shell_def === -->
<!-- === DO_NOT_EDIT: pkg-ext log_to_live_def === -->
<a id="log_to_live_def"></a>

### function: `log_to_live`
- [source](../../ask_shell/_internal/rich_live.py#L234)
> **Since:** 0.3.0

```python
def log_to_live(
    *objects,
    sep: str = " ",
    end: str = "\n",
    style: str | Style | None = None,
    justify: Literal[default, left, center, right, full] | None = None,
    emoji: bool | None = None,
    markup: bool | None = None,
    highlight: bool | None = None,
    log_locals: bool = False,
    _stack_offset: int = 1,
) -> None: ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext log_to_live_def === -->
<!-- === DO_NOT_EDIT: pkg-ext new_task_def === -->
<a id="new_task_def"></a>

### class: `new_task`
- [source](../../ask_shell/_internal/rich_progress.py#L168)
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
- [source](../../ask_shell/_internal/rich_live.py#L195)
> **Since:** 0.3.0

```python
def print_to_live(
    *objects,
    sep: str = " ",
    end: str = "\n",
    style: str | Style | None = None,
    justify: Literal[default, left, center, right, full] | None = None,
    overflow: Literal[fold, crop, ellipsis, ignore] | None = None,
    no_wrap: bool | None = None,
    emoji: bool | None = None,
    markup: bool | None = None,
    highlight: bool | None = None,
    width: int | None = None,
    height: int | None = None,
    crop: bool = True,
    soft_wrap: bool | None = None,
    new_line_start: bool = False,
): ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext print_to_live_def === -->
<!-- === DO_NOT_EDIT: pkg-ext disable_interactive_shell_def === -->
<a id="disable_interactive_shell_def"></a>

### function: `disable_interactive_shell`
- [source](../../ask_shell/_internal/_run_env.py#L47)
> **Since:** 0.9.0

```python
def disable_interactive_shell() -> None: ...
```

Force non-interactive mode for the remainder of this process.

### Changes

| Version | Change |
|---------|--------|
| 0.9.0 | Made public |
<!-- === OK_EDIT: pkg-ext disable_interactive_shell_def === -->
<!-- === DO_NOT_EDIT: pkg-ext liveprintcontext_def === -->
<a id="liveprintcontext_def"></a>

### class: `LivePrintContext`
- [source](../../ask_shell/_internal/live_print_context.py#L9)
> **Since:** 0.10.0

```python
class LivePrintContext:
    prefix: str = ""
    suppress: bool = False
```

| Field | Type | Default | Since |
|---|---|---|---|
| prefix | `str` | `''` | 0.10.0 |
| suppress | `bool` | `False` | 0.10.0 |

### Changes

| Version | Change |
|---------|--------|
| 0.10.0 | Made public |
<!-- === OK_EDIT: pkg-ext liveprintcontext_def === -->
<!-- === DO_NOT_EDIT: pkg-ext get_live_print_context_def === -->
<a id="get_live_print_context_def"></a>

### function: `get_live_print_context`
- [source](../../ask_shell/_internal/live_print_context.py#L18)
> **Since:** 0.10.0

```python
def get_live_print_context() -> LivePrintContext | None: ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.10.0 | Made public |
<!-- === OK_EDIT: pkg-ext get_live_print_context_def === -->
<!-- === DO_NOT_EDIT: pkg-ext live_print_scope_def === -->
<a id="live_print_scope_def"></a>

### function: `live_print_scope`
- [source](../../ask_shell/_internal/live_print_context.py#L22)
- [Example: Prefix or suppress live-console scroll lines per scope, including across run_pool workers](../examples/console/live_print_scope.md)
> **Since:** 0.10.0

```python
def live_print_scope(*, prefix: str = "", suppress: bool = False) -> Iterator[None]: ...
```

### Changes

| Version | Change |
|---------|--------|
| 0.10.0 | Made public |
<!-- === OK_EDIT: pkg-ext live_print_scope_def === -->