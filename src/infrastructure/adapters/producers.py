import json

import aioredis

from infrastructure.ports.producers import Producer

import pika


class RedisProducer(Producer):
    def __init__(self) -> None:
        self.redis = aioredis.Redis(host='localhost', port=6379, db=0, encoding='utf-8')

    async def publish(self, group: str, data: dict[str, str]) -> None:
        await self.redis.publish(group, json.dumps(data))


class RabbitMQProducer(Producer):
    connection_params = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/')

    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

    async def publish(self, group: str, data: dict[str, str]) -> None:
        props = pika.BasicProperties(headers={
            'message_type': 'event',
            'payload_type': data['event_type'],
        })
        self.channel.basic_publish(
            exchange='games',
            routing_key='games.events.all',
            body=json.dumps(data),
            properties=props,
        )
