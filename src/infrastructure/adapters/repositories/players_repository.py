from domain.models import Player

from infrastructure.ports.repositories import PlayersRepository


class InMemoryPlayersRepository(PlayersRepository):
    players: dict[int, Player] = {}

    async def get(self, pk: int) -> Player:
        self.seen.add(self.players[pk])
        return Player(pk=pk, username=f'client{pk}')

    async def create(self, player: Player) -> Player:
        self.players[player.pk] = player
        return player
