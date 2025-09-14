from datetime import datetime
from typing import Any

import pytest

from server.event.deadline import Deadline


class TestScheduleEvent:
    @pytest.fixture
    def deadline_json(self) -> dict[str, Any]:
        return {
            "title": "Deadline for submissions",
            "description": "Last chance to submit your work to take part in the competition",
            "time": "2024-10-11 10:00",
            "announcements": [10, 60, 120],
        }

    @pytest.fixture
    def example_deadline(self) -> Deadline:
        return Deadline(
            title="Deadline for submissions",
            description="Last chance to submit your work to take part in the competition",
            time=datetime(2024, 10, 11, 10, 0),
            announcements=[10, 60, 120],
        )

    def test_model_validate(
        self, example_deadline: Deadline, deadline_json: dict[str, Any]
    ) -> None:
        # Act
        schedule_event = Deadline.model_validate(deadline_json)

        # Assert
        assert schedule_event == example_deadline

    def test_reminder_time(self, example_deadline: Deadline) -> None:
        # Act
        reminder_time = example_deadline.reminder_time

        # Assert
        assert reminder_time == example_deadline.time
