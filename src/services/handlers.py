from typing import Callable, Type

from domain import commands, events, models
from domain.models.strategies import IdentityPlayerTurnSelector

from infrastructure.ports import UnitOfWork


async def connect_user(command: commands.AddUser, uow: UnitOfWork) -> None:
    async with uow:
        player = models.Player(command.user_pk, command.username)
        game = await uow.games.get(command.game_pk)
        game.add_player(player)
        await uow.commit()


async def disconnect_user(command: commands.RemoveUser, uow: UnitOfWork) -> None:
    async with uow:
        player = await uow.players.get(command.user_pk)
        game = await uow.games.get(command.game_pk)
        game.remove_player(player)
        await uow.commit()


async def start_game(event: events.GameStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start()
        await uow.commit()


async def select_player_turn(event: events.GameStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.select_player_turn(IdentityPlayerTurnSelector())
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
        answer = await uow.answers.get(pk=command.answer_pk)
        game = await uow.games.get(pk=command.game_pk)
        game.verify_answer(answer)
        await uow.commit()


async def send_message_notification(event: events.GameEvent, uow: UnitOfWork) -> None:
    await uow.message_producer.publish(event.game_pk, event.model_dump())


COMMAND_HANDLERS = {
    commands.AddUser: connect_user,
    commands.RemoveUser: disconnect_user,
}

EVENT_HANDLERS: dict[Type[events.Event], list[Callable]] = {
    events.PlayerAdded: [send_message_notification],
    events.PlayerRemoved: [send_message_notification],
    events.GameClosed: [start_game],
    events.GameStarted: [select_player_turn, send_message_notification],
    events.PlayerTurnChanged: [send_message_notification],
}
