from pathlib import Path
from unittest.mock import MagicMock

import pytest

from client import Client
from embed_splitter import EmbedField
from server import Server

SERVERS_PATH = Path.cwd() / "tests" / "assets" / "servers"


@pytest.fixture
def mock_client() -> MagicMock:
    client = MagicMock(spec=Client)
    client.servers = Server.from_directory(SERVERS_PATH)

    return client


@pytest.fixture
def example_server() -> Server:
    server_path = SERVERS_PATH / "server.json"

    return Server.model_validate_json(server_path.read_bytes())


@pytest.fixture
def example_full_schedule_embed_fields() -> list[EmbedField]:
    return [
        EmbedField(
            name="━━━━━━      2024-10-07      ━━━━━━",
            value="10:00 → 20:00 UTC | 12:00 → 22:00 CET",
        ),
        EmbedField(
            name="Registration",
            value="10:00 UTC | 12:00 CET",
        ),
        EmbedField(
            name="Conventional Quantum Algorithms In Qiskit - Part 1: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
            value="- Qiskit introduction\n- Classical gates\n- Phase kickback\n- Deutsch algorithm",
        ),
        EmbedField(
            name="━━━━━━      2024-10-08      ━━━━━━",
            value="17:00 → 20:00 UTC | 19:00 → 22:00 CET",
        ),
        EmbedField(
            name="Conventional Quantum Algorithms In Qiskit - Part 2: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
            value="- Simon's algorithm",
        ),
        EmbedField(
            name="━━━━━━      2024-10-09      ━━━━━━",
            value="17:00 → 20:00 UTC | 19:00 → 22:00 CET",
        ),
        EmbedField(
            name="Conventional Quantum Algorithms In Qiskit - Part 3: 17:00 → 20:00 UTC | 19:00 → 22:00 CET",
            value="- Deutsch-Jozsa algorithm\n- Berenstein-Vazirani algorithm",
        ),
        EmbedField(
            name="━━━━━━      2024-10-10      ━━━━━━",
            value="10:00 UTC | 12:00 CET",
        ),
        EmbedField(
            name="Deadline for submissions",
            value="10:00 UTC | 12:00 CET",
        ),
        EmbedField(
            name="━━━━━━      2024-10-11      ━━━━━━",
            value="10:00 UTC | 12:00 CET",
        ),
        EmbedField(
            name="Announcement of results",
            value="10:00 UTC | 12:00 CET",
        ),
    ]
