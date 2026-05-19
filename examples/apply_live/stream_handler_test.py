from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from apply_live.stream_handler import PlanStreamHandler

_MODULE = PlanStreamHandler.__module__


def _line(payload: dict) -> str:
    return json.dumps(payload) + "\n"


@patch(f"{_MODULE}.ask_console.add_renderable")
def test_panel_removed_on_flush_only(add_mock: MagicMock) -> None:
    remove_mock = MagicMock()
    add_mock.return_value = remove_mock
    handler = PlanStreamHandler()
    handler.feed_line(_line({"type": "change_summary", "changes": {"add": 0, "operation": "apply"}}))
    remove_mock.assert_not_called()
    handler.flush()
    remove_mock.assert_called_once()


@patch(f"{_MODULE}.ask_console.add_renderable", return_value=MagicMock())
@patch(f"{_MODULE}.interactive_shell", return_value=False)
def test_ci_heartbeat_during_refresh(_interactive_mock: MagicMock, _add_mock: MagicMock) -> None:
    handler = PlanStreamHandler()
    handler._last_heartbeat = 0.0
    with patch(f"{_MODULE}.logger") as logger_mock:
        handler.feed_line(_line({"type": "refresh_start", "hook": {"resource": {"addr": "a"}}}))
        handler.feed_line(_line({"type": "refresh_complete", "hook": {"resource": {"addr": "a"}}}))
    heartbeat = logger_mock.info.call_args_list[0][0][0]
    assert "refresh:" in heartbeat
    assert "complete" in heartbeat
    assert "in progress" in heartbeat


@patch(f"{_MODULE}.ask_console.add_renderable", return_value=MagicMock())
def test_diagnostic_immediate(_add_mock: MagicMock) -> None:
    handler = PlanStreamHandler()
    with patch(f"{_MODULE}.ask_console.print_to_live") as print_mock:
        handler.feed_line(
            _line(
                {
                    "type": "diagnostic",
                    "diagnostic": {"severity": "error", "summary": "bad config", "detail": "line 1"},
                }
            )
        )
    rendered = [str(c[0][0]) for c in print_mock.call_args_list]
    assert rendered[0] == ""
    assert "Error: bad config" in rendered[1]
    assert "line 1" in rendered[2]


@patch(f"{_MODULE}.ask_console.add_renderable", return_value=MagicMock())
def test_apply_events_and_planning_status(_add_mock: MagicMock) -> None:
    handler = PlanStreamHandler()
    with patch(f"{_MODULE}.ask_console.print_to_live") as print_mock:
        handler.feed_line(_line({"type": "apply_start", "hook": {"resource": {"addr": "a"}}}))
        status = handler._status_line()
        handler.feed_line(_line({"type": "apply_complete", "hook": {"resource": {"addr": "a"}}}))
        after_complete = handler._status_line()
        handler.feed_line(_line({"type": "log", "@message": "planning"}))
    assert status is not None
    plain = status.plain
    assert "refresh" in plain
    assert "0 done" in plain
    assert "1 running" in plain
    assert after_complete is not None
    assert "1 done" in after_complete.plain
    assert "0 running" in after_complete.plain
    planning_status = handler._status_line()
    assert planning_status is not None
    assert planning_status.plain == "planning…"
    assert "plan: computing changes…" in [c[0][0] for c in print_mock.call_args_list]
