from __future__ import annotations

import pytest
from model_lib import parse
from model_lib.constants import FileFormat
from zero_3rdparty import file_utils

from ask_shell._internal import non_interactive as ni
from ask_shell._internal.interactive_models import (
    ChoiceTyped,
    NonInteractivePromptFile,
    PromptKind,
    SelectQuestion,
)
from ask_shell._internal.non_interactive import (
    NonInteractivePromptError,
    record_answered_row,
    replay_or_dump,
    try_replay_answered,
)
from ask_shell.settings import AskShellSettings


@pytest.fixture(autouse=True)
def _reset_replay_index() -> None:
    ni._replay_index = 0


def _dump_path(settings: AskShellSettings) -> NonInteractivePromptFile:
    return parse.parse_model(settings.non_interactive_prompt_file, t=NonInteractivePromptFile, format=FileFormat.yaml)


def _as_select(question: object) -> SelectQuestion:
    match question:
        case SelectQuestion() as row:
            return row
        case _:
            raise AssertionError(f"expected select, got {type(question)}")


def _select_choices() -> list[ChoiceTyped[int]]:
    return [ChoiceTyped(name="one", value=1), ChoiceTyped(name="two", value=2)]


def test_empty_file_writes_undecided_and_raises(settings):
    path = settings.non_interactive_prompt_file
    with pytest.raises(NonInteractivePromptError, match=str(path)):
        replay_or_dump(kind=PromptKind.CONFIRM, prompt="Go?", settings=settings)
    doc = _dump_path(settings)
    assert len(doc.questions) == 1
    assert doc.questions[0].kind == PromptKind.CONFIRM
    assert doc.questions[0].prompt == "Go?"
    assert doc.session is not None
    assert doc.session.pinned


def test_answered_select_returns_choice_value(settings):
    file_utils.ensure_parents_write_text(
        settings.non_interactive_prompt_file,
        """\
questions:
  - kind: select
    prompt: Pick a number
    alternatives:
      - name: one
      - name: two
    chosen: two
""",
    )
    assert (
        replay_or_dump(kind=PromptKind.SELECT, prompt="Pick a number", settings=settings, choices=_select_choices())
        == 2
    )


def test_replays_first_then_dumps_second(settings):
    file_utils.ensure_parents_write_text(
        settings.non_interactive_prompt_file,
        """\
questions:
  - kind: select
    prompt: Pick a number
    alternatives:
      - name: one
      - name: two
    chosen: one
""",
    )
    assert (
        replay_or_dump(kind=PromptKind.SELECT, prompt="Pick a number", settings=settings, choices=_select_choices())
        == 1
    )
    with pytest.raises(NonInteractivePromptError):
        replay_or_dump(kind=PromptKind.CONFIRM, prompt="Continue?", settings=settings)
    assert len(_dump_path(settings).questions) == 2


def test_prompt_mismatch_replaces_file(settings):
    file_utils.ensure_parents_write_text(
        settings.non_interactive_prompt_file,
        """\
questions:
  - kind: confirm
    prompt: Old?
    response: true
""",
    )
    with pytest.raises(NonInteractivePromptError):
        replay_or_dump(kind=PromptKind.CONFIRM, prompt="New?", settings=settings)
    doc = _dump_path(settings)
    assert len(doc.questions) == 1
    assert doc.questions[0].prompt == "New?"


def test_answered_multi_without_checked_is_empty(settings):
    file_utils.ensure_parents_write_text(
        settings.non_interactive_prompt_file,
        """\
questions:
  - kind: select_multiple
    prompt: Extra
    status: answered
    alternatives:
      - name: foo
      - name: bar
""",
    )
    choices = [ChoiceTyped(name="foo", value="foo"), ChoiceTyped(name="bar", value="bar")]
    assert replay_or_dump(kind=PromptKind.SELECT_MULTIPLE, prompt="Extra", settings=settings, choices=choices) == []


def test_kind_mismatch_keeps_prefix(settings):
    file_utils.ensure_parents_write_text(
        settings.non_interactive_prompt_file,
        """\
questions:
  - kind: confirm
    prompt: First?
    response: true
  - kind: text
    prompt: Name?
    response: Ada
""",
    )
    assert replay_or_dump(kind=PromptKind.CONFIRM, prompt="First?", settings=settings)
    with pytest.raises(NonInteractivePromptError):
        replay_or_dump(kind=PromptKind.SELECT, prompt="Pick", settings=settings, choices=_select_choices())
    doc = _dump_path(settings)
    assert len(doc.questions) == 2
    assert doc.questions[0].kind == PromptKind.CONFIRM
    assert doc.questions[1].kind == PromptKind.SELECT


def test_unknown_chosen_rewrites(settings):
    file_utils.ensure_parents_write_text(
        settings.non_interactive_prompt_file,
        """\
questions:
  - kind: select
    prompt: Pick a number
    alternatives:
      - name: one
    chosen: missing
""",
    )
    with pytest.raises(NonInteractivePromptError):
        replay_or_dump(kind=PromptKind.SELECT, prompt="Pick a number", settings=settings, choices=_select_choices())
    row = _as_select(_dump_path(settings).questions[0])
    assert row.chosen is None
    assert [alt.name for alt in row.alternatives] == ["one", "two"]


def test_undecided_select_rewrites_and_keeps_index(settings):
    choices = [
        ChoiceTyped(name="one", value=1, description="first"),
        ChoiceTyped(name="two", value=2),
    ]
    with pytest.raises(NonInteractivePromptError):
        replay_or_dump(kind=PromptKind.SELECT, prompt="Pick", settings=settings, choices=choices)
    assert _as_select(_dump_path(settings).questions[0]).alternatives[0].description == "first"
    with pytest.raises(NonInteractivePromptError):
        replay_or_dump(kind=PromptKind.SELECT, prompt="Pick", settings=settings, choices=choices)
    assert len(_dump_path(settings).questions) == 1


def test_try_replay_answered_and_record(settings):
    record_answered_row(
        kind=PromptKind.CONFIRM,
        prompt="Go?",
        settings=settings,
        value=True,
    )
    ni._replay_index = 0
    assert try_replay_answered(kind=PromptKind.CONFIRM, prompt="Go?", settings=settings) is True
    assert try_replay_answered(kind=PromptKind.TEXT, prompt="Name?", settings=settings) is None
