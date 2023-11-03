from typing import Callable

import aioredis

from infrastructure.ports import Consumer


class RedisConsumer(Consumer):
    def __init__(self, on_message: Callable) -> None:
        self.redis = aioredis.Redis(host='localhost', port=6379, db=0)
        self.pubsub = self.redis.pubsub()

    async def subscribe(self, group: str) -> None:
        await self.pubsub.subscribe(group)

    async def unsubscribe(self, group: str) -> None:
        await self.pubsub.unsubscribe(group)
        await self.redis.close()
