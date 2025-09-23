from typing import Any

import discord

from server import BaseEvent, Server


class Announcement:
    EMBED_COLOUR = 0x2F3855

    def __init__(self, server: Server, event: BaseEvent):
        self._server = server
        self._event = event

    @property
    def embed(self) -> discord.Embed:
        result = discord.Embed(
            title=self._server.language.config.embed.reminder, colour=self.EMBED_COLOUR
        )

        result.add_field(
            name=self._event.get_embed_name(self._server.timezones),
            value=self._event.get_embed_value(self._server.timezones),
            inline=False,
        )

        return result

    @property
    def channel_id(self) -> int:
        return self._server.announcement_channel_id

    @property
    def name(self) -> str | None:
        return self.embed.fields[0].name

    @property
    def comparison_key(self) -> tuple[int, str | None]:
        return (self.channel_id, self.name)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Announcement):
            return False

        return self.comparison_key == other.comparison_key

    def __hash__(self) -> int:
        return hash(self.comparison_key)
