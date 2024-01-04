from domain import events
from domain.value_objects import Answer

from infrastructure.ports import UnitOfWork

from services import commands


async def create_game(command: commands.CreateGame, uow: UnitOfWork) -> None:
    async with uow:
        await uow.games.create(command.creator_id)
        await uow.commit()


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


async def select_base(command: commands.SelectBase, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(command.game_id)
        player = await uow.players.get(command.player_id)
        field = await uow.fields.get(command.field_id)
        game.select_player_base(player, field)
        await uow.commit()


async def mark_field(command: commands.MarkField, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(command.game_id)
        player = await uow.players.get(command.player_id)
        field = await uow.fields.get(command.field_id)
        game.mark_field(player, field)
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
        answer = Answer(id=command.answer_pk)
        game.set_player_answer(player, answer)
        await uow.commit()


async def try_start_game(event: events.PlayerAdded, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.try_start()
        await uow.commit()


async def start_preparatory_stage(event: events.GameStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_preparatory_stage()
        await uow.commit()


async def start_round(event: events.StageStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_round()
        await uow.commit()


async def finish_round(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.finish_round()
        await uow.commit()


async def capture_marked_fields(event: events.RoundFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.capture_marked_fields()
        await uow.commit()


async def check_round_outcome(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_round_outcome()
        await uow.commit()


async def check_are_all_players_marked_fields(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_are_all_players_marked_fields()
        await uow.commit()


async def check_marking_conflict(event: events.AllPlayersMarkedFields, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_marking_conflict()
        await uow.commit()


async def start_marking_battle(event: events.MarkingConflictDetected, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        players = [await uow.players.get(player.id) for player in event.players]
        field = await uow.fields.get(event.field.id)
        category = await uow.categories.random()
        game.start_marking_battle(players, field, category)
        await uow.commit()


async def select_question(event: events.MarkingBattleStarted | events.DuelRoundStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        question = await uow.questions.random_by_category(event.category.id)
        game.set_question(question)
        await uow.commit()


async def check_are_all_players_answered(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_are_all_players_answered()
        await uow.commit()


async def finish_battle_round(event: events.AllPlayersAnswered, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.finish_battle_round()
        await uow.commit()


async def start_duel(event: events.FieldAttacked, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        attacker, defender = await uow.players.get(event.attacker.id), await uow.players.get(event.defender.id)
        field = await uow.fields.get(event.field.id)
        category = await uow.categories.random()
        game.start_duel(attacker, defender, field, category)
        await uow.commit()


async def check_round_process_outcome(event: events.DuelRoundFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_duel_round_outcome()
        await uow.commit()


async def check_stage_outcome(event: events.StageFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_stage_outcome(event.name)
        await uow.commit()


async def start_duel_round(event: events.DuelStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_duel_round()
        await uow.commit()


async def send_notification(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        await uow.games.get(event.game_id)
        # print(f'Sending notification for {game.get_id()} event: {event}')
        await uow.commit()


COMMAND_HANDLERS = {
    commands.CreateGame: create_game,
    commands.AddUser: add_game_player,
    commands.RemoveUser: remove_game_player,
    commands.SelectBase: select_base,
    commands.MarkField: mark_field,
    commands.SendAnswer: send_answer,
    commands.AttackField: attack_field,
}

EVENT_HANDLERS = {
    events.PlayerAdded: [try_start_game],
    events.PlayerRemoved: [],

    events.GameStarted: [start_preparatory_stage],
    events.GameFinished: [],

    events.StageStarted: [start_round],
    events.StageFinished: [check_stage_outcome],

    events.RoundStarted: [],
    events.RoundFinished: [check_round_outcome],

    events.QuestionSelected: [],
    events.PlayerAnswered: [check_are_all_players_answered],
    events.AllPlayersAnswered: [finish_battle_round],

    events.BaseSelected: [finish_round],

    events.PlayerMarkedField: [check_are_all_players_marked_fields],
    events.AllPlayersMarkedFields: [check_marking_conflict],
    events.MarkedFieldsCaptured: [finish_round],
    events.MarkingConflictDetected: [start_marking_battle],
    events.MarkingBattleStarted: [select_question],
    events.MarkingBattleFinished: [capture_marked_fields],

    events.FieldAttacked: [start_duel],
    events.DuelStarted: [start_duel_round],
    events.DuelRoundStarted: [select_question],
    events.DuelRoundFinished: [check_round_process_outcome],
    events.DuelFinished: [finish_round],
}
