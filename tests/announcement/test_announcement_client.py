import logging
from datetime import datetime, timezone
from unittest.mock import call, MagicMock, patch

import discord
import pytest
from freezegun import freeze_time

from announcement.announcement_client import AnnouncementClient
from server import Server


class TestAnnouncementController:
    @pytest.fixture
    def example_server_from_directory_result(
        self, example_server: Server
    ) -> dict[int, Server]:
        other_server = example_server.model_copy()
        other_server.server_id = 123456
        other_server.announcement_channel_id = 1234567890
        other_server.schedule = other_server.schedule[1:]
        other_server.schedule[0] = other_server.schedule[0].model_copy()
        other_server.schedule[0].title = "Some other event"

        return {
            example_server.server_id: example_server,
            other_server.server_id: other_server,
        }

    @pytest.mark.asyncio
    @patch("aiocron.crontab")
    @patch("server.Server.from_directory")
    async def test_on_ready(
        self,
        mock_server_from_directory: MagicMock,
        mock_aiocron_crontab: MagicMock,
        example_server_from_directory_result: dict[int, Server],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        # Arrange
        mock_server_from_directory.return_value = example_server_from_directory_result

        expected_log_message = "Logged in as None"

        announcement_client = AnnouncementClient(intents=discord.Intents())

        # Act
        with caplog.at_level(logging.INFO, "announcement.announcement_client"):
            await announcement_client.on_ready()

        # Assert
        assert announcement_client.servers == example_server_from_directory_result

        assert expected_log_message in caplog.text

        mock_server_from_directory.assert_called_once_with()

        mock_aiocron_crontab.assert_called_once_with(
            "* * * * *", announcement_client.send_announcements
        )

    @pytest.mark.asyncio
    @patch("server.Server.from_directory")
    @patch("discord.Client.get_channel")
    @freeze_time(datetime(2024, 10, 7, 16, 50, tzinfo=timezone.utc))
    async def test_send_announcements(
        self,
        mock_client_get_channel: MagicMock,
        mock_server_from_directory: MagicMock,
        example_server_from_directory_result: dict[int, Server],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        # Arrange
        mock_server_from_directory.return_value = example_server_from_directory_result

        mock_channel = MagicMock(discord.abc.Messageable)
        mock_client_get_channel.return_value = mock_channel

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

        announcement_client = AnnouncementClient(intents=discord.Intents())
        await announcement_client.on_ready()

        # Act
        with caplog.at_level(logging.INFO, "announcement.announcement_client"):
            await announcement_client.send_announcements()

        # Assert
        assert all(message in caplog.text for message in expected_log_messages)

        mock_client_get_channel.assert_called_once_with(54321)
        mock_channel.send.assert_awaited_once_with("@everyone", embed=expected_embed)

    @pytest.mark.asyncio
    @patch("server.Server.from_directory")
    @patch("discord.Client.get_channel")
    @freeze_time(datetime(2024, 10, 8, 16, 50, tzinfo=timezone.utc))
    async def test_send_announcements_multiple_announcements(
        self,
        mock_client_get_channel: MagicMock,
        mock_server_from_directory: MagicMock,
        example_server_from_directory_result: dict[int, Server],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        # Arrange
        mock_server_from_directory.return_value = example_server_from_directory_result

        mock_channel = MagicMock(discord.abc.Messageable)
        mock_client_get_channel.return_value = mock_channel

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

        announcement_client = AnnouncementClient(intents=discord.Intents())
        await announcement_client.on_ready()

        # Act
        with caplog.at_level(logging.INFO, "announcement.announcement_client"):
            await announcement_client.send_announcements()

        # Assert
        assert all(message in caplog.text for message in expected_log_messages)

        assert sorted(mock_client_get_channel.call_args_list) == [
            call(54321),
            call(1234567890),
        ]

        assert mock_channel.send.await_count == 2
        mock_channel.send.assert_has_awaits(
            [
                call("@everyone", embed=expected_first_embed),
                call("@everyone", embed=expected_second_embed),
            ],
            any_order=True,
        )

    @pytest.mark.asyncio
    @patch("server.Server.from_directory")
    @patch("discord.Client.get_channel")
    @freeze_time(datetime(2024, 10, 8, 16, 51, tzinfo=timezone.utc))
    async def test_send_announcements_no_announcements(
        self,
        mock_client_get_channel: MagicMock,
        mock_server_from_directory: MagicMock,
        example_server_from_directory_result: dict[int, Server],
    ) -> None:
        # Arrange
        mock_server_from_directory.return_value = example_server_from_directory_result

        announcement_client = AnnouncementClient(intents=discord.Intents())
        await announcement_client.on_ready()

        # Act
        await announcement_client.send_announcements()

        # Assert
        mock_client_get_channel.assert_not_called()

    @pytest.mark.asyncio
    @patch("server.Server.from_directory")
    @patch("discord.Client.get_channel")
    @freeze_time(datetime(2024, 10, 7, 16, 50, tzinfo=timezone.utc))
    async def test_send_announcements_invalid_channel(
        self,
        mock_client_get_channel: MagicMock,
        mock_server_from_directory: MagicMock,
        caplog: pytest.LogCaptureFixture,
        example_server_from_directory_result: dict[int, Server],
    ) -> None:
        # Arrange
        mock_server_from_directory.return_value = example_server_from_directory_result

        mock_channel = MagicMock()
        mock_client_get_channel.return_value = mock_channel

        expected_log_message = "Announcement count: 1"

        announcement_client = AnnouncementClient(intents=discord.Intents())
        await announcement_client.on_ready()

        # Act
        with (
            pytest.raises(ValueError, match="Cannot send messages to channel ID 54321"),
            caplog.at_level(logging.INFO, "announcement.announcement_client"),
        ):
            await announcement_client.send_announcements()

        # Assert
        assert expected_log_message in caplog.text

        mock_client_get_channel.assert_called_once_with(54321)
        mock_channel.send.assert_not_called()
