from domain import events

from infrastructure.ports import Factory


class EventFactory(Factory):
    registry = {
        'PlayerAdded': events.PlayerAdded,
        'PlayerRemoved': events.PlayerRemoved,

        'GameStarted': events.GameStarted,
        'GameFinished': events.GameFinished,

        'StageStarted': events.StageStarted,
        'StageFinished': events.StageFinished,

        'RoundStarted': events.RoundStarted,
        'RoundFinished': events.RoundFinished,

        'QuestionSetted': events.QuestionSetted,
        'PlayerAnsweredImplicitly': events.PlayerAnsweredImplicitly,
        'AllPlayersAnswered': events.AllPlayersAnswered,

        'BaseSelected': events.BaseSelected,

        'PlayerImplicitlyMarkedField': events.PlayerImplicitlyMarkedField,
        'AllPlayersMarkedFields': events.AllPlayersMarkedFields,
        'MarkedFieldsCaptured': events.MarkedFieldsCaptured,
        'MarkingConflictDetected': events.MarkingConflictDetected,
        'MarkingBattleStarted': events.MarkingBattleStarted,
        'MarkingBattleFinished': events.MarkingBattleFinished,

        'FieldAttacked': events.FieldAttacked,
        'DuelStarted': events.DuelStarted,
        'DuelRoundStarted': events.DuelRoundStarted,
        'DuelRoundFinished': events.DuelRoundFinished,
        'DuelFinished': events.DuelFinished,
    }


class CommandFactory(Factory):
    registry: dict = {}
