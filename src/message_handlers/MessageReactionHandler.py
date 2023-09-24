import discord
from src.Translations import Translations
from src.Server import Server

class MessageReactionHandler:
    server = None
    message = None
    translations = None

    def __init__(self, message: discord.Message, servers: dict[int, Server]):
        self.message = message

        if message.guild.id in servers:
            self.server = servers[message.guild.id]
            self.translations = Translations(self.server.language)

    async def handle_reaction(self):
        if None in [self.message, self.translations, self.server]:
            return

        content = self.message.content.capitalize()

        if content.startswith(self.translations.get_translation("task") + ":"):
            for item in ["🌕", "🌘", "☁️"]:
                await self.message.add_reaction(item)


