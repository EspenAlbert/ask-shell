import os
from unittest.mock import Mock

import pytest
from model_lib import StaticSettings
from rich.console import Console
from zero_3rdparty.file_utils import ensure_parents_write_text

from ask_shell._internal._run import stop_runs_and_pool
from ask_shell._internal.models import ShellConfig, ShellRun
from ask_shell._internal.rich_live import get_live, reset_live
from ask_shell._internal.rich_progress import get_default_progress_manager
from ask_shell.settings import ENV_PREFIX, AskShellSettings


@pytest.fixture(autouse=True)
def _isolate_ask_shell_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(AskShellSettings.ENV_NAME_NON_INTERACTIVE_PROMPT_PATH, raising=False)
    monkeypatch.delenv("RUN_LOGS_DIR", raising=False)
    monkeypatch.delenv(f"{ENV_PREFIX}RUN_LOGS_DIR", raising=False)


@pytest.fixture(autouse=True)
def settings(static_env_vars: StaticSettings, _isolate_ask_shell_env: None) -> AskShellSettings:
    return AskShellSettings.from_env(global_callback_strings=[], **static_env_vars.model_dump())


tf_example = """\
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "2.4.1"
    }
  }
}
"""


@pytest.fixture()
def tf_dir(settings):
    """Fixture to create a temporary directory with a Terraform example."""
    if os.environ.get("SLOW", "") == "":
        pytest.skip("needs os.environ[SLOW]")
    tf_path = settings.static_root / "terraform_example/main.tf"
    ensure_parents_write_text(tf_path, tf_example)
    return tf_path.parent


@pytest.fixture(scope="session", autouse=True)
def stop_consumer():
    yield
    stop_runs_and_pool()


@pytest.fixture(autouse=True)
def reset_progress_fix():
    progress_manager = get_default_progress_manager()
    progress_manager.reset_progress()


# https://github.com/Textualize/rich/blob/8c4d3d1d50047e3aaa4140d0ffc1e0c9f1df5af4/tests/test_live.py#L11
def create_capture_console(*, width: int = 60, height: int = 80, force_terminal: bool = True) -> Console:
    return Console(
        width=width,
        height=height,
        force_terminal=force_terminal,
        legacy_windows=False,
        color_system=None,  # use no color system to reduce complexity of output,
        _environ={},
    )


@pytest.fixture()
def capture_console() -> Console:  # type: ignore
    """
    Fixture to capture output from the console.
    """
    console = create_capture_console()
    console.begin_capture()
    live = get_live()
    live.console = console
    yield console
    console.end_capture()
    reset_live()


def create_run_mocked_config(user_input: bool = False) -> ShellRun:
    mock_settings = AskShellSettings.for_testing(global_callback_strings=[], remove_os_secrets=False)
    return ShellRun(
        config=Mock(
            spec=ShellConfig,
            message_callbacks=[],
            user_input=user_input,
            print_prefix="Mocked Run",
            shell_input="echo 'Mocked Run Output'",
            skip_progress_output=False,
            mute_shell_summary=False,
            allow_non_zero_exit=False,
            settings=mock_settings,
        )
    )
