from typing import Any, ClassVar
from zoneinfo import available_timezones, ZoneInfo

from pydantic import BaseModel, ConfigDict, field_validator


class Timezone(BaseModel):
    AVAILABLE_TIMEZONES: ClassVar[frozenset[str]] = frozenset(available_timezones())

    model_config = ConfigDict(frozen=True)

    name: str
    text: str

    @field_validator("name", mode="before")
    @classmethod
    def ensure_name_is_timezone(cls, name: str) -> str:
        if name not in cls.AVAILABLE_TIMEZONES:
            raise ValueError(f"'{name}' isn't a valid timezone")

        return name

    @property
    def zone_info(self) -> ZoneInfo:
        return ZoneInfo(self.name)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Timezone):
            return False

        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
