import json

import aioredis

from infrastructure.ports import Producer


class RedisProducer(Producer):
    def __init__(self) -> None:
        self.redis = aioredis.Redis(host='localhost', port=6379, db=0, encoding='utf-8')

    async def publish(self, group: str, data: dict[str, str]) -> None:
        await self.redis.publish(group, json.dumps(data))
