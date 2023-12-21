import asyncio

from core.container import container
from core.settings import rabbitmq_settings

from main import app  # noqa


async def main() -> None:
    serializer = container.message_serializer()
    consumer = container.message_consumer()
    async for message in consumer.listen(rabbitmq_settings.games_events_queue):
        await container.messagebus().handle(serializer.deserialize(message), container.unit_of_work())
        await consumer.commit()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
