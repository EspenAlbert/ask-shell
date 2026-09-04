import os
import re
import shlex
from pathlib import Path

import pytest
from zero_3rdparty import file_utils

from ask_shell import settings as settings_mod
from ask_shell.settings import AskShellSettings


@pytest.mark.skipif(os.environ.get("SLOW", "") == "", reason="needs os.environ[SLOW]")
def test_using_run_logs_dir_and_adding_1000_dirs_should_not_clean_it(tmp_path, settings):
    run_logs_dir = settings.run_logs_dir = tmp_path / "run_logs"
    assert (
        settings.configure_run_logs_dir_if_unset(new_absolute_path=run_logs_dir, skip_env_update=True) == run_logs_dir
    )
    for i in range(100):
        run_dir = settings.next_run_logs_dir(f"test-{i}")
        if i == 0:
            assert run_dir.name == "001_test-0"
        elif i == 99:
            assert run_dir.name == "100_test-99"
        run_dir.mkdir(parents=True, exist_ok=True)
    assert len(list(run_logs_dir.iterdir())) == 100
    last_dir = settings.next_run_logs_dir("test-100")
    last_dir.mkdir(parents=True, exist_ok=True)
    assert last_dir.name == "101_test-100"
    assert len(list(run_logs_dir.iterdir())) == 101, "Run logs directory should be cleaned up"
    for i in range(1_000):
        run_dir = settings.next_run_logs_dir(f"test-{i}")
        run_dir.mkdir(parents=True, exist_ok=True)
        if i == 999:
            assert run_dir.name == "1101_test-999"


def test_configure_run_logs_dir_if_unset(tmp_path, settings):
    cache_root = settings.cache_root
    assert cache_root == tmp_path / "cache/ask_shell"
    new_run_logs_dir = settings.configure_run_logs_dir_if_unset(
        new_relative_path="my-app/test-command",
        skip_env_update=True,
        date_folder_expressing=None,
    )
    assert new_run_logs_dir == cache_root / "my-app/test-command"
    settings.run_logs_dir = None
    re_configured = settings.configure_run_logs_dir_if_unset(
        new_relative_path="my-app/test-command", skip_env_update=True
    )
    assert re_configured != new_run_logs_dir
    assert re_configured.name.endswith("Z")


def test_default_prompt_file_uses_classvar_filename(settings):
    assert AskShellSettings.NON_INTERACTIVE_PROMPT_FILENAME == "non_interactive_prompt.yaml"
    assert (
        settings.non_interactive_prompt_file == settings.cache_root / AskShellSettings.NON_INTERACTIVE_PROMPT_FILENAME
    )
    assert settings.use_defaults


def test_configure_prompt_path_if_unset_and_noop(settings):
    filename = AskShellSettings.NON_INTERACTIVE_PROMPT_FILENAME
    first = settings.configure_non_interactive_prompt_path_if_unset(
        new_relative_dir="my-app/leaf", skip_env_update=True
    )
    assert first == settings.cache_root / "my-app" / "leaf" / filename
    assert first.name == filename
    second = settings.configure_non_interactive_prompt_path_if_unset(new_relative_dir="other", skip_env_update=True)
    assert second == first
    pinned = settings.cache_root / "pinned.yaml"
    settings.non_interactive_prompt_path = pinned
    assert settings.configure_non_interactive_prompt_path_if_unset(new_relative_dir="ignored") == pinned


@pytest.mark.parametrize(
    ("yaml", "app", "cmd", "expected_suffix"),
    [
        (
            "session:\n  command: adoc/gh_rr\n  pinned: false\nquestions: []\n",
            "adoc",
            "gh_rr",
            "adoc/gh_rr",
        ),
        (
            "session:\n  command: adoc/gh_rr\n  pinned: true\nquestions: []\n",
            "pkg-ext",
            "pre_commit",
            "adoc/gh_rr",
        ),
        ("questions: []\n", "pkg-ext", "pre_commit", "pkg-ext/pre_commit"),
    ],
    ids=["same-command", "pinned-foreign", "legacy-foreign"],
)
def test_resolve_non_interactive_prompt_path(settings, yaml, app, cmd, expected_suffix):
    filename = AskShellSettings.NON_INTERACTIVE_PROMPT_FILENAME
    parent = settings.cache_root / "adoc" / "gh_rr" / filename
    file_utils.ensure_parents_write_text(parent, yaml)
    settings.non_interactive_prompt_path = parent
    resolved = settings.resolve_non_interactive_prompt_path(app_name=app, command_name=cmd)
    assert resolved == settings.cache_root / Path(*expected_suffix.split("/")) / filename


def test_configure_prompt_path_writes_env(settings):
    path = settings.configure_non_interactive_prompt_path_if_unset(new_relative_dir="my-app/leaf")
    assert os.environ[AskShellSettings.ENV_NAME_NON_INTERACTIVE_PROMPT_PATH] == str(path)
    loaded = AskShellSettings.from_env()
    assert loaded.non_interactive_prompt_file == path
    assert AskShellSettings.ENV_NAME_NON_INTERACTIVE_PROMPT_PATH in settings.prompt_path_export_line()
    assert str(path.resolve()) in settings.prompt_path_export_line()


def test_configure_prompt_path_requires_dir_or_absolute(settings):
    with pytest.raises(ValueError, match="Either new_absolute_path or new_relative_dir must be provided"):
        settings.configure_non_interactive_prompt_path_if_unset()


def test_prompt_path_export_line_escapes_single_quotes(settings, tmp_path):
    path = tmp_path / "agent's" / AskShellSettings.NON_INTERACTIVE_PROMPT_FILENAME
    settings.non_interactive_prompt_path = path
    export_line = settings.prompt_path_export_line()
    expected = f"export {AskShellSettings.ENV_NAME_NON_INTERACTIVE_PROMPT_PATH}={shlex.quote(str(path.resolve()))}"
    assert export_line == expected


def test_archive_prompt_file_and_collision(settings, monkeypatch):
    filename = AskShellSettings.NON_INTERACTIVE_PROMPT_FILENAME
    live = settings.non_interactive_prompt_file
    assert settings.archive_non_interactive_prompt_file() is None
    file_utils.ensure_parents_write_text(live, "questions: []\n")
    archived = settings.archive_non_interactive_prompt_file()
    assert archived is not None
    assert not live.exists()
    assert archived.name.startswith("20")
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z_", archived.name)
    assert archived.name.endswith(f"_{filename}")
    stamp = "2026-09-03T20-18-00Z"
    monkeypatch.setattr(settings_mod, "_utc_archive_stamp", lambda: stamp)
    file_utils.ensure_parents_write_text(live, "again\n")
    taken = live.with_name(f"{stamp}_{filename}")
    file_utils.ensure_parents_write_text(taken, "taken\n")
    collided = settings.archive_non_interactive_prompt_file()
    assert collided == live.with_name(f"{stamp}-2_{filename}")
    assert collided.read_text() == "again\n"
