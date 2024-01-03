from enum import Enum
from typing import Any

from pydantic import BaseModel


class Player(BaseModel):
    id: int


class Field(BaseModel):
    id: int


class GameResultLine(BaseModel):
    place: int
    player: Player
    score: int


class StageType(str, Enum):
    PREPARATORY = 'PREPARATORY'
    CAPTURING = 'CAPTURING'
    BATTLINGS = 'BATTLINGS'


class ResultType(str, Enum):
    CAPTURED = 'CAPTURED'
    DEFENDED = 'DEFENDED'


class FieldCaptured(BaseModel):
    field: Field
    player: Player
    new_field_value: int


class FieldDefended(BaseModel):
    field: Field
    new_field_value: int


class StageInfo(BaseModel):
    rounds_count: int


class RoundType(str, Enum):
    ORDERED = 'ORDERED'
    UNORDERED = 'UNORDERED'


class Category(BaseModel):
    id: int
    name: str


class Answer(BaseModel):
    id: int
    body: str


class Question(BaseModel):
    body: str
    answers: list[Answer]


class ExplicitAnswer(BaseModel):
    id: int


class PlayerAnswer(BaseModel):
    player: Player
    answer: ExplicitAnswer


class MarkedField(BaseModel):
    player: Player
    field: Field


class Event(BaseModel):
    pass


class GameEvent(Event):
    game_id: int


class PlayerAdded(GameEvent):
    player: Player
    connected_players: list[Player]


class PlayerRemoved(GameEvent):
    player: Player


class GameStarted(GameEvent):
    fields: list[Field]
    order: list[Player]


class GameFinished(GameEvent):
    results: list[GameResultLine]


class StageStarted(GameEvent):
    stage_type: StageType
    stage_info: StageInfo | None = None

    def model_dump(self, **kwargs: Any) -> dict:
        if self.stage_type == StageType.CAPTURING and self.stage_info is not None:
            raise ValueError('Capturing stage must not have stage info')
        return super().model_dump(exclude_none=True, **kwargs)


class StageFinished(GameEvent):
    stage_type: StageType


class RoundStarted(GameEvent):
    round_type: RoundType
    round_number: int
    duration_seconds: int
    player: Player | None = None

    def model_dump(self, **kwargs: Any) -> dict:
        if self.round_type == RoundType.UNORDERED and self.player is not None:
            raise ValueError('Unordered round must not have player')
        return super().model_dump(exclude_none=True, **kwargs)


class RoundFinished(GameEvent):
    pass


class BaseSelected(GameEvent):
    player: Player
    field: Field
    new_field_value: int


class QuestionSetted(GameEvent):
    question: Question


class PlayerAnsweredImplicitly(GameEvent):
    player: Player


class AllPlayersAnswered(GameEvent):
    answers: list[PlayerAnswer]


class PlayerImplicitlyMarkedField(GameEvent):
    player: Player


class AllPlayersMarkedFields(GameEvent):
    marked_fields: list[MarkedField]


class MarkingConflictDetected(GameEvent):
    field: Field
    players: list[Player]


class MarkedFieldsCaptured(GameEvent):
    fields: list[FieldCaptured]


class MarkingBattleStarted(GameEvent):
    players: list[Player]
    field: Field
    category: Category


class MarkingBattleFinished(GameEvent):
    winner: Player


class FieldAttacked(GameEvent):
    attacker: Player
    defender: Player
    field: Field


class DuelStarted(GameEvent):
    attacker: Player
    defender: Player
    field: Field
    category: Category


class DuelFinished(GameEvent):
    result_type: ResultType
    result: FieldDefended | FieldCaptured


class DuelRoundStarted(GameEvent):
    game_id: int
    round_number: int
    duration_seconds: int
    category: Category


class DuelRoundFinished(GameEvent):
    pass
