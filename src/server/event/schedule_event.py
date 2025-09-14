from datetime import datetime
from typing import Any, Self

from pydantic import Field, field_validator, model_validator

from server.event.base_event import BaseEvent


class ScheduleEvent(BaseEvent):
    start: datetime
    end: datetime
    announcements: list[int] = Field(default_factory=lambda: [10])

    @field_validator("start", mode="before")
    @classmethod
    def convert_start_to_datetime(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, cls.DATETIME_FORMAT)

    @field_validator("end", mode="before")
    @classmethod
    def convert_end_to_datetime(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, cls.DATETIME_FORMAT)

    @model_validator(mode="after")
    def ensure_start_and_end_is_valid(self) -> Self:
        if self.start > self.end:
            raise ValueError(
                f"Start of event {self.title} cannot happen after the event has ended"
            )

        return self

    @property
    def reminder_time(self) -> datetime:
        return self.start
