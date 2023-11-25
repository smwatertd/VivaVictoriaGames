from domain.events import Event


class Model:
    def __init__(self, id: int) -> None:
        self._id: int = id
        self._events: list[Event] = []

    def _register_event(self, event: Event) -> None:
        self._events.append(event)

    def collect_events(self) -> list[Event]:
        return self._events
