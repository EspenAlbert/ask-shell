# AbortRetryError

Exception that can be raised from a `should_retry` callback to stop retrying immediately with a custom error.

## Usage

When `attempts > 1` and a command fails, ask-shell calls `should_retry(run)`. The callback can:

- **Return `True`** — retry (optionally after cleanup)
- **Return `False`** — stop retrying, caller gets `ShellError`
- **Raise `AbortRetryError`** — stop retrying, caller gets `ShellError` with `base_error` set to the `AbortRetryError`

```python
from ask_shell.shell import AbortRetryError, ShellRun, run_and_wait

def should_retry_init(run: ShellRun) -> bool:
    if "checksum" in run.stderr:
        (run.config.cwd / ".terraform/providers").unlink(missing_ok=True)
        return True
    raise AbortRetryError(f"permanent failure: {run.stderr[:500]}")

result = run_and_wait("terraform init", attempts=3, should_retry=should_retry_init)
```
