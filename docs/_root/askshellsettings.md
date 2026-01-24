# AskShellSettings

<!-- === DO_NOT_EDIT: pkg-ext askshellsettings_def === -->
## class: AskShellSettings
- [source](../../ask_shell/settings.py#L93)
> **Since:** 0.3.0

```python
class AskShellSettings(StaticSettings):
    STATIC_DIR: Path | None
    CACHE_DIR: Path | None
    SKIP_APP_NAME: bool = False
    log_level: Literal[DEBUG, INFO, WARNING, ERROR, CRITICAL, UNSET] = 'UNSET'
    force_interactive_shell: bool = False
    thread_count: int = 50
    thread_pool_full_wait_time_seconds: float = 5
    search_enabled_after_choices: int = 7
    global_callback_strings: list[str] = ...
    remove_os_secrets: bool = ...
    run_logs_dir: Path | None
    run_logs_clean: str = 'yesterday'
```
<!-- === OK_EDIT: pkg-ext askshellsettings_def === -->

### Environment Variables

| Variable | Field | Type | Default |
|----------|-------|------|---------|
| `static_dir` | `STATIC_DIR` | Path | PydanticUndefined |
| `cache_dir` | `CACHE_DIR` | Path | PydanticUndefined |
| `skip_app_name` | `SKIP_APP_NAME` | bool | False |
| `log_level` | `log_level` | Literal[DEBUG, INFO, WARNING, ERROR, CRITICAL, UNSET] | 'UNSET' |
| `ask_shell_force_interactive_shell` | `force_interactive_shell` | bool | False |
| `force_interactive_shell` | `force_interactive_shell` | bool | False |
| `ask_shell_thread_count` | `thread_count` | int | 50 |
| `thread_count` | `thread_count` | int | 50 |
| `ask_shell_thread_pool_full_wait_time_seconds` | `thread_pool_full_wait_time_seconds` | float | 5 |
| `thread_pool_full_wait_time_seconds` | `thread_pool_full_wait_time_seconds` | float | 5 |
| `ask_shell_search_enabled_after_choices` | `search_enabled_after_choices` | int | 7 |
| `search_enabled_after_choices` | `search_enabled_after_choices` | int | 7 |
| `ask_shell_global_callbacks` | `global_callback_strings` | list[str] | ... |
| `global_callback_strings` | `global_callback_strings` | list[str] | ... |
| `ask_shell_remove_os_secrets` | `remove_os_secrets` | bool | ... |
| `remove_os_secrets` | `remove_os_secrets` | bool | ... |
| `ask_shell_run_logs_dir` | `run_logs_dir` | Path | None | - |
| `run_logs_dir` | `run_logs_dir` | Path | None | - |
| `ask_shell_run_logs_clean` | `run_logs_clean` | str | 'yesterday' |
| `run_logs_clean` | `run_logs_clean` | str | 'yesterday' |

### Fields

| Field | Type | Default | Since | Description |
|---|---|---|---|---|
| STATIC_DIR | `Path` | `PydanticUndefined` | 0.2.0 | - |
| CACHE_DIR | `Path` | `PydanticUndefined` | 0.2.0 | - |
| SKIP_APP_NAME | `bool` | `False` | 0.2.0 | - |
| log_level | `Literal[DEBUG, INFO, WARNING, ERROR, CRITICAL, UNSET]` | `'UNSET'` | 0.2.0 | - |
| force_interactive_shell | `bool` | `False` | 0.2.0 | Useful for testing |
| thread_count | `int` | `50` | 0.2.0 | Thread count for ask-shell pool |
| thread_pool_full_wait_time_seconds | `float` | `5` | 0.2.0 | How long to wait when the thread pools is full before trying again |
| search_enabled_after_choices | `int` | `7` | 0.2.0 | How many choices to show before enabling search |
| global_callback_strings | `list[str]` | `...` | 0.2.0 | Use global callbacks to receive ShellRun events. Uses `locate` to find the callback function by its string name. Setting this will override defaults |
| remove_os_secrets | `bool` | `...` | 0.2.0 | Use a log filter to remove secrets from the terminal output. No guarantees though. Always be careful when logging. |
| run_logs_dir | `Path | None` | - | 0.2.0 | Directory to store run logs. If not set, defaults to `cache_root/run_logs/YYYY-MM-DD`. You can also use `configure_run_logs_dir_if_unset` to set it dynamically. |
| run_logs_clean | `str` | `'yesterday'` | 0.2.0 | Runs once If `run_logs_dir` is not set. Can be 'yesterday' or a date string like '2023-01-01'. Will clean all logs up until the specified date but not that date itself. |

<!-- === DO_NOT_EDIT: pkg-ext askshellsettings_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext askshellsettings_changes === -->