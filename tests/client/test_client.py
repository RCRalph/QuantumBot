import logging
from unittest.mock import MagicMock, patch

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
