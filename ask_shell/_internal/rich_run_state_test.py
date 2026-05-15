from unittest.mock import Mock, patch

import pytest

from ask_shell._internal.events import ShellRunAfter, ShellRunStdOutput
from ask_shell._internal.models import (
    ShellConfig,
    ShellRun,
)
from ask_shell._internal.rich_live import get_live
from ask_shell._internal.rich_run_state import _RunState
from ask_shell.settings import ShellRunSummary


def test_run_with_output_is_logged_to_console(settings, capture_console, caplog):
    config = ShellConfig(
        shell_input='echo "Hello, World!"',
        print_prefix="Test Run",
        settings=settings,
    )
    run = ShellRun(config=config)
    state = _RunState()
    assert not get_live().is_started
    state.add_run(run)
    assert get_live().is_started
    assert state.active_runs == [run]
    assert state.no_user_input_runs
    run._on_event(
        ShellRunStdOutput(
            is_stdout=True,
            content="Hello, World!\n",
        ),
    )
    run._on_event(
        ShellRunStdOutput(
            is_stdout=False,
            content="This is an error message.\n",
        )
    )
    run._on_event(ShellRunAfter(run=run, error=Exception("Test error")))
    state.remove_run(run, error=Exception("Test error"))
    output = capture_console.end_capture()
    assert "Test Run" in output
    assert "Hello, World!" in output
    assert "This is an error message." in output
    assert "Test error" in output
    log_output = caplog.text
    assert "❌ " in log_output
    assert 'echo "Hello, World!"\'' in log_output
    assert not get_live().is_started


def test_skip_progress_output(settings, capture_console):
    config = ShellConfig(
        shell_input='echo "Hello, World!"',
        print_prefix="Test Run",
        settings=settings,
        skip_progress_output=True,
    )
    run = ShellRun(config=config)
    state = _RunState()
    assert not get_live().is_started
    state.add_run(run)
    assert get_live().is_started
    assert state.active_runs == [run]
    assert state.no_user_input_runs
    run._on_event(
        ShellRunStdOutput(
            is_stdout=True,
            content="Hello, World!\n",
        ),
    )
    run._on_event(
        ShellRunStdOutput(
            is_stdout=False,
            content="This is an error message.\n",
        )
    )
    run._on_event(ShellRunAfter(run=run, error=Exception("Test error")))
    state.remove_run(run, error=Exception("Test error"))
    output = capture_console.end_capture()
    assert "..." in output  # Output is skipped


@pytest.mark.parametrize(
    ("summary", "exit_code", "expect_log"),
    [
        (ShellRunSummary.ERRORS_ONLY, 0, False),
        (ShellRunSummary.ERRORS_ONLY, 1, True),
        (ShellRunSummary.ALL, 0, True),
    ],
)
@patch("ask_shell._internal.rich_run_state.log_task_done")
def test_remove_run_respects_shell_run_summary(mock_log_done, settings, summary, exit_code, expect_log):
    cfg = ShellConfig(
        shell_input='echo "x"',
        settings=settings.model_copy(update={"shell_run_summary": summary}),
    )
    run = ShellRun(config=cfg)
    proc = Mock(spec=["returncode"])
    proc.returncode = exit_code
    run.p_open = proc
    state = _RunState()
    state.add_run(run)
    state.remove_run(run, error=None)
    if expect_log:
        mock_log_done.assert_called_once()
    else:
        mock_log_done.assert_not_called()


@patch("ask_shell._internal.rich_run_state.log_task_done")
def test_remove_run_mute_shell_summary_skips_log(mock_log_done, settings):
    cfg = ShellConfig(
        shell_input='echo "x"',
        settings=settings,
        mute_shell_summary=True,
    )
    run = ShellRun(config=cfg)
    proc = Mock(spec=["returncode"])
    proc.returncode = 1
    run.p_open = proc
    state = _RunState()
    state.add_run(run)
    state.remove_run(run, error=None)
    mock_log_done.assert_not_called()
