from random import choice

from domain.models import Category

from infrastructure.ports.clients import HTTPClient


class CategoriesClient:
    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    async def random(self) -> Category:
        categories = await self._client.get_all_categories()
        random_category = choice(categories)
        return Category(id=random_category.id, name=random_category.name)
