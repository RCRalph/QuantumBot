import os
from unittest.mock import MagicMock, patch

from discord import Intents

from client import Client
from main import main

EXAMPLE_TOKEN = "Some token"


@patch("client.Client.__new__")
@patch.dict(os.environ, {"BOT_TOKEN": EXAMPLE_TOKEN}, clear=True)
def test_main(client_new_mock: MagicMock, mock_client: MagicMock) -> None:
    # Arrange
    client_new_mock.return_value = mock_client

    expected_intents = Intents().default()
    expected_intents.message_content = True

    # Act
    main()

    # Assert
    client_new_mock.assert_called_once_with(Client, intents=expected_intents)
    mock_client.run.assert_called_once_with(EXAMPLE_TOKEN)
