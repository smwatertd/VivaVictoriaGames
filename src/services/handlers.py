from typing import Callable, Type

from core.settings import game_settings

from domain import commands, events

from infrastructure.ports import UnitOfWork


async def add_game_player(command: commands.AddUser, uow: UnitOfWork) -> None:
    async with uow:
        player = await uow.players.get_or_create(command.user_pk)
        game = await uow.games.get(command.game_pk)
        game.add_player(player)
        await uow.commit()


async def remove_game_player(command: commands.RemoveUser, uow: UnitOfWork) -> None:
    async with uow:
        player = await uow.players.get(command.user_pk)
        game = await uow.games.get(command.game_pk)
        game.remove_player(player)
        await uow.commit()


async def attack_field(command: commands.AttackField, uow: UnitOfWork) -> None:
    async with uow:
        field = await uow.fields.get(command.field_pk)
        attacker = await uow.players.get(command.attacker_pk)
        game = await uow.games.get(command.game_pk)
        game.attack_field(attacker, field)
        await uow.commit()


async def send_answer(command: commands.SendAnswer, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(command.game_pk)
        player = await uow.players.get(command.player_pk)
        answer = await uow.answers.get(command.answer_pk)
        game.set_player_answer(player, answer)
        await uow.commit()


async def try_start_game(event: events.PlayerAdded, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        if game.is_full():
            game.start()
        await uow.commit()


async def start_round(event: events.GameStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_round()
        await uow.commit()


async def start_round_timer(event: events.RoundStarted, uow: UnitOfWork) -> None:
    async with uow:
        pass
        # game = await uow.games.get(event.game_id)
        # await uow.commit()


async def check_round_outcome(event: events.RoundFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.increase_round_number(1)
        if game.round_number == game_settings.max_rounds:
            game.finish()
        else:
            game.start_round()
        await uow.commit()


async def start_duel_round_timer(event: events.DuelRoundStarted, uow: UnitOfWork) -> None:
    async with uow:
        pass
        # game = await uow.games.get(event.game_id)
        # await uow.commit()


async def finish_round(event: events.FieldCaptured, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.finish_round()
        await uow.commit()


async def start_duel(event: events.PlayerFieldAttacked, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        defender, attacker = await uow.players.get(event.defender_id), await uow.players.get(event.attacker_id)
        field = await uow.fields.get(event.field_id)
        game.start_duel(attacker, defender, field)
        await uow.commit()


async def start_duel_round(event: events.DuelStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_duel_round()
        await uow.commit()


async def select_category(event: events.DuelRoundStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        category = await uow.categories.random()
        game.set_duel_category(category)
        await uow.commit()


async def select_question(event: events.CategorySetted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        question = await uow.questions.random_by_category(event.category_id)
        game.set_duel_question(question)
        await uow.commit()


async def check_duel_round_outcome(event: events.DuelRoundFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.increase_duel_round_number(1)
        if game._duel.round_number == game_settings.duel_max_rounds:
            game.finish_duel()
        else:
            game.start_duel_round()
        await uow.commit()


async def check_are_all_players_answered(event: events.PlayerAnswered, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        if game.are_all_players_answered():
            game.finish_duel_round()
        await uow.commit()


async def send_message_notification(event: events.Event, uow: UnitOfWork) -> None:
    try:
        game_id = event.game_id
    except AttributeError:
        return

    async with uow:
        message = uow.serializer.serialize(event)
        await uow.chat_message_producer.publish(str(game_id), message)


COMMAND_HANDLERS = {
    commands.AddUser: add_game_player,
    commands.RemoveUser: remove_game_player,
    commands.AttackField: attack_field,
    commands.SendAnswer: send_answer,
}

EVENT_HANDLERS: dict[Type[events.Event], list[Callable]] = {
    events.PlayerAdded: [send_message_notification, try_start_game],
    events.PlayerRemoved: [send_message_notification],

    events.GameStarted: [send_message_notification, start_round],
    events.GameEnded: [send_message_notification],

    events.RoundStarted: [send_message_notification],
    # events.RoundStarted: [send_message_notification, start_round_timer],
    events.PlayerFieldAttacked: [send_message_notification, start_duel],
    events.FieldCaptured: [send_message_notification, finish_round],
    events.FieldDefended: [send_message_notification, finish_round],
    events.RoundFinished: [send_message_notification, check_round_outcome],

    events.DuelStarted: [send_message_notification, start_duel_round],
    events.DuelRoundStarted: [send_message_notification, select_category],
    # events.DuelRoundStarted: [send_message_notification, select_category, start_duel_round_timer],
    events.CategorySetted: [send_message_notification, select_question],
    events.QuestionSetted: [send_message_notification],
    events.PlayerAnswered: [send_message_notification, check_are_all_players_answered],
    events.DuelRoundFinished: [send_message_notification, check_duel_round_outcome],
    events.DuelEnded: [send_message_notification],
}
