import logging

import discord

from server import Server

logger = logging.getLogger(__name__)


class ReactionController:
    @classmethod
    def is_reactable(cls, message: discord.Message, server: Server) -> bool:
        if (reaction := server.reactions.get(message.channel.id)) is None:
            return False

        return reaction.prompt_text.lower() in message.content.lower()

    @classmethod
    async def add_reactions(cls, message: discord.Message, server: Server) -> None:
        for emoji in server.reactions[message.channel.id].emojis:
            await message.add_reaction(emoji)
