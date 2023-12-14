from random import randint

from domain.models import Category

from infrastructure.ports.repositories import CategoriesRepository


class HTTPCategoriesRepository(CategoriesRepository):
    async def random(self) -> Category:
        return Category(randint(1, 1000))
