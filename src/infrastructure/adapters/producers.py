import json

import aio_pika

from infrastructure.adapters.messages import Message
from infrastructure.ports.producers import Producer


class RabbitMQProducer(Producer):
    def __init__(self, host: str, port: int, virtual_host: str, exchange: str) -> None:
        self._host = host
        self._port = port
        self._virtual_host = virtual_host
        self._exchange = exchange

    async def publish(self, group: str, message: Message) -> None:
        connection = await aio_pika.connect(host=self._host, port=self._port, virtualhost=self._virtual_host)
        async with connection.channel() as channel:
            exchange = await channel.get_exchange(self._exchange)
            await exchange.publish(
                message=aio_pika.Message(
                    body=json.dumps(message.payload).encode(),
                    headers={
                        'type': message.type.value,
                        'payload_type': message.payload_type,
                    },
                ),
                routing_key=group,
            )
        await connection.close()
