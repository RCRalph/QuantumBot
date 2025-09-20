import pytest

from client.announcement.announcement import Announcement
from server import Server


class TestAnnouncement:
    @pytest.fixture
    def example_announcement(self, example_server: Server) -> Announcement:
        return Announcement(example_server, example_server.events[0])

    def test_embed(self, example_announcement: Announcement) -> None:
        # Arrange
        expected_embed_content = {
            "color": Announcement.EMBED_COLOR,
            "fields": [
                {
                    "inline": False,
                    "name": "Registration",
                    "value": "10:00 UTC | 12:00 CET",
                }
            ],
            "flags": 0,
            "title": "Reminder!",
            "type": "rich",
        }

        # Act
        embed = example_announcement.embed

        # Assert
        assert embed.to_dict() == expected_embed_content

    def test_comparison_key(self, example_announcement: Announcement) -> None:
        # Arrange
        expected_comparison_key = (54321, "Registration")

        # Act
        comparison_key = example_announcement.comparison_key

        # Assert
        assert comparison_key == expected_comparison_key

    def test_eq(
        self, example_announcement: Announcement, example_server: Server
    ) -> None:
        # Arrange
        other_value = Announcement(example_server, example_server.events[0])

        # Assert
        assert example_announcement == other_value

    def test_eq_other_announcement(
        self, example_announcement: Announcement, example_server: Server
    ) -> None:
        # Arrange
        other_value = Announcement(example_server, example_server.events[1])

        # Assert
        assert example_announcement != other_value

    def test_eq_other_instance(self, example_announcement: Announcement) -> None:
        # Arrange
        other_value = 12345

        # Assert
        assert example_announcement != other_value

    def test_hash(self, example_announcement: Announcement) -> None:
        # Arrange
        expected_hash = hash(example_announcement.comparison_key)

        # Act
        hash_value = hash(example_announcement)

        # Assert
        assert hash_value == expected_hash
