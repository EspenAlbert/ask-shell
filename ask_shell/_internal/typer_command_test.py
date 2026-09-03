import logging
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest
import typer
from zero_3rdparty import file_utils

from ask_shell._internal import typer_command
from ask_shell._internal.non_interactive import (
    NonInteractivePromptError,
    PromptSessionLockedError,
    prompt_session_lock,
)
from ask_shell.settings import AskShellSettings


def test_hide_secrets(caplog, tmp_path):
    root_logger = logging.getLogger()
    assert root_logger.handlers
    handler = root_logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    secrets = {
        "SECRET_KEY": "my_secret_value",
        "ANOTHER_KEY": "another",
        "token": "adsfadf",
        "ok": "some-value",
        "my-secret-path": str(tmp_path),
    }
    typer_command.hide_secrets(handler, secrets)
    expect_hidden = {value for key, value in secrets.items() if key not in {"ok", "my-secret-path"}}
    expect_shown = {value for key, value in secrets.items() if key in {"ok", "my-secret-path"}}
    all_vars_logged = ",".join(f"{key}={value}" for key, value in secrets.items())
    root_logger.warning(f"Logging all variables: {all_vars_logged}")
    output = caplog.text
    found_hidden = {value for value in expect_hidden if value in output}
    assert not found_hidden
    found_shown: set[str] = {value for value in expect_shown if value in output}
    assert found_shown == expect_shown, f"Expected to find {expect_shown}, but found {found_shown}"


def test_configure_logging_wraps_commands_in_nested_typers() -> None:
    root = typer.Typer(name="root")
    sub = typer.Typer(help="sub")

    @sub.command("leaf")
    def leaf() -> None:
        return None

    root.add_typer(sub, name="grp")
    nested = root.registered_groups[0].typer_instance
    assert nested is not None
    before = nested.registered_commands[0].callback
    typer_command.configure_logging(root, skip_except_hook=True)
    after = nested.registered_commands[0].callback
    assert after is not before


def test_configure_logging_skips_group_without_typer_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    root = typer.Typer(name="r")
    sub = typer.Typer(help="s")

    @sub.command("x")
    def x() -> None:
        return None

    root.add_typer(sub, name="g")
    group_info = root.registered_groups[0]
    monkeypatch.setattr(group_info, "typer_instance", None)
    typer_command.configure_logging(root, skip_except_hook=True)


def _leaf_live(settings: AskShellSettings, *parts: str) -> Path:
    return settings.cache_root.joinpath(*parts, AskShellSettings.NON_INTERACTIVE_PROMPT_FILENAME)


def _wrap(settings: AskShellSettings, fn: Callable, *, name: str = "root", cmd: str = "leaf"):
    app = typer.Typer(name=name)
    app.command(cmd)(fn)
    typer_command.configure_logging(app, settings=settings, skip_except_hook=True)
    callback = app.registered_commands[0].callback
    assert callback is not None
    return callback


def _capture_live(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    lines: list[str] = []
    monkeypatch.setattr(typer_command, "log_to_live", lambda *objs, **_: lines.append(" ".join(map(str, objs))))
    return lines


def _archives(live: Path) -> list[Path]:
    return [path for path in live.parent.glob(f"*_{live.name}") if path != live]


def test_command_scoped_and_nested_prompt_path(settings):
    seen: dict[str, Path] = {}

    def leaf() -> None:
        seen["path"] = settings.non_interactive_prompt_file

    _wrap(settings, leaf)()
    assert seen["path"] == _leaf_live(settings, "root", "leaf")
    settings.non_interactive_prompt_path = None
    root = typer.Typer(name="root")
    sub = typer.Typer()
    sub.command("leaf")(leaf)
    root.add_typer(sub, name="grp")
    typer_command.configure_logging(root, settings=settings, skip_except_hook=True)
    nested = root.registered_groups[0].typer_instance
    assert nested is not None
    callback = nested.registered_commands[0].callback
    assert callback is not None
    callback()
    assert seen["path"] == _leaf_live(settings, "root", "grp", "leaf")


def test_env_pin_is_unchanged(settings, tmp_path):
    pinned = tmp_path / "custom.yaml"
    settings.non_interactive_prompt_path = pinned
    _wrap(settings, lambda: None)()
    assert settings.non_interactive_prompt_file == pinned


def test_success_archives_live_file(settings):
    live = _leaf_live(settings, "root", "leaf")
    file_utils.ensure_parents_write_text(live, "questions: []\n")
    _wrap(settings, lambda: None)()
    assert not live.exists()
    assert len(_archives(live)) == 1


def test_success_without_live_file_is_noop(settings):
    live = _leaf_live(settings, "root", "leaf")
    _wrap(settings, lambda: None)()
    yaml_files = list(live.parent.glob("*.yaml")) if live.parent.exists() else []
    assert yaml_files == []


def test_error_keeps_live_file(settings, monkeypatch):
    live = _leaf_live(settings, "root", "leaf")
    file_utils.ensure_parents_write_text(live, "questions: []\n")
    lines = _capture_live(monkeypatch)

    def boom() -> None:
        raise RuntimeError("nope")

    with pytest.raises(RuntimeError, match="nope"):
        _wrap(settings, boom)()
    assert live.exists()
    assert _archives(live) == []
    joined = "\n".join(lines)
    assert str(live) in joined
    assert settings.prompt_path_export_line() in joined


@pytest.mark.parametrize(
    "factory",
    [
        lambda live: NonInteractivePromptError(live),
        lambda live: PromptSessionLockedError(live, Path(f"{live}.lock")),
    ],
    ids=["prompt", "locked"],
)
def test_session_errors_exit_1_without_traceback(settings, monkeypatch, factory):
    live = _leaf_live(settings, "root", "leaf")
    file_utils.ensure_parents_write_text(live, "questions: []\n")
    lines = _capture_live(monkeypatch)

    def boom() -> None:
        raise factory(live)

    with pytest.raises(typer.Exit) as exc_info:
        _wrap(settings, boom)()
    assert exc_info.value.exit_code == 1
    assert live.exists()
    assert _archives(live) == []
    joined = "\n".join(lines)
    assert str(live) in joined
    assert "Traceback" not in joined
    assert "non_interactive.py" not in joined
    assert "interactive.py" not in joined


_LOCK_CHILD = """
import sys
import typer
from ask_shell._internal import typer_command
from ask_shell.settings import AskShellSettings

settings = AskShellSettings.from_env()
app = typer.Typer(name="root")

@app.command("leaf")
def leaf():
    return None

typer_command.configure_logging(app, settings=settings, skip_except_hook=True)
try:
    app.registered_commands[0].callback()
except typer.Exit as exc:
    raise SystemExit(exc.exit_code) from None
"""


def test_overlapping_process_fails_fast(settings):
    live = _leaf_live(settings, "root", "leaf")
    file_utils.ensure_parents_write_text(live, "questions: []\n")
    settings.non_interactive_prompt_path = live
    env = os.environ | {AskShellSettings.ENV_NAME_NON_INTERACTIVE_PROMPT_PATH: str(live)}
    with prompt_session_lock(settings):
        held = subprocess.run([sys.executable, "-c", _LOCK_CHILD], env=env, capture_output=True, text=True, check=False)
        assert held.returncode == 1, held.stderr
        assert live.read_text() == "questions: []\n"
    released = subprocess.run([sys.executable, "-c", _LOCK_CHILD], env=env, capture_output=True, text=True, check=False)
    assert released.returncode == 0, released.stderr
