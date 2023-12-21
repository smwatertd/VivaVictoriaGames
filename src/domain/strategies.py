from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from domain.models import Player


class PlayerTurnSelector(ABC):
    def select(self, round_number: int, players: list['Player']) -> 'Player':
        sorted_players = self.get_order(players)
        return sorted_players[(round_number - 1) % len(sorted_players)]

    @abstractmethod
    def get_order(self, players: list['Player']) -> list['Player']:
        pass


class IdentityPlayerTurnSelector(PlayerTurnSelector):
    def get_order(self, players: list['Player']) -> list['Player']:
        return sorted(players, key=lambda player: -player.get_id())


class ConnectionTimeAndIdentityPlayerTurnSelector(PlayerTurnSelector):
    def get_order(self, players: list['Player']) -> list['Player']:
        return sorted(players, key=lambda player: (player.get_connected_at(), player.get_id()))
