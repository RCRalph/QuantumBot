import discord, aiocron
from src.Servers import Servers
from src.Translations import Translations

class Client(discord.Client):
    color = 0x2f3855
    servers_data: Servers = None

    async def on_ready(self):
        print(f"Logged in as {self.user}!", end="\n\n")
        self.servers_data = Servers()

        aiocron.crontab("* * * * *", self.check_for_announcements)

    async def check_for_announcements(self):
        for item in self.servers_data.check_for_announcements():
            embed = discord.Embed(
                title = Translations.get_translation(
                    self.servers_data.servers[item["server_id"]].language,
                    "reminder"
                ),
                color = self.color
            )

            embed.add_field(name=item["name"], value=item["value"])

            await self.get_channel(item["channel_id"]).send("@everyone", embed=embed)

    async def hello(self, message: discord.Message):
        await message.channel.send(f"Hello {message.author.mention}!")

    async def schedule_full(self, message: discord.Message):
        embed = discord.Embed(
            title=Translations.get_translation(
                self.servers_data.servers[message.guild.id].language,
                "schedule"
            ) + " - " + self.servers_data.servers[message.guild.id].name,
            color=self.color
        )

        if message.guild.id in self.servers_data.servers:
            self.servers_data.servers[message.guild.id].get_full_schedule(embed)
        else:
            embed.add_field(
                name=Translations.get_translation(
                    self.servers_data.servers[message.guild.id].language,
                    "schedule-empty"
                ),
                value=""
            )

        await message.channel.send(embed=embed)

    async def schedule(self, message: discord.Message):
        embed = discord.Embed(
            title=Translations.get_translation(
                self.servers_data.servers[message.guild.id].language,
                "schedule-today"
            ),
            color=self.color
        )

        if not self.servers_data.servers[message.guild.id].get_todays_schedule(embed):
            embed.add_field(name=Translations.get_translation(
                self.servers_data.servers[message.guild.id].language,
                "schedule-empty"
            ))

        await message.channel.send(embed=embed)

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

        if self.servers_data.servers[message.guild.id].workshop_reaction_channel_id == message.channel.id:
            task_callout = Translations.get_translation(
                self.servers_data.servers[message.guild.id].language,
                'task'
            )

            if message.content.capitalize().startswith(task_callout + ":"):
                await message.add_reaction("🌕")
                await message.add_reaction("🌘")
                await message.add_reaction("☁️")

        if message.content.startswith("!help"):
            embed = discord.Embed(
                title=Translations.get_translation(
                    self.servers_data.servers[message.guild.id].language,
                    "help"
                ),
                color=self.color
            )

            embed.add_field(
                name="!help",
                value=Translations.get_translation(
                    self.servers_data.servers[message.guild.id].language,
                    "help-description"
                ),
                inline=False
            )

            for item in sorted(COMMANDS, key=lambda x: x["callout"]):
                embed.add_field(
                    name=item["callout"],
                    value=Translations.get_translation(
                        self.servers_data.servers[message.guild.id].language,
                        item["description"]
                    ),
                    inline=False
                )

            await message.channel.send(embed=embed)
            return

        for item in COMMANDS:
            if message.content.startswith(item["callout"]):
                await item["function"](message)
                return
