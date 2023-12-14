from domain.models import Player

from infrastructure.ports.repositories import PlayersRepository

from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyPlayersRepository(PlayersRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def add(self, player: Player) -> None:
        self._session.add(player)

    async def get(self, id: int) -> Player:
        player = await self._session.get(Player, id)
        if player is None:
            # TODO: replace with proper exception
            raise ValueError(f'Player {id} not found')
        return player

    async def get_or_create(self, id: int) -> Player:
        player = await self._session.get(Player, id)
        if player is None:
            player = Player(id, None)
            self._session.add(player)
        return player
