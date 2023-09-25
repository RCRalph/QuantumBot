import datetime, discord

from src.Server import Server
from src.Formats import Formats
from src.Translations import Translations
from src.Event import Event
from src.Deadline import Deadline

class Announcement:
    embed: discord.Embed
    channel_id: int

    def __init__(self, channel_id: int, embed: discord.Embed):
        self.channel_id = channel_id
        self.embed = embed

class AnnouncementHandler:
    EMBED_COLOR = 0x2f3855
    servers: dict[int, Server] = dict()
    announcements: list[Announcement] = list()

    def __init__(self, servers: dict[int, Server]):
        self.servers = servers

        self.check_schedule_announcements()

    def get_announcements(self):
        for i in self.announcements:
            yield i

        self.announcements.clear()

    def make_announcement(self, translations: Translations, server: Server, event: Event | Deadline):
        embed = discord.Embed(
            title=translations.get_translation("reminder"),
            color=self.EMBED_COLOR
        )

        embed.add_field(
            name=f"{event.title}: {event.times}" if event.description is not None else event.title,
            value=event.description if event.description is not None else event.times,
            inline=False
        )

        self.announcements.append(Announcement(server.announcement_channel_id, embed))

    def check_schedule_announcements(self):
        current_datetime = datetime.datetime.now(datetime.timezone.utc)

        for server_id in self.servers:
            for date in self.servers[server_id].schedule:
                for event in self.servers[server_id].schedule[date]:
                    for i in event.announcements:
                        timestamp = current_datetime + datetime.timedelta(minutes = i)

                        if timestamp.strftime(Formats.DATETIME) == event.start_UTC:
                            self.make_announcement(self.servers[server_id].translations, self.servers[server_id], event)

    def check_deadline_announcements(self):
        current_datetime = datetime.datetime.now(datetime.timezone.utc)

        for server_id in self.servers:
            for date in self.servers[server_id].deadlines:
                for deadline in self.servers[server_id].deadlines[date]:
                    for i in deadline.announcements:
                        timestamp = current_datetime + datetime.timedelta(minutes = i)

                        if timestamp.strftime(Formats.DATETIME) == deadline.time_UTC:
                            self.make_announcement(self.servers[server_id].translations, self.servers[server_id], deadline)
