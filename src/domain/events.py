from pydantic import BaseModel


class Event(BaseModel):
    pass


class GameEvent(Event):
    game_pk: int


class FieldEvent(GameEvent):
    field_pk: int


class PlayerAdded(GameEvent):
    player_pk: int
    username: str


class GameStarted(GameEvent):
    pass


class PlayerTurnChanged(GameEvent):
    player_pk: int


class PlayerRemoved(GameEvent):
    player_pk: int


class FieldAttacked(GameEvent):
    attacker_pk: int


class FieldCaptured(GameEvent):
    capturer_pk: int


class DuelStarted(GameEvent):
    attacker: int
    defender: int
