import logging
import re
from datetime import datetime
from typing import TYPE_CHECKING

import discord

from embed_splitter import EmbedSplitter
from server import Server

if TYPE_CHECKING:
    from client.client import Client


logger = logging.getLogger(__name__)


class CommandController:
    EMBED_COLOUR = 0x2F3855
    COMMAND_SPLIT_REGEX = r"((?:[^\s\"']+)|\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*')"
    QUOTATION_REMOVAL_REGEX = r"(^[\"']|[\"']$)"

    def __init__(self, client: "Client") -> None:
        self.client = client

    async def reply(self, message: discord.Message) -> None:
        if message.guild is None:
            logger.warning("Message guild not found")
            return

        if (server := self.client.servers.get(message.guild.id)) is None:
            logger.error("Server %s not found", message.guild.id)
            return

        command = [
            re.sub(self.QUOTATION_REMOVAL_REGEX, "", arg)
            for arg in re.findall(self.COMMAND_SPLIT_REGEX, message.content[1:])
        ]

        match command[0].lower():
            case "test":
                await self._reply_test(message, server)
            case "schedule":
                await self._reply_schedule(message, server, command)

    async def _reply_test(self, message: discord.Message, server: Server) -> None:
        await message.channel.send(server.language.config.message.test)

    async def _reply_schedule(
        self, message: discord.Message, server: Server, command: list[str]
    ) -> None:
        is_full_schedule = len(command) > 1 and command[1].lower() in {"full", "all"}

        if is_full_schedule:
            schedule_title_prefix = server.language.config.embed.schedule
            fields = server.get_full_schedule_embed_fields()
        else:
            schedule_title_prefix = server.language.config.embed.schedule_today
            fields = server.get_todays_schedule_embed_fields(
                datetime.now(server.timezones[0].zone_info).date()
            )

        embed = discord.Embed(
            title=f"{schedule_title_prefix} - {server.name}",
            color=self.EMBED_COLOUR,
        )

        for embed in EmbedSplitter(embed, list(fields), server.HEADER_PREFIX):
            await message.channel.send(embed=embed)
