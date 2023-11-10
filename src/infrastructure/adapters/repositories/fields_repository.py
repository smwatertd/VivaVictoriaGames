from domain.models import Field

from infrastructure.adapters.repositories.games_repository import InMemoryGamesRepository
from infrastructure.ports.repositories import FieldsRepository


class InMemoryFieldsRepository(FieldsRepository):
    fields: dict[int, Field] = {}

    async def get(self, pk: int) -> Field:
        for _, game in InMemoryGamesRepository.games.items():
            for field in game._fields:
                if field._pk == pk:
                    return field
        return Field(pk=pk)
