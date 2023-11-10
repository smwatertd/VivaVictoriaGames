from typing import Callable, Type

from domain import commands, events
from domain.models.player import Player

from infrastructure.ports import UnitOfWork


async def connect_user(command: commands.AddUser, uow: UnitOfWork) -> None:
    async with uow:
        player = await uow.players.create(Player(pk=command.user_pk, username=command.username))
        game = await uow.games.get(pk=command.game_pk)
        game.add_player(player)
        await uow.commit()


async def disconnect_user(command: commands.RemoveUser, uow: UnitOfWork) -> None:
    async with uow:
        player = await uow.players.get(pk=command.user_pk)
        game = await uow.games.get(pk=command.game_pk)
        game.remove_player(player)
        await uow.commit()


async def attack_field(command: commands.AttackField, uow: UnitOfWork) -> None:
    async with uow:
        field = await uow.fields.get(pk=command.field_pk)
        attacker = await uow.players.get(pk=command.attacker_pk)
        game = await uow.games.get(pk=command.game_pk)
        game.attack_field(attacker, field)
        await uow.commit()


async def send_answer(command: commands.SendAnswer, uow: UnitOfWork) -> None:
    async with uow:
        # game = await uow.games.get(pk=command.game_pk)
        # game.send_answer()
        await uow.commit()


COMMAND_HANDLERS = {
    commands.AddUser: connect_user,
    commands.RemoveUser: disconnect_user,
    commands.AttackField: attack_field,
    commands.SendAnswer: send_answer,
}

EVENT_HANDLERS: dict[Type[events.Event], tuple[Callable, ...]] = {
}
