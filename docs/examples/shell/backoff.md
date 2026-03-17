<!--
description: Configurable exponential backoff with jitter for retries
-->
# backoff

`ShellConfig` supports exponential backoff between retry attempts via three fields:
`retry_initial_wait`, `retry_max_wait`, and `retry_jitter`.

When `attempts > 1`, the wait before retry N is `min(initial_wait * 2^(N-2), max_wait) + uniform(0, jitter)`.

```python
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from ask_shell.shell import run_and_wait

script = """\
from pathlib import Path
p = Path(__file__).with_name("attempt")
n = int(p.read_text()) if p.exists() else 1
p.write_text(str(n + 1))
if n < 4:
    raise SystemExit(1)
print(f"ok on attempt {n}")
"""

with TemporaryDirectory() as tmp:
    script_path = Path(tmp) / "retry.py"
    script_path.write_text(script)
    start = time.monotonic()
    result = run_and_wait(
        f"{sys.executable} {script_path}",
        attempts=4,
        retry_initial_wait=0.1,
        retry_max_wait=10,
        retry_jitter=0,
    )
    elapsed = time.monotonic() - start
    print(result.stdout)
    #> ok on attempt 4
    print(f"waited at least 0.7s: {elapsed >= 0.7}")
    #> waited at least 0.7s: True
    print(f"waited less than 2s: {elapsed < 2}")
    #> waited less than 2s: True
```
