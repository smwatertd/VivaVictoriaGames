from pydantic import BaseModel


class Event(BaseModel):
    pass


class UserConnected(Event):
    pk: int
    user_pk: int


class UserDisconnected(Event):
    pk: int
    user_pk: int


class GameStarted(Event):
    pk: int


class GameStarting(Event):
    pk: int
