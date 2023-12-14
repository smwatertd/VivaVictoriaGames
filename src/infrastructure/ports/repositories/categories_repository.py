from abc import ABC, abstractmethod

from domain.models import Category

from infrastructure.ports.repositories.repository import Repository


class CategoriesRepository(Repository, ABC):
    @abstractmethod
    async def random(self) -> Category:
        pass
