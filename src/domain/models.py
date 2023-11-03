from typing import Iterable

from domain import enums, events, exceptions
from domain.value_objects import Player

from questions import Question


USER_COUNT = 3


class Model:
    def __init__(self) -> None:
        self._events: list[events.Event] = []

    def _add_event(self, event: events.Event) -> None:
        self._events.append(event)

    def get_events(self) -> list[events.Event]:
        return self._events


class Game(Model):
    def __init__(
        self,
        pk: int,
        players: Iterable[Player] | None = None,
        state: enums.GameState = enums.GameState.PLAYERS_WAITING,
        question: Question | None = None,
    ) -> None:
        super().__init__()
        self._pk = pk
        self._players = set(players) if players else set()
        self._state = state
        self._question = question

    def add_player(self, player: Player) -> None:
        if self._is_begin():
            raise exceptions.GameInvalidState
        self._add_player(player)
        if self._is_users_count_limit():
            self._start()

    def discard_player(self, player: Player) -> None:
        self._players.discard(player)
        self._add_event(events.UserDisconnected(id=self._pk, user_id=player.id))

    def set_question(self, question: Question) -> None:
        self._question = question

    def _start(self) -> None:
        self._state = enums.GameState.STARTED
        self._add_event(events.GameStarted(id=self._pk))

    def _is_begin(self) -> bool:
        return self._state != enums.GameState.PLAYERS_WAITING

    def _add_player(self, player: Player) -> None:
        self._players.add(player)
        self._add_event(events.UserConnected(id=self._pk, user_id=player.pk))

    def _is_users_count_limit(self) -> bool:
        return len(self._players) == USER_COUNT
