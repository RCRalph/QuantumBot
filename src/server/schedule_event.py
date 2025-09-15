from datetime import datetime, timezone
from typing import Any, Self

from pydantic import Field, field_validator, model_validator

from server.base_event import BaseEvent
from server.timezone import Timezone


class ScheduleEvent(BaseEvent):
    start: datetime
    end: datetime
    announcements: list[int] = Field(default_factory=lambda: [10])

    @field_validator("start", mode="before")
    @classmethod
    def convert_start_to_datetime(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, cls.DATETIME_FORMAT).replace(
            tzinfo=timezone.utc
        )

    @field_validator("end", mode="before")
    @classmethod
    def convert_end_to_datetime(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, cls.DATETIME_FORMAT).replace(
            tzinfo=timezone.utc
        )

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

    def _get_event_time_text(self, timezone: Timezone) -> str:
        start_datetime = self.start.astimezone(timezone.zone_info)
        end_datetime = self.end.astimezone(timezone.zone_info)

        if start_datetime.date() == end_datetime.date():
            start_time_text = start_datetime.strftime(self.TIME_FORMAT)
            end_time_text = end_datetime.strftime(self.TIME_FORMAT)
        else:
            start_time_text = start_datetime.strftime(self.DATETIME_FORMAT)
            end_time_text = end_datetime.strftime(self.DATETIME_FORMAT)

        return f"{start_time_text} → {end_time_text} {timezone.text}"
