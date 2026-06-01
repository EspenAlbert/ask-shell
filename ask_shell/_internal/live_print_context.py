from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Iterator


@dataclass
class LivePrintContext:
    prefix: str = ""
    suppress: bool = False


_live_print_ctx: ContextVar[LivePrintContext | None] = ContextVar("live_print_ctx", default=None)


def get_live_print_context() -> LivePrintContext | None:
    return _live_print_ctx.get()


@contextmanager
def live_print_scope(*, prefix: str = "", suppress: bool = False) -> Iterator[None]:
    token = _live_print_ctx.set(LivePrintContext(prefix=prefix, suppress=suppress))
    try:
        yield
    finally:
        _live_print_ctx.reset(token)
