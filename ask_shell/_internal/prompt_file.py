from __future__ import annotations

import os
from pathlib import Path

from model_lib import dump, parse
from model_lib.constants import FileFormat
from model_lib.errors import PayloadError
from pydantic import ValidationError
from zero_3rdparty import file_utils

from ask_shell._internal.interactive_models import (
    ConfirmQuestion,
    MultiSelectStatus,
    NonInteractivePromptFile,
    PromptQuestion,
    PromptSession,
    SelectMultipleQuestion,
    SelectQuestion,
    TextQuestion,
)

_UNDECIDED = "undecided"


def load_prompt_file(path: Path) -> tuple[NonInteractivePromptFile, str | None]:
    if path.exists() and path.stat().st_size > 0:
        try:
            return parse.parse_model(path, t=NonInteractivePromptFile, format=FileFormat.yaml), None
        except (PayloadError, ValidationError) as exc:
            return NonInteractivePromptFile(), str(exc)
    return NonInteractivePromptFile(), None


def write_prompt_file(path: Path, doc: NonInteractivePromptFile) -> None:
    content = dump.dump_as_str(doc.model_dump(mode="json", exclude_none=True), FileFormat.yaml)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    file_utils.ensure_parents_write_text(tmp, content)
    os.replace(tmp, path)


def _row_is_undecided(row: PromptQuestion) -> bool:
    match row:
        case ConfirmQuestion(response="undecided"):
            return True
        case TextQuestion(response="undecided"):
            return True
        case SelectQuestion(chosen=None) | SelectQuestion(chosen=""):
            return True
        case SelectMultipleQuestion(status=MultiSelectStatus.UNDECIDED):
            return True
        case _:
            return False


def prompt_session_needs_attention(doc: NonInteractivePromptFile) -> bool:
    return bool(doc.questions) and any(_row_is_undecided(row) for row in doc.questions)


def is_empty_prompt_stub(doc: NonInteractivePromptFile) -> bool:
    return not doc.questions and doc.session is not None and not doc.session.pinned


def discard_empty_prompt_stub(path: Path) -> bool:
    if not path.exists():
        return False
    doc, _ = load_prompt_file(path)
    if not is_empty_prompt_stub(doc):
        return False
    path.unlink(missing_ok=True)
    return True


def ensure_session_header(path: Path, *, command: str, pinned: bool = False) -> None:
    doc, _ = load_prompt_file(path)
    if doc.session is not None and doc.session.command == command and doc.session.pinned == pinned:
        return
    doc.session = PromptSession(command=command, pinned=pinned or (doc.session.pinned if doc.session else False))
    write_prompt_file(path, doc)
