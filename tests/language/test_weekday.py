from datetime import date
from itertools import cycle

import pytest

from language.weekday import Weekday


class TestWeekday:
    FROM_DATE_PARAMETRIZATION = list(
        zip(
            (date(2025, 12, i + 1) for i in range(7)),
            cycle(
                [
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                ]
            ),
        )
    )

    @pytest.fixture
    def english_weekday(self) -> Weekday:
        return Weekday(
            monday="monday",
            tuesday="tuesday",
            wednesday="wednesday",
            thursday="thursday",
            friday="friday",
            saturday="saturday",
            sunday="sunday",
        )

    def test_to_list(self, english_weekday: Weekday) -> None:
        # Act
        weekday_list = english_weekday.to_list()

        # Assert
        assert weekday_list == [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]

    def test_from_date(self, english_weekday: Weekday) -> None:
        # Arrange
        weekday_value_cycle = cycle(
            [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]
        )

        days_to_check = (date(2025, 12, i + 1) for i in range(31))

        # Act
        for day, weekday in zip(days_to_check, weekday_value_cycle):
            assert english_weekday.from_date(day) == weekday
