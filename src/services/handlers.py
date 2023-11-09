from typing import Callable, Type

from domain import commands, events
from domain.models.player import Player

from infrastructure.ports import UnitOfWork


async def connect_user(command: commands.AddUser, uow: UnitOfWork) -> None:
    async with uow:
        player = Player(pk=command.user_id, username=command.username)
        game = await uow.games.get(pk=command.game_id)
        game.add_player(player)
        await uow.commit()


async def disconnect_user(command: commands.RemoveUser, uow: UnitOfWork) -> None:
    async with uow:
        player = Player(pk=command.user_id, username=command.username)
        game = await uow.games.get(pk=command.game_id)
        game.remove_player(player)
        await uow.commit()


COMMAND_HANDLERS = {
    commands.AddUser: connect_user,
    commands.RemoveUser: disconnect_user,
}

EVENT_HANDLERS: dict[Type[events.Event], tuple[Callable, ...]] = {
}
