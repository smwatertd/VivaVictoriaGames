from domain import events

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


async def send_marking_conflict_answer(command: commands.SendMarkingConflictAnswer, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(command.game_id)
        player = await uow.players.get(command.player_id)
        game.send_marking_conflict_answer(player, command.answer_id)
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


async def start_stage(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_stage()
        await uow.commit()


# async def start_selecting_base_stage(event: events.GameStarted, uow: UnitOfWork) -> None:
#     async with uow:
#         game = await uow.games.get(event.game_id)
#         game.start_preparatory_stage()
#         await uow.commit()


async def start_round(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_round()
        await uow.commit()


# async def start_selecting_base_stage_round(event: events.PreparatoryStageStarted, uow: UnitOfWork) -> None:
#     async with uow:
#         game = await uow.games.get(event.game_id)
#         game.start_preparatory_stage_round()
#         await uow.commit()


async def finish_round(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.finish_round()
        await uow.commit()


# async def stop_selecting_base_stage_round(event: events.BaseSelected, uow: UnitOfWork) -> None:
#     async with uow:
#         game = await uow.games.get(event.game_id)
#         game.stop_preparatory_stage_round()
#         await uow.commit()


async def check_round_outcome(event: events.GameEvent, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_round_outcome()
        await uow.commit()


# async def check_selecting_base_stage_round_outcome(
#     event: events.SelectingBaseStageRoundFinished,
#     uow: UnitOfWork,
# ) -> None:
#     async with uow:
#         game = await uow.games.get(event.game_id)
#         game.check_preparatory_stage_round_outcome()
#         await uow.commit()


async def check_stage_outcome(event: events.StageFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_stage_outcome(event.stage_type)
        await uow.commit()


# async def start_capturing_stage(event: events.SelectingBaseStageFinished, uow: UnitOfWork) -> None:
#     async with uow:
#         game = await uow.games.get(event.game_id)
#         game.start_capturing_stage()
#         await uow.commit()


async def start_capturing_stage_round(event: events.CapturingStageStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_capturing_stage_round()
        await uow.commit()


async def check_are_all_players_marked_fields(event: events.FieldMarked, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_are_all_players_marked_fields()
        await uow.commit()


async def check_marking_conflict(event: events.FieldsMarked, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_marking_conflict()
        await uow.commit()


async def start_capturing_battle(event: events.MarkingConflictDetected, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        players = [await uow.players.get(player.id) for player in event.players]
        field = await uow.fields.get(event.field_id)
        game.start_capturing_battle(players, field)
        await uow.commit()


async def select_capturing_category(event: events.CapturingBattleStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        category = await uow.categories.random()
        game.set_capturing_category(category)
        await uow.commit()


async def select_capturing_question(event: events.CapturingBattleCategorySetted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        question = await uow.questions.random_by_category(event.category_id)
        game.set_capturing_question(question)
        correct_answer = await uow.questions.get_correct_answer(question)
        game.set_capturing_correct_answer(correct_answer)
        await uow.commit()


async def check_capturing_battle_outcome(event: events.CapturingBattlePlayerAnswered, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_capturing_battle_outcome()
        await uow.commit()


async def check_capturing_stage_round_outcome(event: events.CapturingStageRoundFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_capturing_stage_round_outcome()
        await uow.commit()


async def start_battlings_stage(event: events.CapturingStageFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_battlings_stage()
        await uow.commit()


async def start_battlings_stage_round(event: events.BattlingsStageStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_battlings_stage_round()
        await uow.commit()


async def start_duel(event: events.FieldAttacked, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        attacker, defender = await uow.players.get(event.attacker_id), await uow.players.get(event.defender_id)
        field = await uow.fields.get(event.field_id)
        game.start_duel(attacker, defender, field)
        await uow.commit()


async def select_duel_category(event: events.DuelStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        category = await uow.categories.random()
        game.set_duel_category(category)
        await uow.commit()


async def start_duel_round(event: events.DuelStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.start_duel_round()
        await uow.commit()


async def select_duel_question(event: events.DuelRoundStarted, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        question = await uow.questions.random_by_category(game.get_duel_category())
        game.set_duel_question(question)
        correct_answer = await uow.questions.get_correct_answer(question)
        game.set_duel_correct_answer(correct_answer)
        await uow.commit()


async def check_are_all_players_answered(event: events.PlayerAnswered, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_are_all_players_answered()
        await uow.commit()


async def check_duel_round_outcome(event: events.DuelRoundFinished, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_duel_round_outcome()
        await uow.commit()


async def finish_battlings_stage_round(event: events.DuelEnded, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.finish_battlings_stage_round()
        await uow.commit()


async def check_battlings_stage_round_outcome(event: events.BattlingsStageRoundEnded, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.check_battlings_stage_round_outcome()
        await uow.commit()


async def finish_game(event: events.BattlingsStageEnded, uow: UnitOfWork) -> None:
    async with uow:
        game = await uow.games.get(event.game_id)
        game.finish()
        await uow.commit()


COMMAND_HANDLERS = {
    commands.CreateGame: create_game,
    commands.AddUser: add_game_player,
    commands.RemoveUser: remove_game_player,
    commands.SelectBase: select_base,
    commands.MarkField: mark_field,
    commands.SendMarkingConflictAnswer: send_marking_conflict_answer,
    commands.AttackField: attack_field,
    commands.SendAnswer: send_answer,
}

EVENT_HANDLERS = {
    events.PlayerAdded: [try_start_game],
    events.PlayerRemoved: [],
    events.GameStarted: [start_stage],
    events.GameFinished: [],
    # The Selecting Base Stage
    events.LimitedByRoundsStageStarted: [start_round],
    events.OrderedRoundStarted: [],
    events.BaseSelected: [finish_round],
    events.RoundFinished: [check_round_outcome],
    events.StageFinished: [check_stage_outcome],
    # The Capturing Stage
    events.CapturingStageStarted: [start_capturing_stage_round],
    events.CapturingStageRoundStarted: [],
    events.FieldMarked: [check_are_all_players_marked_fields],
    events.FieldsMarked: [check_marking_conflict],
    events.MarkingConflictDetected: [start_capturing_battle],
    events.CapturingBattleStarted: [select_capturing_category],
    events.CapturingBattleCategorySetted: [select_capturing_question],
    events.CapturingBattlePlayerAnswered: [check_capturing_battle_outcome],
    events.CapturingStageRoundFinished: [check_capturing_stage_round_outcome],
    events.CapturingStageFinished: [start_battlings_stage],
    # The Battlings Stage
    events.BattlingsStageStarted: [start_battlings_stage_round],
    events.BattlingsStageRoundStarted: [],
    events.FieldAttacked: [start_duel],
    events.BattlingsStageRoundEnded: [check_battlings_stage_round_outcome],
    events.BattlingsStageEnded: [finish_game],
    # The Duel
    events.DuelStarted: [select_duel_category],
    events.DuelCategorySetted: [start_duel_round],
    events.DuelRoundStarted: [select_duel_question],
    events.QuestionSetted: [],
    events.PlayerAnswered: [check_are_all_players_answered],
    events.DuelRoundFinished: [check_duel_round_outcome],
    events.DuelEnded: [finish_battlings_stage_round],
}
