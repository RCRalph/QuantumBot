from datetime import datetime
from typing import Any

from pydantic import Field, field_validator

from server.event.base_event import BaseEvent


class Deadline(BaseEvent):
    time: datetime = Field(alias="time")
    announcements: list[int] = Field(default_factory=lambda: [600, 240, 120])

    @field_validator("time", mode="before")
    @classmethod
    def convert_time_to_datetime(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, cls.DATETIME_FORMAT)

    @property
    def reminder_time(self) -> datetime:
        return self.time
