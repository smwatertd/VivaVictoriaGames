from domain import models

from infrastructure.ports.repositories import PlayersRepository

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class SQLAlchemyPlayersRepository(PlayersRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def add(self, player: models.Player) -> None:
        self._session.add(player)

    async def get(self, id: int) -> models.Player:
        result = await self._session.execute(
            select(models.Player)
            .where(models.Player._id == id)
            .options(
                joinedload(models.Player._fields),
                joinedload(models.Player._marked_field),
            ),
        )
        player = result.unique().scalar_one_or_none()
        if player is None:
            # TODO: replace with proper exception
            raise ValueError(f'Player {id} not found')
        return player

    async def get_or_create(self, id: int) -> models.Player:
        player = await self._session.get(models.Player, id)
        if player is None:
            player_id = await self._session.execute(insert(models.Player).values(id=id).returning(models.Player._id))
            player = await self._session.get(models.Player, player_id.scalar_one())
        return player
