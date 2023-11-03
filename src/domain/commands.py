from pydantic import BaseModel


class Command(BaseModel):
    pass


class ConnectUser(Command):
    game_id: int
    user_id: int
    username: str


class DisconnectUser(Command):
    game_id: int
    user_id: int
    username: str


class GetQuestion(Command):
    game_pk: int
