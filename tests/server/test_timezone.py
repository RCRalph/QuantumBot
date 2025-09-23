from zoneinfo import ZoneInfo

import pytest

from server.timezone import Timezone


class TestTimezone:
    @pytest.fixture
    def timezone_json(self) -> dict[str, str]:
        return {"name": "CET", "text": "CET"}

    @pytest.fixture
    def example_timezone(self) -> Timezone:
        return Timezone(name="CET", text="CET")

    def test_model_validate(
        self, timezone_json: dict[str, str], example_timezone: Timezone
    ) -> None:
        # Act
        timezone = Timezone.model_validate(timezone_json)

        # Assert
        assert timezone == example_timezone

    def test_model_validate_invalid_name(self, timezone_json: dict[str, str]) -> None:
        # Arrange
        timezone_json["name"] = "Some name"

        # Act
        with pytest.raises(ValueError, match="'Some name' isn't a valid timezone"):
            Timezone.model_validate(timezone_json)

    def test_zone_info(self, example_timezone: Timezone) -> None:
        # Arrange
        expected_zone_info = ZoneInfo("CET")

        # Act
        zone_info = example_timezone.zone_info

        # Assert
        assert zone_info is expected_zone_info  # Instances should be cached internally

    def test_eq(self, example_timezone: Timezone) -> None:
        # Arrange
        timezone = example_timezone.model_copy()

        # Assert
        assert timezone == example_timezone

    def test_eq_different_text(self, example_timezone: Timezone) -> None:
        # Arrange
        timezone = Timezone(name=example_timezone.name, text="Some text")

        # Assert
        assert timezone == example_timezone

    def test_eq_different_name(self, example_timezone: Timezone) -> None:
        # Arrange
        timezone = Timezone(name="UTC", text="Some text")

        # Assert
        assert timezone != example_timezone

    def test_eq_different_object(self, example_timezone: Timezone) -> None:
        # Assert
        assert example_timezone != 12345
