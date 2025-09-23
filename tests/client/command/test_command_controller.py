from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import discord
import pytest
from freezegun import freeze_time

from client.command.command_controller import CommandController
from embed_splitter.embed_field import EmbedField
from server import Server


class TestCommandController:
    @pytest.mark.parametrize(
        ("message_content", "expected_result"),
        [
            ("!test", True),
            ("!schedule", True),
            ("!schedule full", True),
            ("Example message", False),
        ],
    )
    def test_is_command(self, message_content: str, expected_result: bool) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.content = message_content

        # Act
        is_command = CommandController.is_command(mock_message)

        # Assert
        assert is_command is expected_result

    @pytest.mark.asyncio
    async def test_reply_test(self, example_server: Server) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.channel.send = AsyncMock()
        mock_message.content = "!test"

        # Act
        await CommandController.reply(mock_message, example_server)

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
        command: str,
        example_full_schedule_embed_fields: list[EmbedField],
        example_server: Server,
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.channel.send = AsyncMock()
        mock_message.content = command

        expected_embed = discord.Embed(
            title="Schedule - QNickel16", colour=CommandController.EMBED_COLOUR
        )
        for field in example_full_schedule_embed_fields:
            expected_embed.add_field(
                name=field.name, value=field.value, inline=field.inline
            )

        # Act
        await CommandController.reply(mock_message, example_server)

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
        example_server: Server,
        command: str,
        example_full_schedule_embed_fields: list[EmbedField],
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.channel.send = AsyncMock()
        mock_message.content = command

        expected_embed = discord.Embed(
            title="Today's schedule - QNickel16", colour=CommandController.EMBED_COLOUR
        )
        for field in example_full_schedule_embed_fields[1:3]:
            expected_embed.add_field(
                name=field.name, value=field.value, inline=field.inline
            )

        # Act
        await CommandController.reply(mock_message, example_server)

        # Assert
        mock_message.channel.send.assert_awaited_once_with(embed=expected_embed)

    @pytest.mark.asyncio
    async def test_reply_unknown_command(self, example_server: Server) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.channel.send = AsyncMock()
        mock_message.content = "!unknown"

        # Act
        await CommandController.reply(mock_message, example_server)

        # Assert
        mock_message.channel.send.assert_not_called()
