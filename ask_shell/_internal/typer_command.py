import logging
import os
import sys
import traceback
from contextlib import suppress
from functools import wraps
from pathlib import Path
from types import TracebackType
from typing import Callable, NoReturn, TypeVar

import typer
from rich.logging import RichHandler
from rich.traceback import Traceback

import ask_shell
from ask_shell._internal.non_interactive import (
    NonInteractivePromptError,
    PromptSessionLockedError,
    prompt_session_lock,
)
from ask_shell._internal.prompt_file import ensure_session_header, load_prompt_file
from ask_shell._internal.rich_live import get_live_console, log_to_live
from ask_shell._internal.rich_progress import _is_clean_exit, new_task
from ask_shell.settings import AskShellSettings, default_rich_info_style, path_under_cache_root

T = TypeVar("T", bound=Callable)
original_excepthook = sys.excepthook


def log_exit_summary(settings: AskShellSettings):
    log_to_live(f"{default_rich_info_style()}You can find the run logs in {settings.run_logs} ")


def _print_prompt_error_contract(exc: BaseException, settings: AskShellSettings) -> None:
    log_to_live(str(exc))
    log_to_live("Re-run the same command after editing.")
    log_to_live(settings.prompt_path_export_line())
    live = settings.non_interactive_prompt_file
    if live.exists():
        doc, _ = load_prompt_file(live)
        if doc.session and doc.session.pinned:
            log_to_live("This prompt file stays pinned after the first unanswered dump.")


def _hint_prompt_file_on_error(settings: AskShellSettings) -> None:
    live = settings.non_interactive_prompt_file
    if live.exists():
        log_to_live(f"Prompt session file left at {live}. Re-run to replay. Delete the file to start over.")
        log_to_live(settings.prompt_path_export_line())


def _fail_prompt_session(exc: BaseException, settings: AskShellSettings) -> NoReturn:
    _print_prompt_error_contract(exc, settings)
    raise typer.Exit(1) from None


def except_hook_custom(
    skip_rich_exception: bool,
) -> Callable[[type[BaseException], BaseException, TracebackType | None], None]:
    def except_hook(
        exc_type: type[BaseException],
        exc_value: BaseException,
        tb: TracebackType | None,
    ) -> None:
        """Similar to typer's except hook"""
        internal_modules = [typer, ask_shell]
        console = get_live_console()
        rich_tb = Traceback.from_exception(
            exc_type,
            exc_value,
            tb,
            show_locals=True,
            suppress=internal_modules,
            width=console.width,
        )
        if not skip_rich_exception:
            console.print(rich_tb)
        standard_exception = traceback.TracebackException(exc_type, exc_value, tb, limit=-7, compact=True)
        for line in standard_exception.format(chain=True):
            console.print(line, end="")

    return except_hook


def track_progress_decorator(
    *,
    settings: AskShellSettings,
    skip_except_hook: bool = False,
    use_app_name_command_for_logs: bool = True,
    app_name: str,
    command_name: str,
    skip_rich_exception: bool = False,
) -> Callable[[T], T]:
    def decorator(command: T) -> T:
        @wraps(command)
        def wrapper(*args, **kwargs):
            if (
                not skip_except_hook
            ):  # this must be done inside of the call as the typer.main sets the except hook when the app is called
                sys.excepthook = except_hook_custom(skip_rich_exception)
            if use_app_name_command_for_logs:
                settings.configure_run_logs_dir_if_unset(new_relative_path=f"{app_name}/{command_name}")
            settings.finalize_non_interactive_prompt_path(app_name=app_name, command_name=command_name)
            session_command = f"{app_name}/{command_name}"
            sys_args = " ".join(sys.argv)
            with new_task(
                description=f"Running: '{sys_args}'",
            ):
                try:
                    with prompt_session_lock(settings):
                        ensure_session_header(
                            settings.non_interactive_prompt_file,
                            command=session_command,
                            pinned=not path_under_cache_root(settings.non_interactive_prompt_file, settings.cache_root),
                        )
                        try:
                            result = command(*args, **kwargs)
                        except (NonInteractivePromptError, PromptSessionLockedError) as exc:
                            _fail_prompt_session(exc, settings)
                        except BaseException as exc:
                            if _is_clean_exit(exc):
                                settings.archive_non_interactive_prompt_file()
                                raise
                            _hint_prompt_file_on_error(settings)
                            raise
                        settings.archive_non_interactive_prompt_file()
                        return result
                except PromptSessionLockedError as exc:
                    _fail_prompt_session(exc, settings)
                finally:
                    log_exit_summary(settings)

        return wrapper  # type: ignore

    return decorator


