import discord
import datetime
import json
import aiocron

from decouple import config

dateFormat, color = "%Y-%m-%d %H:%M", 0x7845d1

@aiocron.crontab("* * * * *")
async def check_for_announcement():
    agenda = json.load(open(config("AGENDA_FILE_NAME")))
    messageChannel = client.get_channel(int(config('ANNOUNCEMENT_CHANNEL_ID')))
    currentDate = datetime.datetime.now()

    for i in agenda:
        startDate = datetime.datetime.strptime(i["start"], dateFormat)
        if (currentDate.strftime(dateFormat) == startDate.strftime(dateFormat)):
            embed = discord.Embed(title="Reminder!", color=color)

            startHour = datetime.datetime.strptime(i["start"], dateFormat).strftime("%H:%M")
            endHour = datetime.datetime.strptime(i["end"], dateFormat).strftime("%H:%M")
            embed.add_field(name=i["title"], value=f"{startHour} - {endHour}", inline=False)

            await messageChannel.send(embed=embed)
            print("Sent announcement message")

class Client(discord.Client):
    async def on_ready(self):
        print(f'[{datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}] Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        elif message.content.startswith('!hello'):
            await message.channel.send(f'Hello {message.author.mention}!')
        
        elif message.content.startswith('!agenda'):
            agenda = json.load(open(config("AGENDA_FILE_NAME")))
            currentDate = datetime.datetime.today()

            todaysAgenda = []
            for i in agenda:
                startDate = datetime.datetime.strptime(i["start"], dateFormat)
                if (startDate.strftime("%Y-%m-%d") == currentDate.strftime("%Y-%m-%d")):
                    todaysAgenda.append(i)
            
            if (todaysAgenda):
                embed = discord.Embed(title="Agenda ({})".format(currentDate.strftime("%Y-%m-%d")), color=color)
                for i in todaysAgenda:
                    startHour = datetime.datetime.strptime(i["start"], dateFormat).strftime("%H:%M")
                    endHour = datetime.datetime.strptime(i["end"], dateFormat).strftime("%H:%M")
                    embed.add_field(name=i["title"], value=f"{startHour} - {endHour}", inline=False)
            else:
                embed = discord.Embed(title="Agenda doesn't exist for the current day!", color=color)

            await message.channel.send(embed=embed)
        
        elif message.content.startswith('!help'):
            embed = discord.Embed(title='Available Commands', color=color)

            embed.add_field(name="!hello", value="Welcomes the user.", inline=False)
            embed.add_field(name="!agenda", value="Shows agenda for the current day", inline=False)
            embed.add_field(name="!help", value="Shows available commands", inline=False)

            await message.channel.send(embed=embed)

# Start execution
print("Starting the bot...")
intents = discord.Intents.all() #TODO: set intents

client = Client(intents=intents)
client.run(config('BOT_TOKEN'))