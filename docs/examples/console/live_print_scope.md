<!--
description: Prefix or suppress live-console scroll lines per scope, including across run_pool workers
-->
# live_print_scope

`live_print_scope` stores per-scope metadata in a [`contextvars`](https://docs.python.org/3/library/contextvars.html) `ContextVar`. [`print_to_live`](../../console/index.md#print_to_live_def) and [`log_to_live`](../../console/index.md#log_to_live_def) read the active scope: they prepend `prefix` to each line and skip output when `suppress` is true.

Use it when parallel work (for example tfdo multi-directory orchestration) needs tagged scroll lines without editing every `print_to_live` call site. Pair it with [`run_pool`](../../shell/run_pool.md): `submit` copies the submitter's context into the worker thread.

## Read the active scope

```python
from ask_shell.console import get_live_print_context, live_print_scope

with live_print_scope(prefix="[prod] "):
    ctx = get_live_print_context()
    print(repr(ctx.prefix if ctx else ""))
    #> '[prod] '
```

## Suppress live output

```python
from ask_shell.console import get_live_print_context, live_print_scope

with live_print_scope(suppress=True):
    ctx = get_live_print_context()
    print(ctx.suppress if ctx else False)
    #> True
```

Nested scopes restore the outer context when the inner block exits.

```python
from ask_shell.console import get_live_print_context, live_print_scope

with live_print_scope(prefix="outer "):
    outer = get_live_print_context()
    with live_print_scope(prefix="inner "):
        inner = get_live_print_context()
    after = get_live_print_context()
print(f"{outer.prefix}|{inner.prefix}|{after.prefix}")
#> outer |inner |outer
```

## Context at run_pool submit time

Set `live_print_scope` in the thread that calls `submit`. Each worker sees the scope that was active for its submit call.

```python
from threading import Barrier

from ask_shell.console import get_live_print_context, live_print_scope
from ask_shell.shell import run_pool

results: list[str] = []
barrier = Barrier(2)


def worker() -> None:
    barrier.wait()
    ctx = get_live_print_context()
    results.append(ctx.prefix if ctx else "")


with run_pool("demo", total=2, pool_thread_count=2, max_concurrent_submits=2) as pool:
    with live_print_scope(prefix="a"):
        f_a = pool.submit(worker)
    with live_print_scope(prefix="b"):
        f_b = pool.submit(worker)
    f_a.result()
    f_b.result()

print(sorted(results))
#> ['a', 'b']
```
