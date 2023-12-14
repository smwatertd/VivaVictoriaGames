from domain.events import Event


class Model:
    def __init__(self) -> None:
        self._set_events_default()

    def register_event(self, event: Event) -> None:
        self._events.append(event)

    def collect_events(self) -> list[Event]:
        return self._events

    def clear_events(self) -> None:
        self._set_events_default()

    def _set_events_default(self) -> None:
        self._events: list[Event] = []
