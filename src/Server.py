import datetime, pytz
from src.Formats import Formats
from src.Event import Event

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

    def get_timezones_text(self, timezones: list, start_UTC: datetime.datetime, end_UTC: datetime.datetime):
        result, title_date = [], ""

        for item in timezones:
            start_timestamp = start_UTC.astimezone(pytz.timezone(item))
            start_time = start_timestamp.strftime(Formats.TIME)
            start_date = start_timestamp.strftime(Formats.DATE)

            if not title_date:
                title_date = start_date

            end_timestamp = end_UTC.astimezone(pytz.timezone(item))
            end_time = end_timestamp.strftime(Formats.TIME)
            end_date = end_timestamp.strftime(Formats.DATE)

            if start_date != end_date:
                result.append(f"{start_date} {start_time} {item} - {end_date} {end_time} {item}")
            elif start_time != end_time:
                result.append(f"{start_time} - {end_time} {item}")
            else:
                result.append(f"{start_time} {item}")

        return title_date, " | ".join(result)

    def schedule_to_dict(self, schedule: dict):
        self.schedule = {}

        for item in schedule:
            date, times = self.get_timezones_text(
                self.timezones,
                datetime.datetime.strptime(item["start"], Formats.DATETIME).replace(tzinfo=pytz.utc),
                datetime.datetime.strptime(item["end"], Formats.DATETIME).replace(tzinfo=pytz.utc),
            )

            event = Event(item["title"], item["start"], times)

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
