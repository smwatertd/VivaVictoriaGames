from infrastructure.ports import UnitOfWork


class UnitOfWorkAdapter(UnitOfWork):
    async def rollback(self) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def publish_events(self) -> None:
        for game in self.games.seen:
            for event in game.collect_events():
                await self._event_producer.publish(event.game_pk, event.model_dump())
            game._events.clear()
