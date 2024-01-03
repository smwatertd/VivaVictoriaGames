from dataclasses import dataclass

from domain.enums import ResultType
from domain.models.field import Field
from domain.models.player import Player


@dataclass(slots=True, frozen=True)
class Answer:
    id: int


@dataclass(slots=True, frozen=True)
class BasicCategory:
    id: int


@dataclass(slots=True, frozen=True)
class Category:
    id: int
    name: str


@dataclass(slots=True, frozen=True)
class DuelResult:
    result_type: ResultType
    field: Field


@dataclass(slots=True, frozen=True)
class GameResultLine:
    place: int
    player: Player
    score: int


@dataclass(frozen=True, slots=True)
class MarkingConflict:
    players: tuple[Player, ...]
    field: Field


@dataclass(slots=True, frozen=True)
class QuestionAnswer:
    id: int
    body: str


@dataclass(frozen=True, slots=True)
class Question:
    id: int
    body: str
    answers: list[QuestionAnswer]
    correct_answer: QuestionAnswer
