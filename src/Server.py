import datetime, pytz, discord
from src.Formats import Formats
from src.Event import Event
from src.Translations import Translations

class Server:
    name = ""
    server_id = 0
    announcement_channel_id = 0
    language = ""
    timezones: list[str] = []
    schedule: dict[str, list[Event]] = {}
    last_date = datetime.datetime.now()

    def __init__(self, data):
        self.name = data["name"]
        self.server_id = data["server_id"]
        self.announcement_channel_id = data["announcement_channel_id"]
        self.language = data["language"]
        self.timezones = data["timezones"]

        self.schedule_to_dict(data["schedule"])
        self.last_event_datetime(data["schedule"])

    def last_event_datetime(self, schedule: dict):
        last_ending_event = max(schedule, key = lambda x: x["end"])
        self.last_date = datetime.datetime.strptime(last_ending_event["end"], Formats.DATETIME)

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

    def get_date_header_name(self, date: str):
        header_limit = "-" * 6 + " " * 4

        return header_limit + date + header_limit[::-1]

    def get_date_header_value(self, date: str):
        weekday = datetime.datetime.strptime(date, Formats.DATE).weekday()
        weekday_name = Translations.get_translation(self.language, "weekdays")[weekday]

        start = min(self.schedule[date], key=lambda x: x.start_UTC)
        end = max(self.schedule[date], key=lambda x: x.end_UTC)

        event_span = self.get_timezones_text(
            datetime.datetime.strptime(start.start_UTC, Formats.DATETIME).replace(tzinfo=pytz.utc),
            datetime.datetime.strptime(end.end_UTC, Formats.DATETIME).replace(tzinfo=pytz.utc)
        )

        return f"{weekday_name}, {event_span[1]}"

    def get_full_schedule(self, embed: discord.Embed):
        if not self.schedule:
            embed.add_field(
                name=Translations.get_translation(self.language, 'schedule-empty'),
                value="",
                inline=False
            )

        for date in sorted(list(self.schedule.keys())):
            embed.add_field(
                name=self.get_date_header_name(date),
                value=self.get_date_header_value(date)
            )

            for event in sorted(self.schedule[date], key=lambda x: x.times):
                value = f"{event.times}\n{event.description if event.description is not None else ''}"

                embed.add_field(
                    name=f"{event.title}",
                    value=value,
                    inline=False
                )

    def get_todays_schedule(self, embed: discord.Embed):
        date = self.get_current_timestamp() \
            .replace(tzinfo=pytz.utc) \
            .astimezone(pytz.timezone(self.timezones[0])) \
            .strftime(Formats.DATE)

        if date in self.schedule:
            for event in self.schedule[date]:
                embed.add_field(
                    name=f"{event.title}: {event.times}",
                    value=event.description if event.description is not None else "",
                    inline=False
                )
        else:
            embed.add_field(
                name=Translations.get_translation(self.language, 'schedule-today-empty'),
                value="",
                inline=False
            )

        return True

    def get_current_timestamp(self):
        return datetime.datetime.now(datetime.timezone.utc)
