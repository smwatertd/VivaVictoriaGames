from domain import events

from infrastructure.ports import Factory


class EventFactory(Factory):
    registry = {
        'PlayerAdded': events.PlayerAdded,
        'PlayerRemoved': events.PlayerRemoved,
    }


class CommandFactory(Factory):
    registry: dict = {}
