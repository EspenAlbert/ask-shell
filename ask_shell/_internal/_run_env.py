import logging
import os
import sys
from functools import lru_cache
from os import getenv

from zero_3rdparty.run_env import in_test_env, running_in_container_environment

from ask_shell.settings import AskShellSettings, _global_settings

logger = logging.getLogger(__name__)


def _not_interactive_reason() -> str:
    if in_test_env():
        return "Running in test environment"
    if getenv("TERM", "") in ("dumb", "unknown"):
        return "TERM environment variable is set to 'dumb' or 'unknown'"
    if not sys.stdout.isatty():
        return "Standard output is not a TTY"
    if getenv("CI", "false").lower() in ("true", "1", "yes"):
        return "Running in CI environment"
    if running_in_container_environment():
        return "Running in container environment"
    return ""


@lru_cache
def interactive_shell() -> bool:
    settings = AskShellSettings.from_env()
    if settings.disable_interactive_shell:
        logger.debug(
            f"Interactive shell disabled by environment variable {settings.ENV_NAME_DISABLE_INTERACTIVE_SHELL}"
        )
        return False
    if settings.force_interactive_shell:
        logger.debug(
            f"Interactive shell forced by environment variable {_global_settings.ENV_NAME_FORCE_INTERACTIVE_SHELL}"
        )
        return True
    if non_interactive_reason := _not_interactive_reason():
        logger.debug(f"Interactive shell not available: {non_interactive_reason}")
        return False
    return True


def disable_interactive_shell() -> None:
    """Force non-interactive mode for the remainder of this process."""
    os.environ[AskShellSettings.ENV_NAME_DISABLE_INTERACTIVE_SHELL] = "true"
    interactive_shell.cache_clear()


def resolve_terminal_dimensions(
    settings: AskShellSettings | None = None,
) -> tuple[int | None, int | None]:
    if interactive_shell():
        return None, None
    settings = settings or AskShellSettings.from_env()
    return settings.terminal_width, settings.terminal_height
