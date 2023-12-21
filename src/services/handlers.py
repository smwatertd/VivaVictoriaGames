from typing import Callable, Type

from domain import commands, events
from domain.models.strategies import IdentityPlayerTurnSelector

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
        game.set_player_answer(player, command.answer_pk)
        await uow.commit()


async def try_start_game(event: events.PlayerAdded, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.try_start()
        await uow.commit()


async def start_round(event: events.GameStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_round(IdentityPlayerTurnSelector())
        await uow.commit()


async def start_round_timer(event: events.RoundStarted, uow: UnitOfWork) -> None:
    async with uow:
        pass
        # game = await uow.games.get(event.game_id)
        # await uow.commit()


async def check_round_outcome(event: events.RoundFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_round_outcome(IdentityPlayerTurnSelector())
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
        category_id = await uow.categories.random()
        game.set_duel_category(category_id)
        await uow.commit()


async def select_question(event: events.CategorySetted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        question_id = await uow.questions.random_by_category(event.category_id)
        correct_answer_id = await uow.questions.get_correct_answer(question_id)
        game.set_duel_question(question_id)
        game.set_duel_correct_answer(correct_answer_id)
        await uow.commit()


async def check_duel_round_outcome(event: events.DuelRoundFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_duel_round_outcome()
        await uow.commit()


async def check_are_all_players_answered(event: events.PlayerAnswered, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.try_finish_duel_round()
        await uow.commit()


async def check_duel_results(event: events.DuelEnded, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_duel_results()
        await uow.commit()


COMMAND_HANDLERS = {
    commands.AddUser: add_game_player,
    commands.RemoveUser: remove_game_player,
    commands.AttackField: attack_field,
    commands.SendAnswer: send_answer,
}

EVENT_HANDLERS: dict[Type[events.Event], list[Callable]] = {
    events.PlayerAdded: [try_start_game],
    # events.PlayerRemoved: [],

    events.GameStarted: [start_round],
    # events.GameEnded: [],

    # events.RoundStarted: [],
    # events.RoundStarted: [, start_round_timer],
    events.PlayerFieldAttacked: [start_duel],
    events.FieldCaptured: [finish_round],
    events.FieldDefended: [finish_round],
    events.RoundFinished: [check_round_outcome],

    events.DuelStarted: [start_duel_round],
    events.DuelRoundStarted: [select_category],
    # events.DuelRoundStarted: [, select_category, start_duel_round_timer],
    events.CategorySetted: [select_question],
    # events.QuestionSetted: [],
    events.PlayerAnswered: [check_are_all_players_answered],
    events.DuelRoundFinished: [check_duel_round_outcome],
    events.DuelEnded: [check_duel_results],
}
