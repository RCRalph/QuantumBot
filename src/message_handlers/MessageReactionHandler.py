import discord
from src.Server import Server

class MessageReactionHandler:
    server: Server
    message: discord.Message

    def __init__(self, message: discord.Message, servers: dict[int, Server]):
        self.message = message

        if message.guild.id in servers:
            self.server = servers[message.guild.id]

    async def handle_reaction(self):
        if None in [self.message, self.server]:
            return

        content = self.message.content.capitalize()

        if content.startswith(self.server.translations.get_translation("task") + ":"):
            for item in ["🌕", "🌘", "☁️"]:
                await self.message.add_reaction(item)


