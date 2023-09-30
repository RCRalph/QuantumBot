import datetime, discord
from zoneinfo import ZoneInfo
from src.Formats import Formats
from src.Event import Event
from src.Translations import Translations
from src.TimezoneData import TimezoneData

class Server:
    name: str
    server_id: int
    announcement_channel_id: int
    workshop_reaction_channel_id: int
    language: str
    translations: Translations
    timezones: list[TimezoneData]
    schedule: dict[str, list[Event]]

    def __init__(self, data):
        self.name = data["name"]
        self.server_id = data["server_id"]
        self.announcement_channel_id = data["announcement_channel_id"]

        if "workshop_reaction_channel_id" in data:
            self.workshop_reaction_channel_id = data["workshop_reaction_channel_id"]
        else:
            self.workshop_reaction_channel_id = 0

        self.language = data["language"]
        self.translations = Translations(data["language"])

        self.timezones = []
        for item in data["timezones"]:
            match item:
                case dict() as timezone_data:
                    self.timezones.append(TimezoneData(
                        timezone_data["name"],
                        timezone_data["text"]
                    ))
                case str() as name:
                    self.timezones.append(TimezoneData(name))

        self.schedule = {}
        if "schedule" in data:
            self.schedule_to_dict(data["schedule"])
        if "deadlines" in data:
            self.deadlines_to_dict(data["deadlines"])

    def get_timezones_text(self, start_UTC: datetime.datetime, end_UTC: datetime.datetime):
        result, title_date = [], ""

        for item in self.timezones:
            start_timestamp = start_UTC.astimezone(item.timezone)
            start_date, start_time = start_timestamp.strftime(Formats.DATETIME).split(" ", 2)

            if not title_date:
                title_date = start_date

            end_timestamp = end_UTC.astimezone(item.timezone)
            end_date, end_time = end_timestamp.strftime(Formats.DATETIME).split(" ", 2)

            if start_date != end_date:
                result.append(f"{start_date} {start_time} → {end_date} {end_time} {item.text}")
            elif start_time != end_time:
                result.append(f"{start_time} → {end_time} {item.text}")
            else:
                result.append(f"{start_time} {item.text}")

        return title_date, " | ".join(result)

    def schedule_to_dict(self, schedule: dict):
        for item in schedule:
            date, times = self.get_timezones_text(
                datetime.datetime.strptime(item["start"], Formats.DATETIME).replace(tzinfo=datetime.timezone.utc),
                datetime.datetime.strptime(item["end"], Formats.DATETIME).replace(tzinfo=datetime.timezone.utc),
            )

            event = Event(
                item["title"],
                item["start"],
                item["end"],
                times,
                item["announcements"] if "announcements" in item else [10],
                item["description"] if "description" in item else None
            )

            if date in self.schedule:
                self.schedule[date].append(event)
            else:
                self.schedule[date] = [event]

        for date in self.schedule:
            self.schedule[date].sort(key = lambda x: x.times)

    def deadlines_to_dict(self, deadlines: dict):
        for item in deadlines:
            date, times = self.get_timezones_text(
                datetime.datetime.strptime(item["time"], Formats.DATETIME).replace(tzinfo=datetime.timezone.utc),
                datetime.datetime.strptime(item["time"], Formats.DATETIME).replace(tzinfo=datetime.timezone.utc)
            )

            event = Event(
                item["title"],
                item["time"],
                item["time"],
                times,
                item["announcements"] if "announcements" in item else [600, 240, 120],
                item["description"] if "description" in item else None
            )

            if date in self.schedule:
                self.schedule[date].append(event)
            else:
                self.schedule[date] = [event]

        for date in self.schedule:
            self.schedule[date].sort(key = lambda x: x.times)

    def get_date_header_name(self, date: str):
        header_limit = "━" * 6 + " " * 6

        return header_limit + date + header_limit[::-1]

    def get_date_header_value(self, date: str, show_event_span = True):
        weekday = datetime.datetime.strptime(date, Formats.DATE).weekday()
        result = self.translations.get_weekday(weekday)

        if show_event_span:
            start = min(self.schedule[date], key=lambda x: x.start_UTC)
            end = max(self.schedule[date], key=lambda x: x.end_UTC)

            _, event_span = self.get_timezones_text(
                datetime.datetime.strptime(start.start_UTC, Formats.DATETIME).replace(tzinfo=datetime.timezone.utc),
                datetime.datetime.strptime(end.end_UTC, Formats.DATETIME).replace(tzinfo=datetime.timezone.utc)
            )

            result = f"{result}, {event_span}"

        return result

    def get_full_schedule(self, embed: discord.Embed):
        if not self.schedule:
            embed.add_field(
                name=self.translations.get_translation("schedule-empty"),
                value="",
                inline=False
            )

        for date in sorted(list(self.schedule.keys())):
            embed.add_field(
                name=self.get_date_header_name(date),
                value=self.get_date_header_value(date),
                inline=False
            )

            for event in sorted(self.schedule[date], key=lambda x: x.times):
                value = f"{event.times}\n{event.description if event.description is not None else ''}"

                embed.add_field(
                    name=f"{event.title}",
                    value=value,
                    inline=False
                )

    def get_todays_schedule(self, embed: discord.Embed):
        date = self.get_current_date()

        if not self.schedule:
            embed.add_field(
                name=self.translations.get_translation("schedule-empty"),
                value="",
                inline=False
            )
        elif date in self.schedule:
            for event in self.schedule[date]:
                embed.add_field(
                    name=f"{event.title}: {event.times}",
                    value=event.description if event.description is not None else "",
                    inline=False
                )
        else:
            embed.add_field(
                name=self.translations.get_translation("schedule-today-empty"),
                value="",
                inline=False
            )

    def get_current_date(self):
        return datetime.datetime.now(self.timezones[0].timezone).strftime(Formats.DATE)
