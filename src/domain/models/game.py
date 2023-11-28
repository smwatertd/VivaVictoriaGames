from core.settings import game_settings

from domain import enums, events, exceptions
from domain.models.field import Field
from domain.models.model import Model
from domain.models.player import Player
from domain.models.strategies import PlayerTurnSelector

from questions import Question


class Game(Model):
    def __init__(
        self,
        id: int,
        players: list[Player],
        state: enums.GameState,
        fields: list[Field],
        round_number: int = 0,
        question: Question | None = None,
    ) -> None:
        super().__init__(id)
        self.id = id
        self.state = state
        self.round_number = round_number
        self._players = players
        self._fields = fields
        self._question = question

    def __repr__(self) -> str:
        return """Game(id={}, state={}, round_number={}, players={}, fields={}, question={})""".format(
            self.id,
            self.state,
            self.round_number,
            self._players,
            self._fields,
            self._question,
        )

    def add_player(self, player: Player) -> None:
        self._ensure_can_add_player(player)
        self._add_player(player)
        self._try_close()

    def remove_player(self, player: Player) -> None:
        self._remove_player(player)

    def start(self) -> None:
        self.round_number = 1
        self._set_state(enums.GameState.STARTED)
        self.register_event(events.GameStarted(game_id=self.id))

    def select_player_turn(self, player_turn_selector: PlayerTurnSelector) -> None:
        self._select_player_turn(player_turn_selector)
        self._set_state(enums.GameState.ATTACK_WAITING)

    def _ensure_can_add_player(self, player: Player) -> None:
        if self.state != enums.GameState.PLAYERS_WAITING:
            raise exceptions.GameInvalidState(self.state)
        if player in self._players:
            raise exceptions.PlayerAlreadyAdded()

    def _add_player(self, player: Player) -> None:
        self._players.append(player)
        self.register_event(
            events.PlayerAdded(
                game_id=self.id,
                player_id=player.id,
                username=player.username,
            ),
        )

    def _try_close(self) -> None:
        if self._is_full():
            self.register_event(events.GameClosed(game_id=self.id))
            self._set_state(enums.GameState.START_WAITING)

    def _remove_player(self, player: Player) -> None:
        self._players.remove(player)
        self.register_event(
            events.PlayerRemoved(
                game_id=self.id,
                player_id=player.id,
                username=player.username,
            ),
        )

    def _select_player_turn(self, player_turn_selector: PlayerTurnSelector) -> None:
        player_turn = player_turn_selector.select(self.round_number, self._players)
        self.register_event(
            events.PlayerTurnChanged(
                game_id=self.id,
                player_id=player_turn.id,
            ),
        )

    def _is_full(self) -> bool:
        return len(self._players) == game_settings.players_count_to_start

    def _set_state(self, state: enums.GameState) -> None:
        self.state = state
        self.register_event(events.GameStateChanged(game_id=self.id, state=state))
