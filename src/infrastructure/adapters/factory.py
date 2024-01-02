from domain import events

from infrastructure.ports import Factory


class EventFactory(Factory):
    registry = {
        'PlayerAdded': events.PlayerAdded,
        'PlayerRemoved': events.PlayerRemoved,

        'GameStarted': events.GameStarted,
        'GameFinished': events.GameFinished,

        'LimitedByRoundsStageStarted': events.LimitedByRoundsStageStarted,
        'OrderedRoundStarted': events.OrderedRoundStarted,
        'BaseSelected': events.BaseSelected,
        'RoundFinished': events.RoundFinished,
        'StageFinished': events.StageFinished,


        # 'PreparatoryStageStarted': events.PreparatoryStageStarted,
        # 'SelectingBaseStageRoundStarted': events.SelectingBaseStageRoundStarted,
        # 'BaseSelected': events.BaseSelected,
        # 'SelectingBaseStageRoundFinished': events.SelectingBaseStageRoundFinished,
        # 'SelectingBaseStageFinished': events.SelectingBaseStageFinished,

        # 'CapturingStageStarted': events.CapturingStageStarted,
        # 'CapturingStageRoundStarted': events.CapturingStageRoundStarted,
        # 'FieldMarked': events.FieldMarked,
        # 'FieldsMarked': events.FieldsMarked,
        # 'MarkingConflictDetected': events.MarkingConflictDetected,
        # 'CapturingBattleStarted': events.CapturingBattleStarted,
        # 'CapturingBattleCategorySetted': events.CapturingBattleCategorySetted,
        # 'CapturingBattleQuestionSetted': events.CapturingBattleQuestionSetted,
        # 'CapturingBattlePlayerAnswered': events.CapturingBattlePlayerAnswered,
        # 'CapturingStageRoundFinished': events.CapturingStageRoundFinished,
        # 'CapturingStageFinished': events.CapturingStageFinished,

        # 'BattlingsStageStarted': events.BattlingsStageStarted,
        # 'BattlingsStageRoundStarted': events.BattlingsStageRoundStarted,
        # 'FieldAttacked': events.FieldAttacked,
        # 'BattlingsStageRoundEnded': events.BattlingsStageRoundEnded,
        # 'BattlingsStageEnded': events.BattlingsStageEnded,

        # 'DuelStarted': events.DuelStarted,
        # 'DuelCategorySetted': events.DuelCategorySetted,
        # 'DuelRoundStarted': events.DuelRoundStarted,
        # 'QuestionSetted': events.QuestionSetted,
        # 'PlayerAnswered': events.PlayerAnswered,
        # 'DuelRoundFinished': events.DuelRoundFinished,
        # 'DuelEnded': events.DuelEnded,
    }


class CommandFactory(Factory):
    registry: dict = {}
