from rich.ansi import AnsiDecoder

from ask_shell._internal._run import _log_line


def test_log_line_strips_ansi_when_enabled():
    decoder = AnsiDecoder()
    raw = "\x1b[32mgreen\x1b[0m\n"
    assert _log_line(raw, ansi_content=True, decoder=decoder) == "green\n"
    assert _log_line(raw, ansi_content=False, decoder=decoder) == raw
