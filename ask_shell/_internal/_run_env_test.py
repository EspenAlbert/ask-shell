from unittest.mock import patch

import pytest

from ask_shell._internal import _run_env
from ask_shell._internal._run_env import interactive_shell, resolve_terminal_dimensions
from ask_shell.settings import AskShellSettings


@pytest.fixture(autouse=True)
def _clear_interactive_cache(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(AskShellSettings.ENV_NAME_DISABLE_INTERACTIVE_SHELL, raising=False)
    monkeypatch.delenv(AskShellSettings.ENV_NAME_FORCE_INTERACTIVE_SHELL, raising=False)
    interactive_shell.cache_clear()
    yield
    monkeypatch.delenv(AskShellSettings.ENV_NAME_DISABLE_INTERACTIVE_SHELL, raising=False)
    monkeypatch.delenv(AskShellSettings.ENV_NAME_FORCE_INTERACTIVE_SHELL, raising=False)
    interactive_shell.cache_clear()


def test_disable_interactive_shell_forces_non_interactive(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(AskShellSettings.ENV_NAME_FORCE_INTERACTIVE_SHELL, "true")
    interactive_shell.cache_clear()
    assert interactive_shell()

    monkeypatch.setenv(AskShellSettings.ENV_NAME_DISABLE_INTERACTIVE_SHELL, "true")
    interactive_shell.cache_clear()
    assert not interactive_shell()


def test_resolve_terminal_dimensions_interactive():
    with patch.object(_run_env, "interactive_shell", return_value=True):
        assert resolve_terminal_dimensions() == (None, None)


def test_resolve_terminal_dimensions_non_interactive():
    with patch.object(_run_env, "interactive_shell", return_value=False):
        assert resolve_terminal_dimensions(AskShellSettings()) == (120, 40)


def test_resolve_terminal_dimensions_env_override(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(AskShellSettings.ENV_NAME_TERMINAL_WIDTH, "100")
    with patch.object(_run_env, "interactive_shell", return_value=False):
        assert resolve_terminal_dimensions() == (100, 40)


def test_non_tty_stdin_makes_shell_non_interactive_with_tty_stdout(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(_run_env, "in_test_env", lambda: False)
    monkeypatch.setattr(_run_env, "running_in_container_environment", lambda: False)
    monkeypatch.setenv("TERM", "xterm")
    monkeypatch.setenv("CI", "false")
    with (
        patch.object(_run_env.sys, "stdin") as stdin,
        patch.object(_run_env.sys, "stdout") as stdout,
    ):
        stdin.isatty.return_value = False
        stdout.isatty.return_value = True
        assert not interactive_shell()


@pytest.mark.parametrize(
    ("test_environment", "ci", "container", "expected_interactive"),
    [
        (False, "false", False, True),
        (True, "false", False, False),
        (False, "true", False, False),
        (False, "false", True, False),
    ],
)
def test_both_tty_streams_respect_runtime_environment(
    monkeypatch: pytest.MonkeyPatch,
    test_environment: bool,
    ci: str,
    container: bool,
    expected_interactive: bool,
):
    monkeypatch.setattr(_run_env, "in_test_env", lambda: test_environment)
    monkeypatch.setattr(_run_env, "running_in_container_environment", lambda: container)
    monkeypatch.setenv("TERM", "xterm")
    monkeypatch.setenv("CI", ci)
    with (
        patch.object(_run_env.sys, "stdin") as stdin,
        patch.object(_run_env.sys, "stdout") as stdout,
    ):
        stdin.isatty.return_value = True
        stdout.isatty.return_value = True
        assert interactive_shell() == expected_interactive
