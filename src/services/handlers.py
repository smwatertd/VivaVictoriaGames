from typing import Callable, Type

from domain import commands, events

from infrastructure.ports import UnitOfWork

from questions import Question, QuestionsClient


async def connect_user(command: commands.ConnectUser, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(command.game_id)
        game.add_player(command.user_id)
        await uow.commit()


async def disconnect_user(command: commands.DisconnectUser, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(command.game_id)
        game.discard_player(command.user_id)
        await uow.commit()


async def get_question(command: commands.GetQuestion, uow: UnitOfWork) -> Question:
    async with uow:
        game = await uow.games.get(command.game_pk)
        question = await QuestionsClient().get_random_question()
        game.set_question(question)
        await uow.commit()
    return question


async def user_connected(event: events.UserConnected, uow: UnitOfWork) -> None:
    pass


async def user_disconnected(event: events.UserDisconnected, uow: UnitOfWork) -> None:
    pass


COMMAND_HANDLERS = {
    commands.ConnectUser: connect_user,
    commands.DisconnectUser: disconnect_user,
    commands.GetQuestion: get_question,
}

EVENT_HANDLERS: dict[Type[events.Event], tuple[Callable, ...]] = {
    events.UserConnected: (user_connected,),
    events.UserDisconnected: (user_disconnected,),
}
