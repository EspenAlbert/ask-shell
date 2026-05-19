from unittest.mock import patch

import pytest

from ask_shell._internal import _run_env
from ask_shell._internal._run_env import interactive_shell, resolve_terminal_dimensions
from ask_shell.settings import AskShellSettings


@pytest.fixture(autouse=True)
def _clear_interactive_cache():
    interactive_shell.cache_clear()
    yield
    interactive_shell.cache_clear()


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
