from pydantic import BaseModel


class Event(BaseModel):
    pass


class PlayerAdded(Event):
    game_pk: int
    player_pk: int
    username: str


class GameStarted(Event):
    game_pk: int


class PlayerTurnChanged(Event):
    game_pk: int
    player_pk: int


class PlayerRemoved(Event):
    game_pk: int
    player_pk: int


class FieldAttacked(Event):
    game_pk: int
    player_pk: int
    field_pk: int


class FieldCaptured(Event):
    game_pk: int
    player_pk: int
    field_pk: int


class DuelStarted(Event):
    game_pk: int
    attacker: int
    defender: int
