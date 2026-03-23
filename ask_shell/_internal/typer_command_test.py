import pytest
import typer

from ask_shell._internal import typer_command


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
