from random import choice

from infrastructure.ports.clients import HTTPClient


class CategoriesClient:
    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    async def random(self) -> int:
        categories = await self._client.get_all_categories()
        return choice(categories).id
