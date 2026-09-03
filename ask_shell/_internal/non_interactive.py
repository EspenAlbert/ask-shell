from __future__ import annotations

import contextvars
import errno
import fcntl
import os
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from model_lib import dump, parse
from model_lib.constants import FileFormat
from model_lib.errors import PayloadError
from pydantic import ValidationError
from zero_3rdparty import file_utils

from ask_shell._internal.interactive_models import (
    ChoiceTyped,
    ConfirmQuestion,
    MultiSelectStatus,
    NonInteractivePromptFile,
    PromptKind,
    PromptQuestion,
    SelectAlternative,
    SelectMultipleQuestion,
    SelectQuestion,
    TextQuestion,
)
from ask_shell.settings import AskShellSettings

_UNDECIDED = "undecided"
_replay_index = 0
_lock_fd: contextvars.ContextVar[int | None] = contextvars.ContextVar("_prompt_session_lock_fd", default=None)


class NonInteractivePromptError(Exception):
    def __init__(self, path: Path, *, parse_error: str | None = None) -> None:
        self.path = path
        lines = [f"Non-interactive prompt needs an answer in {path}."]
        if parse_error:
            lines.append(f"Could not parse the existing file: {parse_error}")
        lines.append("Set the last question's response, chosen, checked, or status, then re-run the same command.")
        super().__init__("\n".join(lines))


class PromptSessionLockedError(Exception):
    def __init__(self, path: Path, lock_path: Path) -> None:
        self.path = path
        self.lock_path = lock_path
        super().__init__(f"Prompt session is locked by another process: {path} (lock {lock_path}).")


@contextmanager
def prompt_session_lock(settings: AskShellSettings) -> Iterator[None]:
    if _lock_fd.get() is not None:
        yield
        return
    lock_path = settings.non_interactive_prompt_lock_file
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        os.close(fd)
        if exc.errno not in {errno.EAGAIN, errno.EWOULDBLOCK, errno.EACCES}:
            raise
        raise PromptSessionLockedError(settings.non_interactive_prompt_file, lock_path) from None
    token = _lock_fd.set(fd)
    try:
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
        _lock_fd.reset(token)


def try_replay_answered(
    *,
    kind: PromptKind,
    prompt: str,
    settings: AskShellSettings,
    choices: Sequence[ChoiceTyped] = (),
) -> Any | None:
    if kind in {PromptKind.SELECT, PromptKind.SELECT_MULTIPLE}:
        assert choices, f"choices must not be empty for {kind}"
    with prompt_session_lock(settings):
        return _try_replay_answered(kind=kind, prompt=prompt, settings=settings, choices=choices)


def record_answered_row(
    *,
    kind: PromptKind,
    prompt: str,
    settings: AskShellSettings,
    value: Any,
    choices: Sequence[ChoiceTyped] = (),
) -> None:
    if kind in {PromptKind.SELECT, PromptKind.SELECT_MULTIPLE}:
        assert choices, f"choices must not be empty for {kind}"
    with prompt_session_lock(settings):
        _record_answered_row(kind=kind, prompt=prompt, settings=settings, choices=choices, value=value)


def replay_or_dump(
    *,
    kind: PromptKind,
    prompt: str,
    settings: AskShellSettings,
    choices: Sequence[ChoiceTyped] = (),
) -> Any:
    if kind in {PromptKind.SELECT, PromptKind.SELECT_MULTIPLE}:
        assert choices, f"choices must not be empty for {kind}"
    with prompt_session_lock(settings):
        return _replay_or_dump(kind=kind, prompt=prompt, settings=settings, choices=choices)


def _try_replay_answered(
    *,
    kind: PromptKind,
    prompt: str,
    settings: AskShellSettings,
    choices: Sequence[ChoiceTyped],
) -> Any | None:
    global _replay_index
    doc, _ = _load_prompt_file(settings.non_interactive_prompt_file)
    current = doc.questions[_replay_index] if _replay_index < len(doc.questions) else None
    if current is None or current.kind != kind or current.prompt != prompt or not _row_is_answered(current, choices):
        return None
    value = _row_value(current, choices)
    _replay_index += 1
    return value


def _record_answered_row(
    *,
    kind: PromptKind,
    prompt: str,
    settings: AskShellSettings,
    choices: Sequence[ChoiceTyped],
    value: Any,
) -> None:
    global _replay_index
    path = settings.non_interactive_prompt_file
    doc, _ = _load_prompt_file(path)
    doc.questions = doc.questions[:_replay_index]
    doc.questions.append(_answered_row_from_value(kind, prompt, choices, value))
    _atomic_write(path, doc)
    _replay_index += 1


