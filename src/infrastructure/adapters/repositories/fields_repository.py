from domain.models import Field

from infrastructure.ports.repositories import FieldsRepository

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class SQLAlchemyFieldsRepository(FieldsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, id: int) -> Field:
        result = await self._session.execute(
            select(Field)
            .where(Field._id == id)
            .options(
                joinedload(Field._owner),
            ),
        )
        field = result.scalars().first()
        if field is None:
            # TODO: replace with proper exception
            raise ValueError(f'Field {id} not found')
        return field
