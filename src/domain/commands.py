from pydantic import BaseModel


class Command(BaseModel):
    pass


class AddUser(Command):
    game_pk: int
    user_pk: int
    username: str


class RemoveUser(Command):
    game_pk: int
    user_pk: int
    username: str


class AttackField(Command):
    game_pk: int
    attacker_pk: int
    field_pk: int
