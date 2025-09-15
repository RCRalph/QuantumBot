from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar, Iterable, LiteralString

from pydantic import BaseModel, Field

from server.timezone import Timezone


class BaseEvent(BaseModel, ABC):
    TIME_FORMAT: ClassVar[LiteralString] = "%H:%M"
    DATETIME_FORMAT: ClassVar[LiteralString] = f"%Y-%m-%d {TIME_FORMAT}"

    title: str
    announcements: list[int]
    description: str | None = Field(default=None)

    @property
    @abstractmethod
    def reminder_time(self) -> datetime: ...  # noqa: E704

    @abstractmethod
    def _get_event_time_text(self, timezone: Timezone) -> str: ...  # noqa: E704

    def _get_event_time_with_timezones(self, timezones: Iterable[Timezone]) -> str:
        return " | ".join(map(self._get_event_time_text, timezones))

    def get_embed_name(self, timezones: Iterable[Timezone]) -> str:
        if self.description is None:
            return self.title

        return f"{self.title}: {self._get_event_time_with_timezones(timezones)}"

    def get_embed_value(self, timezones: Iterable[Timezone]) -> str:
        if self.description is not None:
            return self.description

        return self._get_event_time_with_timezones(timezones)
