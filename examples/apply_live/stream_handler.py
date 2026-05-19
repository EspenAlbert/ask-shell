from __future__ import annotations

import json
import logging
import time
from enum import StrEnum

from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text

from ask_shell import console as ask_console
from ask_shell.console import RemoveLivePart, interactive_shell
from ask_shell.shell_events import ShellRunStdOutput

logger = logging.getLogger(__name__)

REFRESH_HEARTBEAT_INTERVAL_S = 5.0


class _Phase(StrEnum):
    REFRESH = "refresh"
    PLANNING = "planning"
    DONE = "done"


class _PlanStatusRenderable:
    def __init__(self, handler: PlanStreamHandler) -> None:
        self._handler = handler

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        status = self._handler._status_line()
        if status:
            yield status


class PlanStreamHandler:
    def __init__(self) -> None:
        self._started = time.monotonic()
        self._phase = _Phase.REFRESH
        self._in_flight: set[str] = set()
        self._done = 0
        self._planning_emitted = False
        self._diagnostic_emitted = False
        self._last_heartbeat = self._started
        self._carry = ""
        self._status = _PlanStatusRenderable(self)
        self._remove_panel: RemoveLivePart | None = ask_console.add_renderable(
            self._status, order=10, name="plan-status"
        )

    def feed_line(self, chunk: str) -> None:
        self._carry += chunk
        while "\n" in self._carry:
            line, self._carry = self._carry.split("\n", 1)
            stripped = line.strip()
            if stripped:
                self._handle_line(stripped)

    def flush(self) -> None:
        if self._carry.strip():
            self._handle_line(self._carry.strip())
        self._carry = ""
        self._remove_status_panel()

    def _handle_line(self, line: str) -> None:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            logger.debug(f"skipping non-json plan stream line: {line[:120]!r}")
            return
        msg_type = data.get("type")
        match msg_type:
            case "diagnostic":
                self._emit_diagnostic(data)
            case "refresh_start" | "apply_start":
                self._on_refresh_start(data)
            case "refresh_complete" | "apply_complete":
                self._on_refresh_complete(data)
            case "change_summary":
                if (data.get("changes") or {}).get("operation") == "apply":
                    self._phase = _Phase.DONE
            case "resource_drift" | "outputs" | "log":
                self._leave_refresh_phase()
            case _:
                pass
        self._maybe_heartbeat()

    def _emit_diagnostic(self, data: dict) -> None:
        diagnostic = data.get("diagnostic") or {}
        summary = diagnostic.get("summary")
        if not summary:
            return
        if not self._diagnostic_emitted:
            self._diagnostic_emitted = True
            ask_console.print_to_live("")
        severity = (diagnostic.get("severity") or "error").capitalize()
        ask_console.print_to_live(f"{severity}: {summary}")
        if detail := diagnostic.get("detail"):
            ask_console.print_to_live(detail)

    def _on_refresh_start(self, data: dict) -> None:
        if addr := _resource_addr(data):
            self._in_flight.add(addr)

    def _on_refresh_complete(self, data: dict) -> None:
        if addr := _resource_addr(data):
            self._in_flight.discard(addr)
        self._done += 1

    def _leave_refresh_phase(self) -> None:
        if self._phase != _Phase.REFRESH:
            return
        self._phase = _Phase.PLANNING
        self._emit_planning_once()

    def _emit_planning_once(self) -> None:
        if self._planning_emitted:
            return
        self._planning_emitted = True
        ask_console.print_to_live("plan: computing changes…")

    def _status_line(self) -> Text | None:
        if self._phase == _Phase.DONE:
            return None
        if self._phase == _Phase.PLANNING:
            return Text("planning…", style="cyan")
        return self._refresh_status(time.monotonic() - self._started)

    def _refresh_status(self, elapsed_s: float) -> Text:
        mins, secs = divmod(int(elapsed_s), 60)
        elapsed = f"{mins}m {secs:02d}s" if mins else f"{secs}s"
        return Text.assemble(
            ("refresh", "cyan"),
            " · ",
            (str(self._done), "bold"),
            " done · ",
            (str(len(self._in_flight)), "bold"),
            " running · ",
            (elapsed, "dim"),
        )

    def _maybe_heartbeat(self) -> None:
        if interactive_shell() or self._phase != _Phase.REFRESH:
            return
        now = time.monotonic()
        if now - self._last_heartbeat < REFRESH_HEARTBEAT_INTERVAL_S:
            return
        self._last_heartbeat = now
        logger.info(self._heartbeat_message(now - self._started))

    def _heartbeat_message(self, elapsed_s: float) -> str:
        mins, secs = divmod(int(elapsed_s), 60)
        elapsed = f"{mins}m {secs:02d}s" if mins else f"{secs}s"
        return f"refresh: {self._done} complete, {len(self._in_flight)} in progress ({elapsed})"

    def _remove_status_panel(self) -> None:
        if self._remove_panel is None:
            return
        self._remove_panel()
        self._remove_panel = None


def _resource_addr(data: dict) -> str | None:
    hook = data.get("hook") or {}
    resource = hook.get("resource") or {}
    addr = resource.get("addr")
    return addr if isinstance(addr, str) else None


def plan_stream_callback(handler: PlanStreamHandler):
    def callback(message) -> bool:
        match message:
            case ShellRunStdOutput(is_stdout=True, content=content):
                handler.feed_line(content)
        return False

    return callback
