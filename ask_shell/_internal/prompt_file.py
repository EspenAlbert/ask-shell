from __future__ import annotations

import os
from pathlib import Path

from model_lib import dump, parse
from model_lib.constants import FileFormat
from model_lib.errors import PayloadError
from pydantic import ValidationError
from zero_3rdparty import file_utils

from ask_shell._internal.interactive_models import NonInteractivePromptFile, PromptSession


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


def ensure_session_header(path: Path, *, command: str, pinned: bool = False) -> None:
    doc, _ = load_prompt_file(path)
    if doc.session is not None and doc.session.command == command and doc.session.pinned == pinned:
        return
    doc.session = PromptSession(command=command, pinned=pinned or (doc.session.pinned if doc.session else False))
    write_prompt_file(path, doc)
