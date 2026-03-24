import logging

import pytest
import typer

from ask_shell._internal import typer_command


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
