from unittest.mock import call, MagicMock

import discord
import pytest

from client.reaction.reaction_controller import ReactionController
from server import Server


class TestReactionController:
    EXAMPLE_CHANNEL_ID = 12321

    @pytest.mark.parametrize(
        ("message_content", "expected_result"),
        [
            ("Task: some task", True),
            ("Example message", False),
            ("How is your task going?", True),
        ],
    )
    def test_is_reactable(
        self, example_server: Server, message_content: str, expected_result: bool
    ) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.channel.id = self.EXAMPLE_CHANNEL_ID
        mock_message.content = message_content

        # Act
        is_reactable = ReactionController.is_reactable(mock_message, example_server)

        # Assert
        assert is_reactable is expected_result

    def test_is_reactable_unknown_channel(self, example_server: Server) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.channel.id = self.EXAMPLE_CHANNEL_ID * 2
        mock_message.content = "Task: some task"

        # Act
        is_reactable = ReactionController.is_reactable(mock_message, example_server)

        # Assert
        assert not is_reactable

    @pytest.mark.asyncio
    async def test_add_reactions(self, example_server: Server) -> None:
        # Arrange
        mock_message = MagicMock(discord.Message)
        mock_message.channel.id = self.EXAMPLE_CHANNEL_ID

        # Act
        await ReactionController.add_reactions(mock_message, example_server)

        # Assert
        assert mock_message.add_reaction.await_args_list == [
            call(item) for item in ["🌕", "🌘", "⏲️"]
        ]
