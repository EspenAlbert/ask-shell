from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated, Generic, Literal, TypeVar

from model_lib import Entity
from pydantic import Field
from questionary import Choice

_UNDECIDED = "undecided"

T = TypeVar("T")


class PromptKind(StrEnum):
    CONFIRM = "confirm"
    TEXT = "text"
    SELECT = "select"
    SELECT_MULTIPLE = "select_multiple"


class MultiSelectStatus(StrEnum):
    UNDECIDED = "undecided"
    ANSWERED = "answered"


class SelectAlternative(Entity):
    name: str
    description: str | None = None


class ConfirmQuestion(Entity):
    kind: Literal[PromptKind.CONFIRM] = PromptKind.CONFIRM
    prompt: str
    response: Literal["undecided"] | bool = _UNDECIDED


class TextQuestion(Entity):
    kind: Literal[PromptKind.TEXT] = PromptKind.TEXT
    prompt: str
    response: str = _UNDECIDED


class SelectQuestion(Entity):
    kind: Literal[PromptKind.SELECT] = PromptKind.SELECT
    prompt: str
    alternatives: list[SelectAlternative] = Field(default_factory=list)
    chosen: str | None = None


class SelectMultipleQuestion(Entity):
    kind: Literal[PromptKind.SELECT_MULTIPLE] = PromptKind.SELECT_MULTIPLE
    prompt: str
    status: MultiSelectStatus = MultiSelectStatus.UNDECIDED
    alternatives: list[SelectAlternative] = Field(default_factory=list)
    checked: list[str] = Field(default_factory=list)


PromptQuestion = Annotated[
    ConfirmQuestion | TextQuestion | SelectQuestion | SelectMultipleQuestion,
    Field(discriminator="kind"),
]


class PromptSession(Entity):
    command: str
    pinned: bool = False


class NonInteractivePromptFile(Entity):
    session: PromptSession | None = None
    questions: list[PromptQuestion] = Field(default_factory=list)


@dataclass
class ChoiceTyped(Generic[T]):
    name: str
    value: T
    description: str | None = None
    checked: bool = False

    @classmethod
    def from_descriptions(cls, descriptions: dict[str, str]) -> list[ChoiceTyped[str]]:
        return [cls(name=name, value=name, description=description) for name, description in descriptions.items()]  # type: ignore

    def as_choice(self) -> Choice:
        return Choice(
            title=self.name,
            value=self.value,
            description=self.description,
            checked=self.checked,
        )
