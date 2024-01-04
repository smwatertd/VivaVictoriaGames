from typing import TYPE_CHECKING

from domain.models.field import Field


if TYPE_CHECKING:
    from domain.models.player import Player


class MarkedField:
    def __init__(self, field: Field, players: list['Player']) -> None:
        self._field = field
        self._players: list['Player'] = players

    def get_id(self) -> int:
        return self._field.get_id()

    def get_field(self) -> Field:
        return self._field

    def get_players(self) -> list['Player']:
        return self._players

    def add_player(self, player: 'Player') -> None:
        self._players.append(player)

    def get_single_player(self) -> 'Player':
        if len(self._players) != 1:
            raise ValueError('Cannot get single player with multiple or no players')
        return self._players[0]
