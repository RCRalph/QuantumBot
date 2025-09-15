from datetime import datetime, timezone
from typing import Any

import pytest

from server.schedule_event import ScheduleEvent
from server.timezone import Timezone


class TestScheduleEvent:
    EXAMPLE_TIMEZONES = [
        Timezone(name="UTC", text="UTC"),
        Timezone(name="CET", text="Warsaw, Poland"),
        Timezone(name="Asia/Dubai", text="GST"),
    ]

    @pytest.fixture
    def schedule_event_json(self) -> dict[str, Any]:
        return {
            "title": "Conventional Quantum Algorithms In Qiskit - Part 3",
            "description": "- Deutsch-Jozsa algorithm\n- Berenstein-Vazirani algorithm",
            "start": "2024-10-09 17:00",
            "end": "2024-10-09 20:00",
            "announcements": [123],
        }

    @pytest.fixture
    def example_schedule_event(self) -> ScheduleEvent:
        return ScheduleEvent(
            title="Conventional Quantum Algorithms In Qiskit - Part 3",
            description="- Deutsch-Jozsa algorithm\n- Berenstein-Vazirani algorithm",
            start=datetime(2024, 10, 9, 17, 0, tzinfo=timezone.utc),
            end=datetime(2024, 10, 9, 20, 0, tzinfo=timezone.utc),
            announcements=[123],
        )

    def test_model_validate(
        self, example_schedule_event: ScheduleEvent, schedule_event_json: dict[str, Any]
    ) -> None:
        # Act
        schedule_event = ScheduleEvent.model_validate(schedule_event_json)

        # Assert
        assert schedule_event == example_schedule_event

    def test_model_validate_start_after_end(
        self, schedule_event_json: dict[str, Any]
    ) -> None:
        # Arrange
        schedule_event_json["start"], schedule_event_json["end"] = (
            schedule_event_json["end"],
            schedule_event_json["start"],
        )

        expected_error_message = (
            "Start of event Conventional Quantum Algorithms "
            "In Qiskit - Part 3 cannot happen after the event has ended"
        )

        # Act
        with pytest.raises(ValueError, match=expected_error_message):
            ScheduleEvent.model_validate(schedule_event_json)

    def test_reminder_time(self, example_schedule_event: ScheduleEvent) -> None:
        # Act
        reminder_time = example_schedule_event.reminder_time

        # Assert
        assert reminder_time == example_schedule_event.start

    @pytest.mark.parametrize(
        ("timezones", "expected_title"),
        [
            pytest.param(
                [EXAMPLE_TIMEZONES[0]],
                "Conventional Quantum Algorithms In Qiskit - Part 3: 17:00 → 20:00 UTC",
                id="UTC",
            ),
            pytest.param(
                [EXAMPLE_TIMEZONES[1]],
                "Conventional Quantum Algorithms In Qiskit - Part 3: 19:00 → 22:00 Warsaw, Poland",
                id="CET",
            ),
            pytest.param(
                [EXAMPLE_TIMEZONES[2]],
                "Conventional Quantum Algorithms In Qiskit - Part 3: 2024-10-09 21:00 → 2024-10-10 00:00 GST",
                id="GST",
            ),
            pytest.param(
                EXAMPLE_TIMEZONES,
                "Conventional Quantum Algorithms In Qiskit - Part 3: 17:00 → 20:00 UTC | 19:00 → 22:00 Warsaw, Poland | 2024-10-09 21:00 → 2024-10-10 00:00 GST",
                id="UTC+CET+GST",
            ),
        ],
    )
    def test_get_embed_name(
        self,
        example_schedule_event: ScheduleEvent,
        timezones: list[Timezone],
        expected_title: str,
    ) -> None:
        # Act
        embed_title = example_schedule_event.get_embed_name(timezones)

        # Assert
        assert embed_title == expected_title

    def test_get_embed_name_empty_description(
        self, example_schedule_event: ScheduleEvent
    ) -> None:
        # Arrange
        example_schedule_event.description = None

        # Act
        embed_title = example_schedule_event.get_embed_name(self.EXAMPLE_TIMEZONES)

        # Assert
        assert embed_title == example_schedule_event.title

    def test_get_embed_value(self, example_schedule_event: ScheduleEvent) -> None:
        # Act
        embed_value = example_schedule_event.get_embed_value(self.EXAMPLE_TIMEZONES)

        # Assert
        assert embed_value == example_schedule_event.description

    @pytest.mark.parametrize(
        ("timezones", "expected_value"),
        [
            pytest.param(
                [EXAMPLE_TIMEZONES[0]],
                "17:00 → 20:00 UTC",
                id="UTC",
            ),
            pytest.param(
                [EXAMPLE_TIMEZONES[1]],
                "19:00 → 22:00 Warsaw, Poland",
                id="CET",
            ),
            pytest.param(
                [EXAMPLE_TIMEZONES[2]],
                "2024-10-09 21:00 → 2024-10-10 00:00 GST",
                id="GST",
            ),
            pytest.param(
                EXAMPLE_TIMEZONES,
                "17:00 → 20:00 UTC | 19:00 → 22:00 Warsaw, Poland | 2024-10-09 21:00 → 2024-10-10 00:00 GST",
                id="UTC+CET",
            ),
        ],
    )
    def test_get_embed_value_empty_description(
        self,
        example_schedule_event: ScheduleEvent,
        timezones: list[Timezone],
        expected_value: str,
    ) -> None:
        # Arrange
        example_schedule_event.description = None

        # Act
        embed_value = example_schedule_event.get_embed_value(timezones)

        # Assert
        assert embed_value == expected_value
