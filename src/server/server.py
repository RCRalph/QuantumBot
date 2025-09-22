import logging
from collections import defaultdict
from datetime import date
from functools import cached_property
from itertools import chain
from pathlib import Path
from typing import Any, ClassVar, Generator, LiteralString, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from embed_splitter import EmbedField
from language import Language
from server.base_event import BaseEvent
from server.deadline import Deadline
from server.reaction import Reaction
from server.schedule_event import ScheduleEvent
from server.timezone import Timezone

logger = logging.getLogger(__name__)


class Server(BaseModel):
    DEFAULT_SERVERS_DIRECTORY: ClassVar[Path] = Path.cwd() / "servers"
    HEADER_PREFIX: ClassVar[LiteralString] = "━━━━━━"

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
        return sorted(chain(self.schedule, self.deadlines), key=lambda x: x.start_time)

    @cached_property
    def events_by_date(self) -> dict[date, list[BaseEvent]]:
        result = defaultdict(list)
        for event in self.events:
            result[event.start_time.date()].append(event)

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

    def _get_header_for_day(self, day: date) -> str:
        return f"{self.HEADER_PREFIX}      {day.isoformat()}      {self.HEADER_PREFIX}"

    def _get_event_span_text(self, events: list[BaseEvent]) -> str:
        start_time = min(event.start_time for event in events)
        end_time = max(event.end_time for event in events)

        event: BaseEvent
        if start_time == end_time:
            event = Deadline(title="", time=start_time)
        else:
            event = ScheduleEvent(title="", start=start_time, end=end_time)

        return event.get_embed_value(self.timezones)

    def get_full_schedule_embed_fields(self) -> Generator[EmbedField, None, None]:
        if not self.events:
            yield EmbedField(name=self.language.config.embed.schedule_empty, value="")
            return

        for event_date, events in self.events_by_date.items():
            yield EmbedField(
                name=self._get_header_for_day(event_date),
                value=self._get_event_span_text(events),
            )

            yield from self.get_todays_schedule_embed_fields(event_date)

    def get_todays_schedule_embed_fields(
        self, event_date: date
    ) -> Generator[EmbedField, None, None]:
        if not (events := self.events_by_date.get(event_date)):
            yield EmbedField(
                name=self.language.config.embed.schedule_today_empty, value=""
            )
            return

        for event in events:
            yield EmbedField(
                name=event.get_embed_name(self.timezones),
                value=event.get_embed_value(self.timezones),
            )
