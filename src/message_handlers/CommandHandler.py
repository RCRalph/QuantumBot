import discord
from src.Translations import Translations
from src.Server import Server
from src.SplitEmbed import SplitEmbed

class CommandHandler:
    EMBED_COLOR = 0x2f3855
    server: Server
    message: discord.Message
    translations: Translations

    def __init__(self, message: discord.Message, servers: dict[int, Server]):
        self.message = message

        if message.guild.id in servers:
            self.server = servers[message.guild.id]
            self.translations = Translations(self.server.language)
        else:
            raise KeyError("Server not found")

    async def handle_message(self):
        if None in [self.message, self.translations, self.server]:
            return await self.config_not_found()

        command_content = self.message.content[1:].split(" ", 2)
        command_name = command_content[0]
        arguments = command_content[1] if len(command_content) > 1 else ""

        match command_name.lower():
            case "test":
                await self.test()
            case "schedule":
                await self.schedule(arguments)

    async def config_not_found(self):
        await self.message.channel.send("Server configuration not found!")

    async def test(self):
        await self.message.channel.send(self.translations.get_translation("test"))

    async def schedule(self, arguments: str):
        arguments = arguments.strip().lower()
        full_schedule = arguments.startswith("full") or arguments.startswith("all")

        embed = discord.Embed(
            title=self.translations.get_translation(
                "schedule" if full_schedule else "schedule-today"
            ) + f" - {self.server.name}",
            color=self.EMBED_COLOR
        )

        if full_schedule:
            self.server.get_full_schedule(embed)
        else:
            self.server.get_todays_schedule(embed)

        for item in SplitEmbed(embed).get_embeds():
            await self.message.channel.send(embed=item)