def _wrap_typer_tree_commands(
    app: typer.Typer,
    *,
    settings: AskShellSettings,
    log_path_prefix: str,
    skip_except_hook: bool,
    use_app_name_command_for_logs: bool,
    render_rich_error_on_sys_exit: bool,
) -> None:
    for command in app.registered_commands:
        command.callback = track_progress_decorator(
            skip_except_hook=skip_except_hook,
            settings=settings,
            use_app_name_command_for_logs=use_app_name_command_for_logs,
            app_name=log_path_prefix,
            command_name=command.name or command.callback.__name__,  # type: ignore
            skip_rich_exception=not render_rich_error_on_sys_exit,
        )(
            command.callback  # type: ignore
        )
    for group in app.registered_groups:
        nested = group.typer_instance
        if nested is None:
            continue
        segment = group.name or nested.info.name or "group"
        child_prefix = f"{log_path_prefix}/{segment}"
        _wrap_typer_tree_commands(
            nested,
            settings=settings,
            log_path_prefix=child_prefix,
            skip_except_hook=skip_except_hook,
            use_app_name_command_for_logs=use_app_name_command_for_logs,
            render_rich_error_on_sys_exit=render_rich_error_on_sys_exit,
        )


def remove_secrets(message: str, secrets: list[str]) -> str:
    for secret in secrets:
        message = message.replace(secret, "***")
    return message


class SecretsHider(logging.Filter):
    def __init__(self, secrets: list[str], name: str = "") -> None:
        self.secrets = secrets
        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.msg
        if isinstance(msg, str):
            record.msg = remove_secrets(msg, self.secrets)
        return True


dangerous_keys = ["key", "token", "secret"]
safe_keys: list[str] = ["/"]


def hide_secrets(handler: logging.Handler, secrets_dict: dict[str, str]) -> None:
    secrets_to_hide = set()
    for key, value in secrets_dict.items():
        if not isinstance(value, str):
            continue
        key_lower = key.lower()
        if value.lower() in {"true", "false"} or value.isdigit():
            continue
        with suppress(Exception):
            if Path(value).exists():
                continue
        if any(safe in key_lower for safe in safe_keys):
            continue
        if any(danger_key_part in key_lower for danger_key_part in dangerous_keys):
            secrets_to_hide.add(value)
    if not secrets_to_hide:
        return
    handler.addFilter(SecretsHider(list(secrets_to_hide), name="secrets-hider"))


def configure_logging(
    app: typer.Typer,
    *,
    settings: AskShellSettings | None = None,
    app_pretty_exceptions_enable: bool = False,
    app_pretty_exceptions_show_locals: bool = False,
    skip_except_hook: bool = False,
    use_app_name_command_for_logs: bool = True,
    render_rich_error_on_sys_exit: bool = False,
) -> logging.Handler:
    settings = settings or AskShellSettings.from_env()
    root_prefix = app.info.name or "typer_app"
    _wrap_typer_tree_commands(
        app,
        settings=settings,
        log_path_prefix=root_prefix,
        skip_except_hook=skip_except_hook,
        use_app_name_command_for_logs=use_app_name_command_for_logs,
        render_rich_error_on_sys_exit=render_rich_error_on_sys_exit,
    )
    handler = RichHandler(rich_tracebacks=False, level=settings.log_level, console=get_live_console())
    logging.basicConfig(
        level=settings.log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[handler],
    )
    if settings.remove_os_secrets:
        hide_secrets(handler, {**os.environ})
    app.pretty_exceptions_enable = app_pretty_exceptions_enable
    app.pretty_exceptions_show_locals = app_pretty_exceptions_show_locals
    return handler
