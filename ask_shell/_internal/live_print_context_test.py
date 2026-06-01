from unittest.mock import MagicMock, patch

from ask_shell._internal.live_print_context import live_print_scope
from ask_shell._internal.rich_live import log_to_live, print_to_live


@patch("ask_shell._internal.rich_live.get_live_console")
def test_live_print_scope_prefix(mock_get_console: MagicMock) -> None:
    console = MagicMock()
    mock_get_console.return_value = console
    with live_print_scope(prefix="[dir] "):
        print_to_live("x")
    console.print.assert_called_once()
    assert console.print.call_args[0][0] == "[dir] "


@patch("ask_shell._internal.rich_live.get_live_console")
def test_live_print_scope_suppress(mock_get_console: MagicMock) -> None:
    console = MagicMock()
    mock_get_console.return_value = console
    with live_print_scope(suppress=True):
        print_to_live("x")
        log_to_live("y")
    console.print.assert_not_called()
    console.log.assert_not_called()


@patch("ask_shell._internal.rich_live.get_live_console")
def test_nested_live_print_scope(mock_get_console: MagicMock) -> None:
    console = MagicMock()
    mock_get_console.return_value = console
    with live_print_scope(prefix="outer "):
        print_to_live("a")
        with live_print_scope(prefix="inner "):
            print_to_live("b")
        print_to_live("c")
    assert [c[0][0] for c in console.print.call_args_list] == ["outer ", "inner ", "outer "]
