import logging
import os

import aiocron
import discord

from client.announcement import AnnouncementController
from server import Server

logger = logging.getLogger(__name__)


class Client(discord.Client):
    COMMAND_PREFIX = os.environ.get("QUANTUM_BOT_PREFIX", "!")

    async def on_ready(self) -> None:
        logger.info("Logged in as %s", self.user)

        self.servers = Server.from_directory()

        self._announcement_controller = AnnouncementController(self)
        self._announcement_cron = aiocron.crontab(
            "* * * * *", self._announcement_controller.send_announcements
        )
