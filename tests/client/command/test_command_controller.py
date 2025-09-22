import logging
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import discord
import pytest
from freezegun import freeze_time

from client.client import Client
from client.command.command_controller import CommandController
from embed_splitter.embed_field import EmbedField


class TestCommandController:
    EXAMPLE_SERVER_ID = 12345

    @pytest.mark.asyncio
    async def test_reply_test(self, mock_client: Client) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_SERVER_ID
        mock_message.channel.send = AsyncMock()
        mock_message.content = "!test"

        controller = CommandController(mock_client)

        # Act
        await controller.reply(mock_message)

        # Assert
        mock_message.channel.send.assert_awaited_once_with(
            "If you can see this message and it's in the expected "
            "language, that means the configuration is correct!"
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "command",
        ["!schedule full", '!schedule "full"', "!schedule all", '!schedule "all"'],
    )
    async def test_reply_schedule_full(
        self,
        mock_client: Client,
        command: str,
        example_full_schedule_embed_fields: list[EmbedField],
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_SERVER_ID
        mock_message.channel.send = AsyncMock()
        mock_message.content = command

        expected_embed = discord.Embed(
            title="Schedule - QNickel16", colour=CommandController.EMBED_COLOUR
        )
        for field in example_full_schedule_embed_fields:
            expected_embed.add_field(
                name=field.name, value=field.value, inline=field.inline
            )

        controller = CommandController(mock_client)

        # Act
        await controller.reply(mock_message)

        # Assert
        mock_message.channel.send.assert_awaited_once_with(embed=expected_embed)

    @freeze_time(datetime(2024, 10, 7, 16, 50, tzinfo=timezone.utc))
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "command",
        ["!schedule", "!schedule today", '!schedule "today"'],
    )
    async def test_reply_schedule_today(
        self,
        mock_client: Client,
        command: str,
        example_full_schedule_embed_fields: list[EmbedField],
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_SERVER_ID
        mock_message.channel.send = AsyncMock()
        mock_message.content = command

        expected_embed = discord.Embed(
            title="Today's schedule - QNickel16", colour=CommandController.EMBED_COLOUR
        )
        for field in example_full_schedule_embed_fields[1:3]:
            expected_embed.add_field(
                name=field.name, value=field.value, inline=field.inline
            )

        controller = CommandController(mock_client)

        # Act
        await controller.reply(mock_message)

        # Assert
        mock_message.channel.send.assert_awaited_once_with(embed=expected_embed)

    @pytest.mark.asyncio
    async def test_reply_unknown_command(self, mock_client: Client) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_SERVER_ID
        mock_message.channel.send = AsyncMock()
        mock_message.content = "!unknown"

        controller = CommandController(mock_client)

        # Act
        await controller.reply(mock_message)

        # Assert
        mock_message.channel.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_reply_message_guild_not_found(
        self, mock_client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild = None

        expected_log_message = "Message guild not found"

        controller = CommandController(mock_client)

        # Act
        with caplog.at_level(logging.WARNING, "client.command.command_controller"):
            await controller.reply(mock_message)

        # Assert
        assert expected_log_message in caplog.text
        mock_message.channel.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_reply_server_not_found(
        self, mock_client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_SERVER_ID * 2

        expected_log_message = f"Server {self.EXAMPLE_SERVER_ID * 2} not found"

        controller = CommandController(mock_client)

        # Act
        with caplog.at_level(logging.WARNING, "client.reaction.reaction_controller"):
            await controller.reply(mock_message)

        # Assert
        assert expected_log_message in caplog.text
        mock_message.channel.send.assert_not_called()
