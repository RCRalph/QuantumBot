import logging
import os
import re
from datetime import datetime

import discord

from embed_splitter import EmbedSplitter
from server import Server

logger = logging.getLogger(__name__)


class CommandController:
    EMBED_COLOUR = 0x2F3855
    COMMAND_PREFIX = os.environ.get("QUANTUM_BOT_PREFIX", "!")
    COMMAND_SPLIT_REGEX = r"((?:[^\s\"']+)|\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*')"
    QUOTATION_REMOVAL_REGEX = r"(^[\"']|[\"']$)"

    @classmethod
    def is_command(cls, message: discord.Message) -> bool:
        return message.content.startswith(cls.COMMAND_PREFIX)

    @classmethod
    async def reply(cls, message: discord.Message, server: Server) -> None:
        command = [
            re.sub(cls.QUOTATION_REMOVAL_REGEX, "", arg)
            for arg in re.findall(cls.COMMAND_SPLIT_REGEX, message.content[1:])
        ]

        match command[0].lower():
            case "test":
                await cls._reply_test(message, server)
            case "schedule":
                await cls._reply_schedule(message, server, command)

    @classmethod
    async def _reply_test(cls, message: discord.Message, server: Server) -> None:
        await message.channel.send(server.language.config.message.test)

    @classmethod
    async def _reply_schedule(
        cls, message: discord.Message, server: Server, command: list[str]
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
            color=cls.EMBED_COLOUR,
        )

        for embed in EmbedSplitter(embed, list(fields), server.HEADER_PREFIX):
            await message.channel.send(embed=embed)