def _replay_or_dump(
    *,
    kind: PromptKind,
    prompt: str,
    settings: AskShellSettings,
    choices: Sequence[ChoiceTyped],
) -> Any:
    global _replay_index
    path = settings.non_interactive_prompt_file
    doc, parse_error = _load_prompt_file(path)
    questions = doc.questions
    current = questions[_replay_index] if _replay_index < len(questions) else None
    if current is None or current.kind != kind or current.prompt != prompt or not _row_is_answered(current, choices):
        doc.questions = questions[:_replay_index]
        doc.questions.append(_undecided_row(kind, prompt, choices))
        _atomic_write(path, doc)
        raise NonInteractivePromptError(path, parse_error=parse_error)
    value = _row_value(current, choices)
    _replay_index += 1
    return value


def _load_prompt_file(path: Path) -> tuple[NonInteractivePromptFile, str | None]:
    if path.exists() and path.stat().st_size > 0:
        try:
            return parse.parse_model(path, t=NonInteractivePromptFile, format=FileFormat.yaml), None
        except (PayloadError, ValidationError) as exc:
            return NonInteractivePromptFile(), str(exc)
    return NonInteractivePromptFile(), None


def _atomic_write(path: Path, doc: NonInteractivePromptFile) -> None:
    content = dump.dump_as_str(doc.model_dump(mode="json", exclude_none=True), FileFormat.yaml)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    file_utils.ensure_parents_write_text(tmp, content)
    os.replace(tmp, path)


def _alternatives(choices: Sequence[ChoiceTyped]) -> list[SelectAlternative]:
    return [SelectAlternative(name=choice.name, description=choice.description) for choice in choices]


def _answered_row_from_value(
    kind: PromptKind,
    prompt: str,
    choices: Sequence[ChoiceTyped],
    value: Any,
) -> PromptQuestion:
    alternatives = _alternatives(choices)
    match kind:
        case PromptKind.CONFIRM:
            return ConfirmQuestion(prompt=prompt, response=value)
        case PromptKind.TEXT:
            return TextQuestion(prompt=prompt, response=value)
        case PromptKind.SELECT:
            name = next(choice.name for choice in choices if choice.value == value)
            return SelectQuestion(prompt=prompt, alternatives=alternatives, chosen=name)
        case PromptKind.SELECT_MULTIPLE:
            checked = [choice.name for choice in choices if choice.value in value]
            return SelectMultipleQuestion(
                prompt=prompt,
                alternatives=alternatives,
                status=MultiSelectStatus.ANSWERED,
                checked=checked,
            )
        case _:
            raise ValueError(f"unsupported prompt kind: {kind}")


def _undecided_row(kind: PromptKind, prompt: str, choices: Sequence[ChoiceTyped]) -> PromptQuestion:
    alternatives = _alternatives(choices)
    match kind:
        case PromptKind.CONFIRM:
            return ConfirmQuestion(prompt=prompt)
        case PromptKind.TEXT:
            return TextQuestion(prompt=prompt)
        case PromptKind.SELECT:
            return SelectQuestion(prompt=prompt, alternatives=alternatives)
        case PromptKind.SELECT_MULTIPLE:
            return SelectMultipleQuestion(prompt=prompt, alternatives=alternatives)
        case _:
            raise ValueError(f"unsupported prompt kind: {kind}")


def _choice_names(choices: Sequence[ChoiceTyped]) -> set[str]:
    return {choice.name for choice in choices}


def _row_is_answered(row: PromptQuestion, choices: Sequence[ChoiceTyped]) -> bool:
    names = _choice_names(choices)
    match row:
        case ConfirmQuestion(response=bool()):
            return True
        case TextQuestion(response=str() as text) if text != _UNDECIDED:
            return True
        case SelectQuestion(chosen=str() as name) if name and name in names:
            return True
        case SelectMultipleQuestion(status=status, checked=checked) if (
            status == MultiSelectStatus.ANSWERED and set(checked) <= names
        ):
            return True
        case _:
            return False


def _row_value(row: PromptQuestion, choices: Sequence[ChoiceTyped]) -> Any:
    match row:
        case ConfirmQuestion(response=bool() as response):
            return response
        case TextQuestion(response=str() as text):
            return text
        case SelectQuestion(chosen=str() as name):
            return next(choice.value for choice in choices if choice.name == name)
        case SelectMultipleQuestion(checked=checked):
            return [next(choice.value for choice in choices if choice.name == name) for name in checked]
        case _:
            raise RuntimeError("answered row missing a value mapping")
