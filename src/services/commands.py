from pydantic import BaseModel


class Command(BaseModel):
    pass


class CreateGame(Command):
    creator_id: int


class AddUser(Command):
    game_pk: int
    user_pk: int
    username: str


class RemoveUser(Command):
    game_pk: int
    user_pk: int
    username: str


class SelectBase(Command):
    game_id: int
    player_id: int
    field_id: int


class AttackField(Command):
    game_pk: int
    attacker_pk: int
    field_pk: int


class SendAnswer(Command):
    game_pk: int
    player_pk: int
    answer_pk: int
