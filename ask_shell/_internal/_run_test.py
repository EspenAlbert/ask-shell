from rich.ansi import AnsiDecoder

from ask_shell._internal._run import _log_line, run_and_wait
from ask_shell._internal.events import ShellRunStdOutput
from ask_shell._internal.live_print_context import get_live_print_context, live_print_scope


def test_log_line_strips_ansi_when_enabled():
    decoder = AnsiDecoder()
    raw = "\x1b[32mgreen\x1b[0m\n"
    assert _log_line(raw, ansi_content=True, decoder=decoder) == "green\n"
    assert _log_line(raw, ansi_content=False, decoder=decoder) == raw


def test_message_callback_inherits_live_print_scope() -> None:
    seen: list[str | None] = []

    def cb(message):
        match message:
            case ShellRunStdOutput(is_stdout=True):
                ctx = get_live_print_context()
                seen.append(ctx.prefix if ctx else None)
        return False

    with live_print_scope(prefix="[test] "):
        run_and_wait("echo ok", message_callbacks=[cb], mute_shell_summary=True)
    assert "[test] " in seen


def test_message_callback_nested_scope() -> None:
    seen: list[str | None] = []

    def cb(message):
        match message:
            case ShellRunStdOutput(is_stdout=True):
                ctx = get_live_print_context()
                seen.append(ctx.prefix if ctx else None)
        return False

    with live_print_scope(prefix="outer "), live_print_scope(prefix="inner "):
        run_and_wait("echo ok", message_callbacks=[cb], mute_shell_summary=True)
    assert seen == ["inner "]
