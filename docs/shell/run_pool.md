# run_pool

<!-- === DO_NOT_EDIT: pkg-ext run_pool_def === -->
## class: run_pool
- [source](../../ask_shell/_internal/run_pool.py#L28)
> **Since:** 0.3.0

```python
class run_pool:
    task_name: str
    total: int = 0
    max_concurrent_submits: int = 4
    threads_used_per_submit: int = 5
    pool_thread_count: int | None = None
    sleep_time: float = 1
    sleep_callback: Callable[[], Any] | None = None
    exit_wait_timeout: float | None = None
    pool: ThreadPoolExecutor
```
<!-- === OK_EDIT: pkg-ext run_pool_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| task_name | `str` | - | 0.3.0 |
| total | `int` | `0` | 0.3.0 |
| max_concurrent_submits | `int` | `4` | 0.3.0 |
| threads_used_per_submit | `int` | `5` | 0.3.0 |
| pool_thread_count | `int | None` | `None` | unreleased |
| sleep_time | `float` | `1` | 0.3.0 |
| sleep_callback | `Callable[[], Any] | None` | `None` | 0.3.0 |
| exit_wait_timeout | `float | None` | `None` | 0.3.0 |
| pool | `ThreadPoolExecutor` | - | 0.3.0 |

<!-- === DO_NOT_EDIT: pkg-ext run_pool_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | field 'pool' default removed (was: ...) |
| unreleased | added optional field 'pool_thread_count' (default: None) |
| 0.3.0 | Made public |
<!-- === OK_EDIT: pkg-ext run_pool_changes === -->