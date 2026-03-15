<!--
description: Stop retrying with a custom error by raising AbortRetryError from should_retry
-->
# AbortRetryError

Raise `AbortRetryError` from a `should_retry` callback to stop retrying immediately.
The exception propagates as `ShellError.base_error`.

## Abort on permanent failure

```python
import sys

import pytest

from ask_shell._internal.models import AbortRetryError, ShellConfig, ShellError, ShellRun
from ask_shell.shell import run_and_wait

PYTHON_EXEC = sys.executable


def should_retry_check(run: ShellRun) -> bool:
    if "transient" in run.stderr:
        return True
    raise AbortRetryError(f"permanent: {run.stderr[:100]}")


script = f"""\
import sys
sys.stderr.write("permanent error")
sys.exit(1)
"""

with pytest.raises(ShellError) as exc:
    run_and_wait(
        ShellConfig(
            shell_input=f"{PYTHON_EXEC} -c '{script}'",
            attempts=3,
            should_retry=should_retry_check,
        )
    )

assert isinstance(exc.value.base_error, AbortRetryError)
print(str(exc.value.base_error))
#> permanent: permanent error
```

## Retry on transient, then succeed

```python
import sys
from pathlib import Path
from tempfile import mkdtemp

from ask_shell._internal.models import AbortRetryError, ShellConfig, ShellRun
from ask_shell.shell import run_and_wait

PYTHON_EXEC = sys.executable
tmp = Path(mkdtemp())
attempt_file = tmp / "attempt"

script_text = f"""\
import sys
from pathlib import Path
p = Path("{attempt_file}")
n = int(p.read_text()) if p.exists() else 1
p.write_text(str(n + 1))
if n < 2:
    sys.stderr.write("transient error")
    sys.exit(1)
print("ok")
"""
(tmp / "run.py").write_text(script_text)


def should_retry_transient(run: ShellRun) -> bool:
    if "transient" in run.stderr:
        return True
    raise AbortRetryError("permanent")


result = run_and_wait(
    ShellConfig(
        shell_input=f"{PYTHON_EXEC} {tmp / 'run.py'}",
        attempts=3,
        should_retry=should_retry_transient,
    )
)
print(result.stdout)
#> ok
```
