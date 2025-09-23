from datetime import datetime, timezone
from typing import Any

import pytest

from server.deadline import Deadline
from server.timezone import Timezone


class TestScheduleEvent:
    EXAMPLE_TIMEZONES = [
        Timezone(name="UTC", text="UTC"),
        Timezone(name="CET", text="Warsaw, Poland"),
    ]

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
            time=datetime(2024, 10, 11, 10, 0, tzinfo=timezone.utc),
            announcements=[10, 60, 120],
        )

    def test_model_validate(
        self, example_deadline: Deadline, deadline_json: dict[str, Any]
    ) -> None:
        # Act
        schedule_event = Deadline.model_validate(deadline_json)

        # Assert
        assert schedule_event == example_deadline

    def test_start_time(self, example_deadline: Deadline) -> None:
        # Act
        start_time = example_deadline.start_time

        # Assert
        assert start_time == example_deadline.time

    def test_end_time(self, example_deadline: Deadline) -> None:
        # Act
        end_time = example_deadline.end_time

        # Assert
        assert end_time == example_deadline.time

    @pytest.mark.parametrize(
        ("timezones", "expected_title"),
        [
            pytest.param(
                [EXAMPLE_TIMEZONES[0]],
                "Deadline for submissions: 10:00 UTC",
                id="UTC",
            ),
            pytest.param(
                [EXAMPLE_TIMEZONES[1]],
                "Deadline for submissions: 12:00 Warsaw, Poland",
                id="CET",
            ),
            pytest.param(
                EXAMPLE_TIMEZONES,
                "Deadline for submissions: 10:00 UTC | 12:00 Warsaw, Poland",
                id="UTC+CET",
            ),
        ],
    )
    def test_get_embed_name(
        self,
        example_deadline: Deadline,
        timezones: list[Timezone],
        expected_title: str,
    ) -> None:
        # Act
        embed_title = example_deadline.get_embed_name(timezones)

        # Assert
        assert embed_title == expected_title

    def test_get_embed_name_empty_description(self, example_deadline: Deadline) -> None:
        # Arrange
        example_deadline.description = None

        # Act
        embed_title = example_deadline.get_embed_name(self.EXAMPLE_TIMEZONES)

        # Assert
        assert embed_title == example_deadline.title

    def test_get_embed_value(self, example_deadline: Deadline) -> None:
        # Act
        embed_value = example_deadline.get_embed_value(self.EXAMPLE_TIMEZONES)

        # Assert
        assert embed_value == example_deadline.description

    @pytest.mark.parametrize(
        ("timezones", "expected_value"),
        [
            pytest.param(
                [EXAMPLE_TIMEZONES[0]],
                "10:00 UTC",
                id="UTC",
            ),
            pytest.param(
                [EXAMPLE_TIMEZONES[1]],
                "12:00 Warsaw, Poland",
                id="CET",
            ),
            pytest.param(
                EXAMPLE_TIMEZONES,
                "10:00 UTC | 12:00 Warsaw, Poland",
                id="UTC+CET",
            ),
        ],
    )
    def test_get_embed_value_empty_description(
        self, example_deadline: Deadline, timezones: list[Timezone], expected_value: str
    ) -> None:
        # Arrange
        example_deadline.description = None

        # Act
        embed_value = example_deadline.get_embed_value(timezones)

        # Assert
        assert embed_value == expected_value
