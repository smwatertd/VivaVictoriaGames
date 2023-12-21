from domain.models import Duel, Game, Player

from infrastructure.ports.repositories import GamesRepository

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class SQLAlchemyGamesRepository(GamesRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def get(self, id: int) -> Game:
        result = await self._session.execute(
            select(Game)
            .where(Game._id == id)
            .options(
                joinedload(Game._players)
                .joinedload(Player._fields),
                joinedload(Game._fields),
                joinedload(Game._duel)
                .joinedload(Duel._attacker),
                joinedload(Game._duel)
                .joinedload(Duel._defender),
                joinedload(Game._player_order),
            ),
        )
        game = result.scalars().first()
        if game is None:
            # TODO: replace with proper exception
            raise ValueError(f'Game {id} not found')
        self.seen.add(game)
        return game
