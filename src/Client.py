import discord, aiocron, os, json, datetime
from decouple import config
from src.Server import Server
from src.Validator import Validator
from src.message_handlers.CommandHandler import CommandHandler
from src.message_handlers.AnnouncementHandler import AnnouncementHandler
from src.message_handlers.MessageReactionHandler import MessageReactionHandler

class Client(discord.Client):
    servers_data: dict[int, Server]
    SERVER_DIRECTORY = "servers"

    async def on_ready(self):
        print(f"{datetime.datetime.now()}: Logged in as {self.user}!")

        self.servers_data = {}
        self.load_servers()

        aiocron.crontab("* * * * *", self.check_for_announcements)

    def load_servers(self):
        files = [
            item for item in os.listdir(self.SERVER_DIRECTORY)
            if Validator.is_json_file(self.SERVER_DIRECTORY, item)
        ]

        invalid_servers: list[str] = []
        successful_servers: list[str] = []

        for filename in files:
            with open(f"{self.SERVER_DIRECTORY}/{filename}") as file:
                content = json.load(file)

                if Validator(file.name, content).validate():
                    self.servers_data[content["server_id"]] = Server(content)
                    successful_servers.append(content["name"])
                else:
                    invalid_servers.append(filename)

        # ----- Summary -----
        if successful_servers:
            print("Successfully loaded the following servers:")
            for item in sorted(successful_servers):
                print(f" - {item}")
            else:
                print()

        if invalid_servers:
            print("Invalid schedule files:")
            for item in sorted(invalid_servers):
                print(f" - {item}")
            else:
                print()

    async def check_for_announcements(self):
        announcements = AnnouncementHandler(self.servers_data).get_announcements()

        if len(announcements):
            print(f"{datetime.datetime.now()}: Started sending announcements ({len(announcements)}):")

            for item in announcements:
                channel = self.get_channel(item.channel_id)
                await channel.send("@everyone", embed=item.embed)
                print(f"Made announcement: {item.embed.fields[0].name}")

            print()

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        try:
            if message.content.startswith(config("BOT_PREFIX")):
                await CommandHandler(message, self.servers_data).handle_message()
            else:
                await MessageReactionHandler(message, self.servers_data).handle_reaction()
        except KeyError as exc:
            print(exc)
