import logging
from collections import defaultdict
from datetime import date
from functools import cached_property
from itertools import chain
from pathlib import Path
from typing import Any, ClassVar, LiteralString, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from language import Language
from server.base_event import BaseEvent
from server.deadline import Deadline
from server.reaction import Reaction
from server.schedule_event import ScheduleEvent
from server.timezone import Timezone

logger = logging.getLogger(__name__)


class Server(BaseModel):
    DEFAULT_SERVERS_DIRECTORY: ClassVar[Path] = Path.cwd() / "servers"
    DATE_EMBED_NAME_TITLE: ClassVar[LiteralString] = "━━━━━━      {date}      ━━━━━━"

    name: str
    server_id: int
    announcement_channel_id: int
    reactions: dict[int, Reaction] = Field(default_factory=dict)
    language: Language
    timezones: list[Timezone] = Field(alias="timezones")
    schedule: list[ScheduleEvent] = Field(default_factory=list)
    deadlines: list[Deadline] = Field(default_factory=list)

    @field_validator("timezones", mode="before")
    @classmethod
    def normalize_timezones(cls, items: Any) -> list[Timezone]:
        result: list[Timezone] = []

        if not isinstance(items, list):
            raise TypeError(f"Timezones should be a list, instead got: {type(items)}")

        for item in items:
            match item:
                case Timezone():
                    timezone = item
                case dict():
                    timezone = Timezone.model_validate(item)
                case str():
                    timezone = Timezone(name=item, text=item)
                case _:
                    raise TypeError(f"Unsupported timezone type: {type(item)}")

            result.append(timezone)

        return result

    @model_validator(mode="after")
    def ensure_timezones_are_distinct(self) -> Self:
        if len(set(self.timezones)) != len(self.timezones):
            raise ValueError("Timezones must be distinct")

        return self

    @cached_property
    def events(self) -> list[BaseEvent]:
        return sorted(
            chain(self.schedule, self.deadlines), key=lambda x: x.reminder_time
        )

    @cached_property
    def events_by_date(self) -> dict[date, list[BaseEvent]]:
        result = defaultdict(list)
        for event in self.events:
            result[event.reminder_time.date()].append(event)

        return dict(result)

    @classmethod
    def from_directory(
        cls, directory: Path = DEFAULT_SERVERS_DIRECTORY
    ) -> dict[int, Self]:
        files = (
            item
            for item in directory.iterdir()
            if item.is_file() and item.name.endswith(".json")
        )

        servers: dict[int, Self] = {}
        exceptions: list[Exception] = []

        for file_path in files:
            try:
                server = cls.model_validate_json(file_path.read_text())
                servers[server.server_id] = server
            except Exception as exc:
                exceptions.append(exc)

        if exceptions:
            raise ExceptionGroup("Error loading server data", exceptions)

        logger.info("Successfully loaded %s servers", len(servers))

        return servers
