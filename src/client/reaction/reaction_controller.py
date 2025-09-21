import logging
from typing import TYPE_CHECKING

import discord

if TYPE_CHECKING:
    from client.client import Client


logger = logging.getLogger(__name__)


class ReactionController:
    def __init__(self, client: "Client"):
        self.client = client

    async def add_reactions(self, message: discord.Message) -> None:
        if message.guild is None:
            logger.warning("Message guild not found")
            return

        if (server := self.client.servers.get(message.guild.id)) is None:
            logger.warning("Server %s not found", message.guild.id)
            return

        if (reaction := server.reactions.get(message.channel.id)) is None:
            return

        if reaction.prompt_text.lower() not in message.content.lower():
            return

        for emoji in reaction.emojis:
            await message.add_reaction(emoji)
