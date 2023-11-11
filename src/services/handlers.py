from typing import Callable, Type

from domain import commands, events
from domain.models.player import Player

from infrastructure.ports import UnitOfWork


DUEL_TIMEOUT = 10


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
    pass


async def send_message_notification(event: events.GameEvent, uow: UnitOfWork) -> None:
    await uow.message_producer.publish(event.game_pk, event.model_dump())


COMMAND_HANDLERS = {
    commands.AddUser: connect_user,
    commands.RemoveUser: disconnect_user,
    commands.AttackField: attack_field,
    commands.SendAnswer: send_answer,
}

EVENT_HANDLERS: dict[Type[events.Event], tuple[Callable, ...]] = {
    events.PlayerAdded: (send_message_notification,),
    events.PlayerRemoved: (send_message_notification,),
    events.GameStarted: (send_message_notification,),
    events.PlayerTurnChanged: (send_message_notification,),
    events.FieldAttacked: (send_message_notification,),
    events.FieldCaptured: (send_message_notification,),
    events.DuelStarted: (send_message_notification,),
}
