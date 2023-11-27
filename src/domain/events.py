from typing import Any

from pydantic import BaseModel


class Event(BaseModel):
    def model_dump(self, *args: Any, **kwargs: Any) -> dict:
        result = super().model_dump(*args, **kwargs)
        result.update({
            'event_type': type(self).__name__,
        })
        return result


class GameEvent(Event):
    game_pk: int


class FieldEvent(GameEvent):
    field_pk: int


class PlayerAdded(Event):
    game_id: int
    player_id: int
    username: str


class GameStarted(GameEvent):
    pass


class GameFull(Event):
    game_id: int


class GameStateChanged(Event):
    game_id: int
    state: str


class GameClosed(Event):
    game_id: int


class PlayerTurnChanged(GameEvent):
    player_pk: int


class PlayerRemoved(GameEvent):
    player_pk: int


class FieldAttacked(FieldEvent):
    attacker_pk: int


class FieldCaptured(FieldEvent):
    capturer_pk: int


class DuelStarted(GameEvent):
    attacker_pk: int
    defender_pk: int


class QuestionSet(GameEvent):
    question_pk: int
    answers: list[tuple[int, str]]


class AllPlayersConnected(Event):
    game_id: int
