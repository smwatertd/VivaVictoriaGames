from pydantic import BaseModel


class Command(BaseModel):
    pass


class AddUser(Command):
    game_id: int
    user_id: int
    username: str


class RemoveUser(Command):
    game_id: int
    user_id: int
    username: str
