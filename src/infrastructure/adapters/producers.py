import aioredis

from infrastructure.ports import Producer


class RedisProducer(Producer):
    def __init__(self) -> None:
        self.redis = aioredis.Redis(host='localhost', port=6379, db=0)

    async def publish(self, channel: str, message: dict) -> None:
        await self.redis.publish(channel, str(message))
