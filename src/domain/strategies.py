from abc import ABC, abstractmethod

from domain.models import Player


class PlayerTurnSelector(ABC):
    @abstractmethod
    def select(self, round_number: int, players: list[Player]) -> Player:
        pass

    @abstractmethod
    def get_order(self, players: list[Player]) -> list[Player]:
        pass


class IdentityPlayerTurnSelector(PlayerTurnSelector):
    def select(self, round_number: int, players: list[Player]) -> Player:
        sorted_players_by_id = self.get_order(players)
        return sorted_players_by_id[round_number % len(sorted_players_by_id)]

    def get_order(self, players: list[Player]) -> list[Player]:
        return sorted(players, key=lambda player: -player.get_id())


class ConnectionTimeAndIdentityPlayerTurnSelector(PlayerTurnSelector):
    def select(self, round_number: int, players: list[Player]) -> Player:
        sorted_players_by_connected_at = self.get_order(players)
        return sorted_players_by_connected_at[round_number % len(sorted_players_by_connected_at)]

    def get_order(self, players: list[Player]) -> list[Player]:
        return sorted(players, key=lambda player: (player.get_connected_at(), player.get_id()))
