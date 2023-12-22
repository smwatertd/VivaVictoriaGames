from collections import defaultdict

from infrastructure.adapters.channels import Channel


class ChannelLayer:
    channels: defaultdict[str, set[Channel]] = defaultdict(set)

    async def group_add(self, group: str, channel: Channel) -> None:
        self._add_channel(group, channel)
        await channel.subscribe(group)

    async def group_discard(self, group: str, channel_id: str) -> None:
        channel = self._get_channel(group, channel_id)
        await channel.unsubscribe()
        self._remove_channel(group, channel)

    def _get_channel(self, group: str, id: str) -> Channel:
        for channel in self.channels[group]:
            if channel.get_id() == id:
                return channel
        raise KeyError('Channel not found')

    def _add_channel(self, group: str, channel: Channel) -> None:
        self.channels[group].add(channel)

    def _remove_channel(self, group: str, channel: Channel) -> None:
        self.channels[group].remove(channel)
