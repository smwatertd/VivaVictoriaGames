from typing import Any

from domain import enums, event_models

from pydantic import BaseModel


class Event(BaseModel):
    pass


class GameEvent(Event):
    game_id: int


class PlayerAdded(GameEvent):
    player: event_models.Player
    connected: list[event_models.Player]


class PlayerRemoved(GameEvent):
    player: event_models.Player


class GameStarted(GameEvent):
    fields: list[event_models.Field]
    order: list[event_models.Player]


class GameFinished(GameEvent):
    results: list[event_models.PlayerResult]


class StageStarted(GameEvent):
    name: enums.StageName
    info: event_models.StageInfo | None = None

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return super().model_dump(**kwargs, exclude_none=True)


class StageFinished(GameEvent):
    name: enums.StageName


class RoundStarted(GameEvent):
    ordered: bool
    number: int
    duration: event_models.Duration
    player: event_models.Player | None = None

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return super().model_dump(**kwargs, exclude_none=True)


class RoundFinished(GameEvent):
    pass


class BaseSelected(GameEvent):
    field: event_models.CapturedField


class QuestionSelected(GameEvent):
    question: event_models.Question


class PlayerAnswered(GameEvent):
    player: event_models.Player


class AllPlayersAnswered(GameEvent):
    answers: list[event_models.PlayerAnswer]


class PlayerMarkedField(GameEvent):
    player: event_models.Player


class AllPlayersMarkedFields(GameEvent):
    fields: list[event_models.MarkedField]


class MarkedFieldsCaptured(GameEvent):
    fields: list[event_models.CapturedField]


class MarkingConflictDetected(GameEvent):
    field: event_models.Field
    players: list[event_models.Player]


class MarkingBattleStarted(GameEvent):
    players: list[event_models.Player]
    field: event_models.Field
    category: event_models.Category


class MarkingBattleFinished(GameEvent):
    winner: event_models.Player


class FieldAttacked(GameEvent):
    attacker: event_models.Player
    defender: event_models.Player
    field: event_models.Field


class DuelStarted(GameEvent):
    attacker: event_models.Player
    defender: event_models.Player
    field: event_models.Field
    category: event_models.Category


class DuelRoundStarted(GameEvent):
    game_id: int
    number: int
    duration: event_models.Duration
    category: event_models.BasicCategory


class DuelRoundFinished(GameEvent):
    correct: event_models.Answer


class DuelFinished(GameEvent):
    captured: bool
    result: event_models.DefendedField | event_models.CapturedField
