from domain import enums, events, exceptions
from domain.models.field import Field
from domain.models.model import Model
from domain.models.player import Player

PLAYERS_COUNT = 3


def select_player_order_by_pk(players: list[Player]) -> Player:
    return min(players, key=lambda player: player.pk)


class Game(Model):
    def __init__(
        self,
        pk: int,
        players: list[Player],
        state: enums.GameState,
        fields: list[Field],
        player_order: Player | None = None,
    ) -> None:
        super().__init__(pk)
        self._players = players
        self._state = state
        self._player_order = player_order
        self._fields = fields

    def add_player(self, player: Player) -> None:
        self._ensure_can_add_player(player)
        self._add_player(player)
        self._try_start()

    def remove_player(self, player: Player) -> None:
        self._remove_player(player)

    def _ensure_can_add_player(self, player: Player) -> None:
        if player in self._players:
            raise exceptions.PlayerAlreadyAdded
        if len(self._players) == PLAYERS_COUNT:
            raise exceptions.GameIsFull

    def _add_player(self, player: Player) -> None:
        self._players.append(player)
        self._register_event(events.PlayerAdded(
            game_pk=self._pk,
            player_pk=player.pk,
            username=player.username,
        ))

    def _try_start(self) -> None:
        if self._can_start():
            self._start()

    def _remove_player(self, player: Player) -> None:
        self._players.remove(player)
        self._register_event(events.PlayerRemoved(
            game_pk=self._pk,
            player_pk=player._pk,
        ))

    def _can_start(self) -> bool:
        return len(self._players) == PLAYERS_COUNT and self._state == enums.GameState.PLAYERS_WAITING

    def _start(self) -> None:
        self._set_state(enums.GameState.STARTED)
        self._set_player_order(select_player_order_by_pk(self._players))

    def _set_state(self, state: enums.GameState) -> None:
        self._state = state
        if state == enums.GameState.STARTED:
            self._register_event(events.GameStarted(
                game_pk=self._pk,
                state=state,
            ))

    def _set_player_order(self, player_order: Player) -> None:
        self._player_order = player_order
        self._register_event(events.PlayerTurnChanged(
            game_pk=self._pk,
            player_pk=player_order.pk,
        ))
