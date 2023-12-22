from domain import events

from infrastructure.ports import Factory


class EventFactory(Factory):
    registry = {
        'PlayerAdded': events.PlayerAdded,
        'PlayerRemoved': events.PlayerRemoved,
        'GameStarted': events.GameStarted,
        'RoundStarted': events.RoundStarted,
        'RoundFinished': events.RoundFinished,
        'FieldAttacked': events.FieldAttacked,
        'FieldCaptured': events.FieldCaptured,
        'PlayerFieldAttacked': events.PlayerFieldAttacked,
        'DuelStarted': events.DuelStarted,
        'DuelRoundStarted': events.DuelRoundStarted,
        'DuelRoundFinished': events.DuelRoundFinished,
        'CategorySetted': events.CategorySetted,
        'QuestionSetted': events.QuestionSetted,
        'DuelEnded': events.DuelEnded,
        'PlayerAnswered': events.PlayerAnswered,
        'GameEnded': events.GameEnded,
        'FieldDefended': events.FieldDefended,
        'RoundTimerStarted': events.RoundTimerStarted,
        'DuelRoundTimerStarted': events.DuelRoundTimerStarted,
    }


class CommandFactory(Factory):
    registry: dict = {}
