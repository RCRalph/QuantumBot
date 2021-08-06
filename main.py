import discord
import datetime
from decouple import config


class Client(discord.Client):

    async def on_ready(self):
        print(f'[{datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}] Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        elif message.content.startswith('$hello'):
            await message.channel.send('Hello!')
        

client = Client()
client.run(config('BOT_TOKEN'))
