from pathlib import Path
from unittest.mock import MagicMock

import pytest

from client import Client
from server import Server

SERVERS_PATH = Path.cwd() / "tests" / "assets" / "servers"


@pytest.fixture
def mock_client() -> Client:
    client = MagicMock(spec=Client)
    client.servers = Server.from_directory(SERVERS_PATH)

    return client


@pytest.fixture
def example_server() -> Server:
    server_path = SERVERS_PATH / "server.json"

    return Server.model_validate_json(server_path.read_bytes())
