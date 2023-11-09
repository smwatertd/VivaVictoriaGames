from infrastructure.adapters.producers import RedisProducer
from infrastructure.ports import UnitOfWork


class UnitOfWorkAdapter(UnitOfWork):
    async def rollback(self) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def publish_events(self) -> None:
        producer = RedisProducer()
        for game in self.games.seen:
            for event in game.collect_events():
                await producer.publish(event.game_pk, str(event.model_dump()))
            game._events.clear()
