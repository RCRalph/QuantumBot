import logging

import discord

from client.command import CommandController
from client.reaction import ReactionController
from server import Server

logger = logging.getLogger(__name__)


class Client(discord.Client):
    async def on_ready(self) -> None:
        logger.info("Logged in as %s", self.user)

        self.servers = Server.from_directory()

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return

        if message.guild is None:
            logger.warning("Message guild not found")
            return

        if (server := self.servers.get(message.guild.id)) is None:
            logger.error("Server %s not found", message.guild.id)
            return

        if CommandController.is_command(message):
            await CommandController.reply(message, server)
        elif ReactionController.is_reactable(message, server):
            await ReactionController.add_reactions(message, server)
