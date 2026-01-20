<!-- === DO_NOT_EDIT: pkg-ext header === -->
# shell_events

<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`OutputCallbackT`](#outputcallbackt_def)
- [`ShellRunAfter`](#shellrunafter_def)
- [`ShellRunBefore`](#shellrunbefore_def)
- [`ShellRunCallbackT`](#shellruncallbackt_def)
- [`ShellRunPOpenStarted`](#shellrunpopenstarted_def)
- [`ShellRunRetryAttempt`](#shellrunretryattempt_def)
- [`ShellRunStdOutput`](#shellrunstdoutput_def)
- [`ShellRunStdReadError`](#shellrunstdreaderror_def)
- [`ShellRunStdStarted`](#shellrunstdstarted_def)
<!-- === OK_EDIT: pkg-ext symbols === -->

<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->

<!-- === DO_NOT_EDIT: pkg-ext outputcallbackt_def === -->
<a id="outputcallbackt_def"></a>

### type_alias: `OutputCallbackT`
- [source](../../ask_shell/_internal/events.py)
> **Since:** 0.2.0

```python
OutputCallbackT = typing.Callable[[str], bool | None]
```
<!-- === OK_EDIT: pkg-ext outputcallbackt_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellrunafter_def === -->
<a id="shellrunafter_def"></a>

### class: `ShellRunAfter`
- [source](../../ask_shell/_internal/events.py#L49)
> **Since:** 0.2.0

```python
class ShellRunAfter:
    run: ShellRun
    error: BaseException | None = None
```

| Field | Type | Default | Since |
|---|---|---|---|
| run | `ShellRun` | - | 0.2.0 |
| error | `BaseException | None` | `None` | 0.2.0 |
<!-- === OK_EDIT: pkg-ext shellrunafter_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellrunbefore_def === -->
<a id="shellrunbefore_def"></a>

### class: `ShellRunBefore`
- [source](../../ask_shell/_internal/events.py#L44)
> **Since:** 0.2.0

```python
class ShellRunBefore:
    run: ShellRun
```

| Field | Type | Default | Since |
|---|---|---|---|
| run | `ShellRun` | - | 0.2.0 |
<!-- === OK_EDIT: pkg-ext shellrunbefore_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellruncallbackt_def === -->
<a id="shellruncallbackt_def"></a>

### type_alias: `ShellRunCallbackT`
- [source](../../ask_shell/_internal/events.py)
> **Since:** 0.2.0

```python
ShellRunCallbackT = typing.Callable[[typing.Union[ask_shell._internal.events.ShellRunBefore, ask_shell._internal.events.ShellRunPOpenStarted, ask_shell._internal.events.ShellRunStdStarted, ask_shell._internal.events.ShellRunStdReadError, ask_shell._internal.events.ShellRunStdOutput, ask_shell._internal.events.ShellRunRetryAttempt, ask_shell._internal.events.ShellRunAfter]], bool | None]
```
<!-- === OK_EDIT: pkg-ext shellruncallbackt_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellrunpopenstarted_def === -->
<a id="shellrunpopenstarted_def"></a>

### class: `ShellRunPOpenStarted`
- [source](../../ask_shell/_internal/events.py#L28)
> **Since:** 0.2.0

```python
class ShellRunPOpenStarted:
    p_open: Popen
```

| Field | Type | Default | Since |
|---|---|---|---|
| p_open | `Popen` | - | 0.2.0 |
<!-- === OK_EDIT: pkg-ext shellrunpopenstarted_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellrunretryattempt_def === -->
<a id="shellrunretryattempt_def"></a>

### class: `ShellRunRetryAttempt`
- [source](../../ask_shell/_internal/events.py#L39)
> **Since:** 0.2.0

```python
class ShellRunRetryAttempt:
    attempt: int
```

| Field | Type | Default | Since |
|---|---|---|---|
| attempt | `int` | - | 0.2.0 |
<!-- === OK_EDIT: pkg-ext shellrunretryattempt_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellrunstdoutput_def === -->
<a id="shellrunstdoutput_def"></a>

### class: `ShellRunStdOutput`
- [source](../../ask_shell/_internal/events.py#L22)
> **Since:** 0.2.0

```python
class ShellRunStdOutput:
    is_stdout: bool
    content: str
```

| Field | Type | Default | Since |
|---|---|---|---|
| is_stdout | `bool` | - | 0.2.0 |
| content | `str` | - | 0.2.0 |
<!-- === OK_EDIT: pkg-ext shellrunstdoutput_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellrunstdreaderror_def === -->
<a id="shellrunstdreaderror_def"></a>

### class: `ShellRunStdReadError`
- [source](../../ask_shell/_internal/events.py#L33)
> **Since:** 0.2.0

```python
class ShellRunStdReadError:
    is_stdout: bool
    error: BaseException
```

| Field | Type | Default | Since |
|---|---|---|---|
| is_stdout | `bool` | - | 0.2.0 |
| error | `BaseException` | - | 0.2.0 |
<!-- === OK_EDIT: pkg-ext shellrunstdreaderror_def === -->
<!-- === DO_NOT_EDIT: pkg-ext shellrunstdstarted_def === -->
<a id="shellrunstdstarted_def"></a>

### class: `ShellRunStdStarted`
- [source](../../ask_shell/_internal/events.py#L15)
> **Since:** 0.2.0

```python
class ShellRunStdStarted:
    is_stdout: bool
    console: Console
    log_path: Path
```

| Field | Type | Default | Since |
|---|---|---|---|
| is_stdout | `bool` | - | 0.2.0 |
| console | `Console` | - | 0.2.0 |
| log_path | `Path` | - | 0.2.0 |
<!-- === OK_EDIT: pkg-ext shellrunstdstarted_def === -->