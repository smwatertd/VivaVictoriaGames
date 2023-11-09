from typing import AsyncIterator

import aioredis

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

    def listen(self) -> AsyncIterator:
        return self.pubsub.listen()


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

    def listen(self) -> AsyncIterator:
        return self.channel.consume(queue='game.events', auto_ack=True)
