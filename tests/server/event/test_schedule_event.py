from datetime import datetime
from typing import Any

import pytest

from server.event.schedule_event import ScheduleEvent


class TestScheduleEvent:
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
            start=datetime(2024, 10, 9, 17, 0),
            end=datetime(2024, 10, 9, 20, 0),
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
