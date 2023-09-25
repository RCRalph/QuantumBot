import datetime, pytz, discord
from src.Formats import Formats
from src.Event import Event
from src.Translations import Translations
from src.Deadline import Deadline

class Server:
    name = ""
    server_id = 0
    announcement_channel_id = 0
    workshop_reaction_channel_id = 0
    language = ""
    timezones: list[str] = []
    schedule: dict[str, list[Event]] = {}
    deadlines: dict[str, list[Deadline]] = {}
    translations: Translations

    def __init__(self, data):
        self.name = data["name"]
        self.server_id = data["server_id"]
        self.announcement_channel_id = data["announcement_channel_id"]
        self.language = data["language"]
        self.timezones = data["timezones"]

        self.translations = Translations(data["language"])

        if "workshop_reaction_channel_id" in data:
            self.workshop_reaction_channel_id = data["workshop_reaction_channel_id"]

        if "schedule" in data:
            self.schedule_to_dict(data["schedule"])

        if "deadlines" in data:
            self.deadlines_to_dict(data["deadlines"])

    def get_timezones_text(self, start_UTC: datetime.datetime, end_UTC: datetime.datetime):
        result, title_date = [], ""

        for item in self.timezones:
            start_timestamp = start_UTC.astimezone(pytz.timezone(item))
            start_time = start_timestamp.strftime(Formats.TIME)
            start_date = start_timestamp.strftime(Formats.DATE)

            if not title_date:
                title_date = start_date

            end_timestamp = end_UTC.astimezone(pytz.timezone(item))
            end_time = end_timestamp.strftime(Formats.TIME)
            end_date = end_timestamp.strftime(Formats.DATE)

            if start_date != end_date:
                result.append(f"{start_date} {start_time} - {end_date} {end_time} {item}")
            elif start_time != end_time:
                result.append(f"{start_time} - {end_time} {item}")
            else:
                result.append(f"{start_time} {item}")

        return title_date, " | ".join(result)

    def schedule_to_dict(self, schedule: dict):
        self.schedule = {}

        for item in schedule:
            date, times = self.get_timezones_text(
                datetime.datetime.strptime(item["start"], Formats.DATETIME).replace(tzinfo=pytz.utc),
                datetime.datetime.strptime(item["end"], Formats.DATETIME).replace(tzinfo=pytz.utc),
            )

            event = Event(item["title"], item["start"], item["end"], times)

            if "announcements" in item:
                event.announcements = item["announcements"]

            if "description" in item:
                event.description = item["description"]

            if date in self.schedule:
                self.schedule[date].append(event)
            else:
                self.schedule[date] = [event]

        for date in self.schedule:
            self.schedule[date].sort(key = lambda x: x.times)

    def deadlines_to_dict(self, deadlines: dict):
        self.deadlines = {}

        for item in deadlines:
            date, times = self.get_timezones_text(
                datetime.datetime.strptime(item["time"], Formats.DATETIME).replace(tzinfo=pytz.utc),
                datetime.datetime.strptime(item["time"], Formats.DATETIME).replace(tzinfo=pytz.utc)
            )

            deadline = Deadline(item["title"], item["time"], times)

            if "announcements" in item:
                deadline.announcements = item["announcements"]

            if "description" in item:
                deadline.description = item["description"]

            if date in self.deadlines:
                self.deadlines[date].append(deadline)
            else:
                self.deadlines[date] = [deadline]

        for date in self.deadlines:
            self.deadlines[date].sort(key = lambda x: x.times)

    def get_date_header_name(self, date: str):
        header_limit = "-" * 6 + " " * 4

        return header_limit + date + header_limit[::-1]

    def get_date_header_value(self, date: str, show_event_span = True):
        weekday = datetime.datetime.strptime(date, Formats.DATE).weekday()
        result = self.translations.get_weekday(weekday)

        if show_event_span:
            start = min(self.schedule[date], key=lambda x: x.start_UTC)
            end = max(self.schedule[date], key=lambda x: x.end_UTC)

            _, event_span = self.get_timezones_text(
                datetime.datetime.strptime(start.start_UTC, Formats.DATETIME).replace(tzinfo=pytz.utc),
                datetime.datetime.strptime(end.end_UTC, Formats.DATETIME).replace(tzinfo=pytz.utc)
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

    def get_deadlines(self, embed: discord.Embed):
        if not self.deadlines:
            embed.add_field(
                name=self.translations.get_translation("deadlines-empty"),
                value="",
                inline=False
            )

        for date in sorted(list(self.deadlines.keys())):
            embed.add_field(
                name=self.get_date_header_name(date),
                value=self.get_date_header_value(date, False),
                inline=False
            )

            for event in sorted(self.deadlines[date], key=lambda x: x.times):
                value = f"{event.times}\n{event.description if event.description is not None else ''}"

                embed.add_field(
                    name=f"{event.title}",
                    value=value,
                    inline=False
                )

    def get_current_date(self):
        return datetime.datetime.now(datetime.timezone.utc) \
            .replace(tzinfo=pytz.utc) \
            .astimezone(pytz.timezone(self.timezones[0])) \
            .strftime(Formats.DATE)
