import discord
from src.Server import Server

class MessageReactionHandler:
    server: Server
    message: discord.Message

    def __init__(self, message: discord.Message, servers: dict[int, Server]):
        self.message = message

        if message.guild.id in servers:
            self.server = servers[message.guild.id]
        else:
            raise KeyError("Server not found")

    async def handle_reaction(self):
        if self.server.workshop_reaction_channel_id != self.message.channel.id:
            return

        content = self.message.content.capitalize()

        if content.startswith(self.server.translations.get_translation("task") + ":"):
            for item in ["🌕", "🌘", "⏲️"]:
                await self.message.add_reaction(item)


