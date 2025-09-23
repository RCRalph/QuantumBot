import logging
from datetime import datetime, timezone
from unittest.mock import call, MagicMock

import discord
import pytest
from freezegun import freeze_time

from client.announcement.announcement_controller import AnnouncementController
from client.client import Client
from server import Server


class TestAnnouncementController:
    @pytest.fixture
    def mock_announcement_client(
        self, mock_client: MagicMock, example_server: Server
    ) -> Client:
        other_server = example_server.model_copy()
        other_server.announcement_channel_id = 1234567890
        other_server.schedule = other_server.schedule[1:]
        other_server.schedule[0].title = "Some other event"

        mock_client.servers[1234567890] = other_server

        return mock_client

    @pytest.mark.asyncio
    @freeze_time(datetime(2024, 10, 7, 16, 50, tzinfo=timezone.utc))
    async def test_send_announcements(
        self, mock_announcement_client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Arrange
        mock_channel = MagicMock(discord.abc.Messageable)
        mock_announcement_client.get_channel.return_value = mock_channel  # type: ignore

        expected_embed = discord.Embed(title="Reminder!", colour=0x2F3855)
        expected_embed.add_field(
            name="Conventional Quantum Algorithms In Qiskit - Part 1: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
            value="- Qiskit introduction\n- Classical gates\n- Phase kickback\n- Deutsch algorithm",
            inline=False,
        )

        expected_log_messages = [
            "Announcement count: 1",
            "Sent announcement: Conventional Quantum Algorithms In Qiskit - Part 1: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
        ]

        controller = AnnouncementController(mock_announcement_client)

        # Act
        with caplog.at_level(
            logging.INFO, "client.announcement.announcement_controller"
        ):
            await controller.send_announcements()

        # Assert
        assert all(message in caplog.text for message in expected_log_messages)

        mock_announcement_client.get_channel.assert_called_once_with(54321)  # type: ignore
        mock_channel.send.assert_awaited_once_with("@everyone", embed=expected_embed)

    @pytest.mark.asyncio
    @freeze_time(datetime(2024, 10, 8, 16, 50, tzinfo=timezone.utc))
    async def test_send_announcements_multiple_announcements(
        self, mock_announcement_client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Arrange
        mock_channel = MagicMock(discord.abc.Messageable)
        mock_announcement_client.get_channel.return_value = mock_channel  # type: ignore

        expected_first_embed = discord.Embed(title="Reminder!", colour=0x2F3855)
        expected_first_embed.add_field(
            name="Conventional Quantum Algorithms In Qiskit - Part 2: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
            value="- Simon's algorithm",
            inline=False,
        )

        expected_second_embed = discord.Embed(title="Reminder!", colour=0x2F3855)
        expected_second_embed.add_field(
            name="Some other event: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
            value="- Simon's algorithm",
            inline=False,
        )

        expected_log_messages = [
            "Announcement count: 2",
            "Sent announcement: Some other event: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
            "Sent announcement: Conventional Quantum Algorithms In Qiskit - Part 2: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
        ]

        controller = AnnouncementController(mock_announcement_client)

        # Act
        with caplog.at_level(
            logging.INFO, "client.announcement.announcement_controller"
        ):
            await controller.send_announcements()

        # Assert
        assert all(message in caplog.text for message in expected_log_messages)

        assert mock_announcement_client.get_channel.call_count == 2  # type: ignore
        mock_announcement_client.get_channel.assert_has_calls(  # type: ignore
            [call(54321), call(1234567890)], any_order=True
        )

        assert mock_channel.send.await_count == 2
        mock_channel.send.assert_has_awaits(
            [
                call("@everyone", embed=expected_first_embed),
                call("@everyone", embed=expected_second_embed),
            ],
            any_order=True,
        )

    @pytest.mark.asyncio
    @freeze_time(datetime(2024, 10, 8, 16, 51, tzinfo=timezone.utc))
    async def test_send_announcements_no_announcements(
        self, mock_announcement_client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Arrange
        controller = AnnouncementController(mock_announcement_client)

        # Act
        await controller.send_announcements()

        # Assert
        mock_announcement_client.get_channel.assert_not_called()  # type: ignore

    @pytest.mark.asyncio
    @freeze_time(datetime(2024, 10, 7, 16, 50, tzinfo=timezone.utc))
    async def test_send_announcements_invalid_channel(
        self, mock_announcement_client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        # Arrange
        mock_channel = MagicMock()
        mock_announcement_client.get_channel.return_value = mock_channel  # type: ignore

        expected_log_message = "Announcement count: 1"

        controller = AnnouncementController(mock_announcement_client)

        # Act
        with (
            pytest.raises(ValueError, match="Cannot send messages to channel ID 54321"),
            caplog.at_level(
                logging.INFO, "client.announcement.announcement_controller"
            ),
        ):
            await controller.send_announcements()

        # Assert
        assert expected_log_message in caplog.text

        mock_announcement_client.get_channel.assert_called_once_with(54321)  # type: ignore
        mock_channel.send.assert_not_called()
