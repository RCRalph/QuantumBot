import logging
from unittest.mock import call, MagicMock

import discord
import pytest

from client.client import Client
from client.reaction.reaction_controller import ReactionController


class TestReactionController:
    EXAMPLE_SERVER_ID = 12345
    EXAMPLE_CHANNEL_ID = 12321

    @pytest.mark.asyncio
    async def test_add_reactions(self, mock_client: Client) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_SERVER_ID
        mock_message.channel.id = self.EXAMPLE_CHANNEL_ID

        mock_message.content = "Task: Some task"

        controller = ReactionController(mock_client)

        # Act
        await controller.add_reactions(mock_message)

        # Assert
        assert mock_message.add_reaction.call_count == 3
        mock_message.add_reaction.assert_has_awaits(
            [call(item) for item in ["🌕", "🌘", "⏲️"]]
        )

    @pytest.mark.asyncio
    async def test_add_reactions_message_guild_not_found(
        self, mock_client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild = None

        expected_log_message = "Message guild not found"

        controller = ReactionController(mock_client)

        # Act
        with caplog.at_level(logging.WARNING, "client.reaction.reaction_controller"):
            await controller.add_reactions(mock_message)

        # Assert
        assert expected_log_message in caplog.text
        mock_message.add_reaction.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_reactions_server_not_found(
        self, mock_client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_CHANNEL_ID

        expected_log_message = f"Server {self.EXAMPLE_CHANNEL_ID} not found"

        controller = ReactionController(mock_client)

        # Act
        with caplog.at_level(logging.WARNING, "client.reaction.reaction_controller"):
            await controller.add_reactions(mock_message)

        # Assert
        assert expected_log_message in caplog.text
        mock_message.add_reaction.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_reactions_message_to_other_channel(
        self, mock_client: Client
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_SERVER_ID
        mock_message.channel.id = self.EXAMPLE_SERVER_ID

        controller = ReactionController(mock_client)

        # Act
        await controller.add_reactions(mock_message)

        # Assert
        mock_message.add_reaction.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_reactions_message_with_other_content(
        self, mock_client: Client
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = self.EXAMPLE_SERVER_ID
        mock_message.channel.id = self.EXAMPLE_CHANNEL_ID
        mock_message.content = "Some other message"

        controller = ReactionController(mock_client)

        # Act
        await controller.add_reactions(mock_message)

        # Assert
        mock_message.add_reaction.assert_not_called()
