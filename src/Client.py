import discord, aiocron
from src.ScheduleData import ScheduleData
from src.Translations import Translations

class Client(discord.Client):
    color = 0x2f3855

    async def on_ready(self):
        print(f"Logged in as {self.user}!", end="\n\n")
        self.schedule_data = ScheduleData()

        aiocron.crontab("* * * * *", self.check_for_announcements)

    async def check_for_announcements(self):
        for item in self.schedule_data.check_for_announcements():
            embed = discord.Embed(
                title = Translations.get_translation(
                    self.schedule_data.get_language(item["server_id"]),
                    "reminder"
                ),
                color = self.color
            )

            embed.add_field(name = item["name"], value = item["value"])

            await self.get_channel(item["channel_id"]).send("@everyone", embed = embed)

    async def hello(self, message: discord.Message):
        await message.channel.send(f"Hello {message.author.mention}!")

    async def schedule_full(self, message: discord.Message):
        embed = discord.Embed(
            title = Translations.get_translation(
                self.schedule_data.get_language(message.guild.id),
                "schedule"
            ) + " - " + self.schedule_data.schedules[message.guild.id].name,
            color = self.color
        )

        if not self.schedule_data.get_full_schedule(message.guild.id, embed):
            embed.add_field(name = Translations.get_translation(
                self.schedule_data.get_language(message.guild.id),
                "schedule-empty"
            ))

        await message.channel.send(embed = embed)

    async def schedule(self, message: discord.Message):
        embed = discord.Embed(
            title = Translations.get_translation(
                self.schedule_data.get_language(message.guild.id),
                "schedule-today"
            ),
            color = self.color
        )

        if not self.schedule_data.get_todays_schedule(message.guild.id, embed):
            embed.add_field(name = Translations.get_translation(
                self.schedule_data.get_language(message.guild.id),
                "schedule-empty"
            ))

        await message.channel.send(embed = embed)

    async def on_message(self, message: discord.Message):
        COMMANDS = [
            {
                "callout": "!hello",
                "description": "hello-description",
                "function": self.hello
            },
            {
                "callout": "!schedule-full",
                "description": "schedule-full-description",
                "function": self.schedule_full
            },
            {
                "callout": "!schedule",
                "description": "schedule-description",
                "function": self.schedule
            },
        ]

        if message.author == self.user:
            return

        if message.content.startswith("!help"):
            embed = discord.Embed(
                title = Translations.get_translation(
                    self.schedule_data.get_language(message.guild.id),
                    "help"
                ),
                color = self.color
            )

            embed.add_field(
                name="!help",
                value=Translations.get_translation(
                    self.schedule_data.get_language(message.guild.id),
                    "help-description"
                ),
                inline=False
            )

            for item in sorted(COMMANDS, key = lambda x: x["callout"]):
                embed.add_field(
                    name=item["callout"],
                    value=Translations.get_translation(
                        self.schedule_data.get_language(message.guild.id),
                        item["description"]
                    ),
                    inline=False
                )

            await message.channel.send(embed = embed)
            return

        for item in COMMANDS:
            if message.content.startswith(item["callout"]):
                await item["function"](message)
                return
