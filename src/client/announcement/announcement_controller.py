import logging
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import discord

from client.announcement.announcement import Announcement

if TYPE_CHECKING:
    from client import Client


logger = logging.getLogger(__name__)


class AnnouncementController:
    def __init__(self, client: "Client"):
        self._client = client

    def _get_announcements_to_send(self) -> set[Announcement]:
        current_datetime = datetime.now(timezone.utc).replace(second=0, microsecond=0)

        return {
            Announcement(server, event)
            for server in self._client.servers.values()
            for event in server.events
            for announcement in event.announcements
            if current_datetime + timedelta(minutes=announcement) == event.start_time
        }

    async def send_announcements(self) -> None:
        if not (announcements := self._get_announcements_to_send()):
            return

        logger.info("Announcement count: %s", len(announcements))

        for item in announcements:
            if not isinstance(
                channel := self._client.get_channel(item.channel_id),
                discord.abc.Messageable,
            ):
                raise ValueError(
                    f"Cannot send messages to channel ID {item.channel_id}"
                )

            await channel.send("@everyone", embed=item.embed)
            logger.info("Sent announcement: %s", item.name)
