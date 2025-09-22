from datetime import datetime, timezone
from typing import Any

from pydantic import Field, field_validator

from server.base_event import BaseEvent
from server.timezone import Timezone


class Deadline(BaseEvent):
    time: datetime = Field(alias="time")
    announcements: list[int] = Field(default_factory=lambda: [600, 240, 120])

    @field_validator("time", mode="before")
    @classmethod
    def convert_time_to_datetime(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, cls.DATETIME_FORMAT).replace(
            tzinfo=timezone.utc
        )

    @property
    def start_time(self) -> datetime:
        return self.time

    @property
    def end_time(self) -> datetime:
        return self.time

    def _get_event_time_text(self, timezone: Timezone) -> str:
        time_text = self.time.astimezone(timezone.zone_info).strftime(self.TIME_FORMAT)

        return f"{time_text} {timezone.text}"
