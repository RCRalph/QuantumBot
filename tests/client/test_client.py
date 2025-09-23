import logging
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from discord import Intents

from client.announcement import AnnouncementController
from client.client import Client
from server import Server


class TestClient:
    @pytest.fixture
    def example_client(self) -> Client:
        return Client(intents=Intents())

    @pytest.fixture
    def example_announcement_controller(
        self, example_client: Client
    ) -> AnnouncementController:
        return AnnouncementController(example_client)

    @pytest.mark.asyncio
    @patch("aiocron.crontab")
    @patch("server.Server.from_directory")
    @patch("client.announcement.AnnouncementController.__new__")
    async def test_on_ready(
        self,
        mock_announcement_controller: MagicMock,
        mock_server_from_directory: MagicMock,
        mock_aiocron_crontab: MagicMock,
        example_client: Client,
        example_announcement_controller: AnnouncementController,
        example_server: Server,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        # Arrange
        mock_announcement_controller.return_value = example_announcement_controller
        mock_server_from_directory.return_value = {
            example_server.server_id: example_server
        }

        expected_log_message = "Logged in as None"

        # Act
        with caplog.at_level(logging.INFO, "client.client"):
            await example_client.on_ready()

        # Assert
        assert example_client.servers == {example_server.server_id: example_server}

        assert expected_log_message in caplog.text

        mock_announcement_controller.assert_called_once_with(
            AnnouncementController, example_client
        )

        mock_server_from_directory.assert_called_once_with()

        mock_aiocron_crontab.assert_called_once_with(
            "* * * * *", example_announcement_controller.send_announcements
        )

    @pytest.mark.asyncio
    @patch("client.command.CommandController.is_command")
    @patch("client.command.CommandController.reply")
    @patch("client.reaction.ReactionController.is_reactable")
    @patch("client.reaction.ReactionController.add_reactions")
    async def test_on_message(
        self,
        reaction_controller_reply: AsyncMock,
        reaction_controller_is_reactable: MagicMock,
        command_controller_reply: AsyncMock,
        command_controller_is_command: MagicMock,
        example_client: Client,
        example_server: Server,
    ) -> None:
        # Arrange
        example_client.servers = {example_server.server_id: example_server}

        command_controller_is_command.return_value = False
        reaction_controller_is_reactable.return_value = False

        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = example_server.server_id

        # Act
        await example_client.on_message(mock_message)

        # Assert
        command_controller_is_command.assert_called_once_with(mock_message)
        command_controller_reply.assert_not_called()
        reaction_controller_is_reactable.assert_called_once_with(
            mock_message, example_server
        )
        reaction_controller_reply.assert_not_called()

    @pytest.mark.asyncio
    @patch("client.command.CommandController.is_command")
    @patch("client.command.CommandController.reply")
    @patch("client.reaction.ReactionController.is_reactable")
    @patch("client.reaction.ReactionController.add_reactions")
    async def test_on_message_command(
        self,
        reaction_controller_reply: AsyncMock,
        reaction_controller_is_reactable: MagicMock,
        command_controller_reply: AsyncMock,
        command_controller_is_command: MagicMock,
        example_client: Client,
        example_server: Server,
    ) -> None:
        # Arrange
        example_client.servers = {example_server.server_id: example_server}

        command_controller_is_command.return_value = True
        reaction_controller_is_reactable.return_value = False

        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = example_server.server_id

        # Act
        await example_client.on_message(mock_message)

        # Assert
        command_controller_is_command.assert_called_once_with(mock_message)
        command_controller_reply.assert_awaited_once_with(mock_message, example_server)
        reaction_controller_is_reactable.assert_not_called()
        reaction_controller_reply.assert_not_called()

    @pytest.mark.asyncio
    @patch("client.command.CommandController.is_command")
    @patch("client.command.CommandController.reply")
    @patch("client.reaction.ReactionController.is_reactable")
    @patch("client.reaction.ReactionController.add_reactions")
    async def test_on_message_reaction(
        self,
        reaction_controller_reply: AsyncMock,
        reaction_controller_is_reactable: MagicMock,
        command_controller_reply: AsyncMock,
        command_controller_is_command: MagicMock,
        example_client: Client,
        example_server: Server,
    ) -> None:
        # Arrange
        example_client.servers = {example_server.server_id: example_server}

        command_controller_is_command.return_value = False
        reaction_controller_is_reactable.return_value = True

        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = example_server.server_id

        # Act
        await example_client.on_message(mock_message)

        # Assert
        command_controller_is_command.assert_called_once_with(mock_message)
        command_controller_reply.assert_not_called()
        reaction_controller_is_reactable.assert_called_once_with(
            mock_message, example_server
        )
        reaction_controller_reply.assert_awaited_once_with(mock_message, example_server)

    @pytest.mark.asyncio
    @patch("client.command.CommandController.is_command")
    @patch("client.command.CommandController.reply")
    @patch("client.reaction.ReactionController.is_reactable")
    @patch("client.reaction.ReactionController.add_reactions")
    async def test_on_message_own_message(
        self,
        reaction_controller_reply: AsyncMock,
        reaction_controller_is_reactable: MagicMock,
        command_controller_reply: AsyncMock,
        command_controller_is_command: MagicMock,
        example_client: Client,
        example_server: Server,
    ) -> None:
        # Arrange
        example_client.servers = {example_server.server_id: example_server}

        command_controller_is_command.return_value = False
        reaction_controller_is_reactable.return_value = True

        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = example_server.server_id
        mock_message.author = example_client.user

        # Act
        await example_client.on_message(mock_message)

        # Assert
        command_controller_is_command.assert_not_called()
        command_controller_reply.assert_not_called()
        reaction_controller_is_reactable.assert_not_called()
        reaction_controller_reply.assert_not_called()

    @pytest.mark.asyncio
    @patch("client.command.CommandController.is_command")
    @patch("client.command.CommandController.reply")
    @patch("client.reaction.ReactionController.is_reactable")
    @patch("client.reaction.ReactionController.add_reactions")
    async def test_on_message_guild_is_none(
        self,
        reaction_controller_reply: AsyncMock,
        reaction_controller_is_reactable: MagicMock,
        command_controller_reply: AsyncMock,
        command_controller_is_command: MagicMock,
        example_client: Client,
        example_server: Server,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        # Arrange
        example_client.servers = {example_server.server_id: example_server}

        command_controller_is_command.return_value = False
        reaction_controller_is_reactable.return_value = True

        mock_message = MagicMock(discord.Message)
        mock_message.guild = None

        expected_log_message = "Message guild not found"

        # Act
        with caplog.at_level(logging.WARNING, "client.client"):
            await example_client.on_message(mock_message)

        # Assert
        assert expected_log_message in caplog.text

        command_controller_is_command.assert_not_called()
        command_controller_reply.assert_not_called()
        reaction_controller_is_reactable.assert_not_called()
        reaction_controller_reply.assert_not_called()

    @pytest.mark.asyncio
    @patch("client.command.CommandController.is_command")
    @patch("client.command.CommandController.reply")
    @patch("client.reaction.ReactionController.is_reactable")
    @patch("client.reaction.ReactionController.add_reactions")
    async def test_on_message_server_not_found(
        self,
        reaction_controller_reply: AsyncMock,
        reaction_controller_is_reactable: MagicMock,
        command_controller_reply: AsyncMock,
        command_controller_is_command: MagicMock,
        example_client: Client,
        example_server: Server,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        # Arrange
        example_client.servers = {}

        command_controller_is_command.return_value = False
        reaction_controller_is_reactable.return_value = True

        mock_message = MagicMock(discord.Message)
        mock_message.guild.id = example_server.server_id

        expected_log_message = f"Server {example_server.server_id} not found"

        # Act
        with caplog.at_level(logging.WARNING, "client.client"):
            await example_client.on_message(mock_message)

        # Assert
        assert expected_log_message in caplog.text

        command_controller_is_command.assert_not_called()
        command_controller_reply.assert_not_called()
        reaction_controller_is_reactable.assert_not_called()
        reaction_controller_reply.assert_not_called()
