import os
from unittest.mock import MagicMock, patch

from discord import Intents

from announcement import AnnouncementClient
from run_announcement import main

EXAMPLE_TOKEN = "Some token"


@patch("announcement.AnnouncementClient.__new__")
@patch.dict(os.environ, {"BOT_TOKEN": EXAMPLE_TOKEN}, clear=True)
def test_main(announcement_client_new_mock: MagicMock, mock_client: MagicMock) -> None:
    # Arrange
    announcement_client_new_mock.return_value = mock_client

    expected_intents = Intents().default()

    # Act
    main()

    # Assert
    announcement_client_new_mock.assert_called_once_with(
        AnnouncementClient, intents=expected_intents
    )
    mock_client.run.assert_called_once_with(EXAMPLE_TOKEN)
