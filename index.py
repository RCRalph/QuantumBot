import discord
from decouple import config
from src.Client import Client

client = Client(intents=discord.Intents.all())
client.run(config('BOT_TOKEN'))
