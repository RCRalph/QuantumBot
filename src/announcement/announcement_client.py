import logging
from datetime import datetime, timedelta, timezone

import aiocron
import discord

from announcement.announcement import Announcement
from server import Server

logger = logging.getLogger(__name__)


class AnnouncementClient(discord.Client):
    async def on_ready(self) -> None:
        logger.info("Logged in as %s", self.user)

        self.servers = Server.from_directory()
        self._announcement_cron = aiocron.crontab("* * * * *", self.send_announcements)

    def _get_announcements_to_send(self) -> set[Announcement]:
        current_datetime = datetime.now(timezone.utc).replace(second=0, microsecond=0)

        return {
            Announcement(server, event)
            for server in self.servers.values()
            for event in server.events
            for announcement in event.announcements
            if current_datetime + timedelta(minutes=announcement) == event.start_time
        }

    async def send_announcements(self) -> None:
        announcements = self._get_announcements_to_send()
        logger.info("Announcement count: %s", len(announcements))

        for item in announcements:
            if not isinstance(
                channel := self.get_channel(item.channel_id),
                discord.abc.Messageable,
            ):
                raise ValueError(
                    f"Cannot send messages to channel ID {item.channel_id}"
                )

            await channel.send("@everyone", embed=item.embed)
            logger.info("Sent announcement: %s", item.name)
