from typing import AsyncGenerator

import aioredis

from infrastructure.adapters import messages
from infrastructure.ports import Consumer

import pika


class RedisConsumer(Consumer):
    def __init__(self) -> None:
        self.redis = aioredis.Redis(host='localhost', port=6379, db=0, encoding='utf-8')
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)

    async def subscribe(self, group: str) -> None:
        await self.pubsub.subscribe(group)

    async def unsubscribe(self, group: str) -> None:
        await self.pubsub.unsubscribe(group)
        await self.redis.close()

    async def listen(self) -> AsyncGenerator[messages.RedisMessage, None]:
        async for message in self.pubsub.listen():
            yield messages.RedisMessage(message)


class RabbitMQConsumer(Consumer):
    connection_params = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/')

    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='games', exchange_type='topic', durable=True)

    async def subscribe(self, group: str) -> None:
        self.channel.queue_declare(queue=group)
        self.channel.queue_bind(queue=group, exchange='games')

    async def unsubscribe(self, group: str) -> None:
        self.channel.queue_unbind(queue=group, exchange='games')

    async def listen(self) -> AsyncGenerator[messages.RabbitMQMessage, None]:
        for message in self.channel.consume(queue='game.events', auto_ack=True):
            yield messages.RabbitMQMessage(*message)
