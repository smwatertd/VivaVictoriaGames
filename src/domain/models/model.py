from typing import Generator

from domain.events import Event


class Model:
    def __init__(self) -> None:
        self._events: list[Event] = []

    def register_event(self, event: Event) -> None:
        self._events.append(event)

    def collect_events(self) -> Generator[Event, None, None]:
        for event in self._events:
            self._events.remove(event)
            yield event
