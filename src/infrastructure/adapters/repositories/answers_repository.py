from domain.models import Answer

from infrastructure.ports.repositories import AnswersRepository

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyAnswersRepository(AnswersRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, id: int) -> Answer:
        result = await self._session.execute(
            select(Answer)
            .where(Answer.id == id),
        )
        answer = result.scalars().first()
        if answer is None:
            # TODO: replace with proper exception
            raise ValueError(f'Answer {id} not found')
        return answer
