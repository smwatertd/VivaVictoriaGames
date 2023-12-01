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


class GameStarted(Event):
    game_id: int


class GameFull(Event):
    game_id: int


class GameStateChanged(Event):
    game_id: int
    state: str


class GameClosed(Event):
    game_id: int


class PlayerTurnChanged(Event):
    game_id: int
    player_id: int


class PlayerRemoved(Event):
    game_id: int
    player_id: int


class FieldAttacked(FieldEvent):
    attacker_pk: int


class FieldCaptured(Event):
    game_id: int
    field_id: int
    capturer_id: int


class PlayerFieldAttacked(Event):
    game_id: int
    attacker_id: int
    defender_id: int
    field_id: int


class DuelStarted(Event):
    game_id: int
    attacker_id: int
    defender_id: int


class QuestionSet(GameEvent):
    question_pk: int
    answers: list[tuple[int, str]]


class AllPlayersConnected(Event):
    game_id: int
