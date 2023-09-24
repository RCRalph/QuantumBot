import discord
from decouple import config
from src.Client import Client

intents = discord.Intents().default()

# Explicit intents
intents.message_content = True

client = Client(intents=intents)
client.run(config("BOT_TOKEN"))
