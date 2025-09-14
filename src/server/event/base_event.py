from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, Field


class BaseEvent(BaseModel, ABC):
    DATETIME_FORMAT: ClassVar[str] = "%Y-%m-%d %H:%M"

    title: str
    announcements: list[int]
    description: str | None = Field(default=None)

    @property
    @abstractmethod
    def reminder_time(self) -> datetime: ...  # noqa: E704
