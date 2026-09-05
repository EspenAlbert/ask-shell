from pathlib import Path

from zero_3rdparty import file_utils

from ask_shell._internal.interactive_models import NonInteractivePromptFile, PromptSession
from ask_shell._internal.prompt_file import (
    discard_empty_prompt_stub,
    is_empty_prompt_stub,
    prompt_session_needs_attention,
)


def test_prompt_session_attention_and_stub(tmp_path: Path) -> None:
    empty = NonInteractivePromptFile(session=PromptSession(command="app/cmd", pinned=False))
    assert not prompt_session_needs_attention(empty)
    assert is_empty_prompt_stub(empty)

    pinned_empty = NonInteractivePromptFile(session=PromptSession(command="app/cmd", pinned=True))
    assert not is_empty_prompt_stub(pinned_empty)

    undecided = NonInteractivePromptFile.model_validate(
        {
            "session": {"command": "app/cmd", "pinned": False},
            "questions": [{"kind": "confirm", "prompt": "Ship?", "response": "undecided"}],
        }
    )
    assert prompt_session_needs_attention(undecided)
    assert not is_empty_prompt_stub(undecided)

    answered = NonInteractivePromptFile.model_validate(
        {
            "session": {"command": "app/cmd", "pinned": False},
            "questions": [{"kind": "confirm", "prompt": "Ship?", "response": True}],
        }
    )
    assert not prompt_session_needs_attention(answered)

    live = tmp_path / "non_interactive_prompt.yaml"
    file_utils.ensure_parents_write_text(
        live,
        "session:\n  command: app/cmd\n  pinned: false\nquestions: []\n",
    )
    assert discard_empty_prompt_stub(live)
    assert not live.exists()
