from abc import ABC, abstractmethod
from typing import Iterable

from domain.models.player import Player


class PlayerTurnSelector(ABC):
    @abstractmethod
    def select(self, round_number: int, players: Iterable[Player]) -> Player:
        pass


class IdentityPlayerTurnSelector(PlayerTurnSelector):
    def select(self, round_number: int, players: Iterable[Player]) -> Player:
        sorted_players_by_id = sorted(players, key=lambda player: player.id)
        return sorted_players_by_id[round_number % len(sorted_players_by_id)]
