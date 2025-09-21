import json
import logging
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, cast, Generator

import pytest

from language import Language
from server.base_event import BaseEvent
from server.deadline import Deadline
from server.reaction import Reaction
from server.schedule_event import ScheduleEvent
from server.server import Server
from server.timezone import Timezone


class TestServer:
    @pytest.fixture
    def server_configuration_json(self) -> dict[str, Any]:
        server_path = Path.cwd() / "tests" / "assets" / "servers" / "server.json"

        return cast(dict[str, Any], json.loads(server_path.read_bytes()))

    @pytest.fixture
    def example_server(self) -> Server:
        return Server(
            name="QNickel16",
            server_id=12345,
            announcement_channel_id=54321,
            reactions={12321: Reaction(prompt_text="Task", emojis=["🌕", "🌘", "⏲️"])},
            language=Language.EN,
            timezones=[
                Timezone(name="UTC", text="UTC"),
                Timezone(name="CET", text="CET"),
            ],
            schedule=[
                ScheduleEvent(
                    title="Conventional Quantum Algorithms In Qiskit - Part 1",
                    description="- Qiskit introduction\n- Classical gates\n- Phase kickback\n- Deutsch algorithm",
                    start=datetime(2024, 10, 7, 17, 0, tzinfo=timezone.utc),
                    end=datetime(2024, 10, 7, 20, 0, tzinfo=timezone.utc),
                ),
                ScheduleEvent(
                    title="Conventional Quantum Algorithms In Qiskit - Part 2",
                    description="- Simon's algorithm",
                    start=datetime(2024, 10, 8, 17, 0, tzinfo=timezone.utc),
                    end=datetime(2024, 10, 8, 20, 0, tzinfo=timezone.utc),
                ),
                ScheduleEvent(
                    title="Conventional Quantum Algorithms In Qiskit - Part 3",
                    description="- Deutsch-Jozsa algorithm\n- Berenstein-Vazirani algorithm",
                    start=datetime(2024, 10, 9, 17, 0, tzinfo=timezone.utc),
                    end=datetime(2024, 10, 9, 20, 0, tzinfo=timezone.utc),
                    announcements=[123],
                ),
            ],
            deadlines=[
                Deadline(
                    title="Registration",
                    time=datetime(2024, 10, 7, 10, 0, tzinfo=timezone.utc),
                ),
                Deadline(
                    title="Deadline for submissions",
                    time=datetime(2024, 10, 10, 10, 0, tzinfo=timezone.utc),
                ),
                Deadline(
                    title="Announcement of results",
                    time=datetime(2024, 10, 11, 10, 0, tzinfo=timezone.utc),
                    announcements=[10],
                ),
            ],
        )

    @pytest.fixture
    def directory_with_configs(
        self, server_configuration_json: dict[str, Any]
    ) -> Generator[Path, None, None]:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir_path = Path(tmp_dir)

            for i in range(3):
                server_configuration_json["name"] = f"Server {i}"
                server_configuration_json["server_id"] = i

                with open(tmp_dir_path / f"server_{i}.json", "w+") as file:
                    json.dump(server_configuration_json, file)

            yield tmp_dir_path

    def test_model_validate(
        self, server_configuration_json: dict[str, Any], example_server: Server
    ) -> None:
        # Act
        server = Server.model_validate(server_configuration_json)

        # Assert
        assert server == example_server

    def test_model_validate_unsupported_timezones_type(
        self, server_configuration_json: dict[str, Any]
    ) -> None:
        # Arrange
        server_configuration_json["timezones"] = "UTC"

        # Act
        with pytest.raises(
            TypeError, match="Timezones should be a list, instead got: <class 'str'"
        ):
            Server.model_validate(server_configuration_json)

    def test_model_validate_duplicate_timezones(
        self, server_configuration_json: dict[str, Any]
    ) -> None:
        # Arrange
        server_configuration_json["timezones"][1] = "UTC"

        # Act
        with pytest.raises(ValueError, match="Timezones must be distinct"):
            Server.model_validate(server_configuration_json)

    def test_model_validate_timezone_as_dict(
        self, server_configuration_json: dict[str, Any], example_server: Server
    ) -> None:
        # Arrange
        server_configuration_json["timezones"][1] = {
            "name": "CET",
            "text": "Warsaw, Poland",
        }

        example_server.timezones[1] = Timezone(name="CET", text="Warsaw, Poland")

        # Act
        server = Server.model_validate(server_configuration_json)

        # Assert
        assert server == example_server

    def test_model_validate_unsupported_timezone_type(
        self, server_configuration_json: dict[str, Any]
    ) -> None:
        # Arrange
        server_configuration_json["timezones"][1] = 12345

        # Act
        with pytest.raises(TypeError, match="Unsupported timezone type: <class 'int'>"):
            Server.model_validate(server_configuration_json)

    def test_events(self, example_server: Server) -> None:
        # Arrange
        expected_event_order: list[BaseEvent] = [
            example_server.deadlines[0],
            example_server.schedule[0],
            example_server.schedule[1],
            example_server.schedule[2],
            example_server.deadlines[1],
            example_server.deadlines[2],
        ]

        # Act
        events = example_server.events

        # Assert
        assert events == expected_event_order
        assert sorted(events, key=lambda x: x.reminder_time) == events

    def test_events_by_date(self, example_server: Server) -> None:
        # Arrange
        expected_events_by_date: dict[date, list[BaseEvent]] = {
            date(2024, 10, 7): [
                example_server.deadlines[0],
                example_server.schedule[0],
            ],
            date(2024, 10, 8): [example_server.schedule[1]],
            date(2024, 10, 9): [example_server.schedule[2]],
            date(2024, 10, 10): [example_server.deadlines[1]],
            date(2024, 10, 11): [example_server.deadlines[2]],
        }

        # Act
        events_by_date = example_server.events_by_date

        # Assert
        assert events_by_date == expected_events_by_date
        assert sorted(events_by_date.keys()) == list(events_by_date.keys())

    def test_from_directory(
        self,
        example_server: Server,
        directory_with_configs: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        # Arrange
        expected_servers = {
            0: example_server.model_copy(),
            1: example_server.model_copy(),
            2: example_server.model_copy(),
        }

        for i in range(3):
            expected_servers[i].server_id = i
            expected_servers[i].name = f"Server {i}"

        # Act
        with caplog.at_level(logging.INFO, "server.server"):
            servers = Server.from_directory(directory_with_configs)

        # Assert
        assert servers == expected_servers
        assert "Successfully loaded 3 servers" in caplog.text

    def test_from_directory_error_loading_data(
        self,
        server_configuration_json: dict[str, Any],
        directory_with_configs: Path,
    ) -> None:
        # Arrange
        server_configuration_json["name"] = 1234

        server_configuration_path = directory_with_configs / "server_0.json"
        server_configuration_path.write_text(json.dumps(server_configuration_json))

        expected_error_message = "Input should be a valid string [type=string_type, input_value=1234, input_type=int]"

        # Act
        with pytest.raises(
            ExceptionGroup, match="Error loading server data"
        ) as exc_info:
            Server.from_directory(directory_with_configs)

        # Assert
        assert len(exc_info.value.exceptions) == 1
        assert expected_error_message in str(exc_info.value.exceptions[0])
