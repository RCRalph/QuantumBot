import discord
import datetime
import json
import aiocron

from decouple import config

dateFormat, color = "%Y-%m-%d %H:%M", 0x7845d1

@aiocron.crontab("* * * * *")
async def check_for_announcement():
    agenda = json.load(open(config("SCHEDULES_FILE_NAME")))

    for j in agenda:
        messageChannel = client.get_channel(j["channel_id"])
        currentDate = datetime.datetime.now(datetime.timezone.utc)

        for i in j["schedule"]:
            startDate = datetime.datetime.strptime(i["start"], dateFormat)
            if (currentDate.strftime(dateFormat) == startDate.strftime(dateFormat)):
                embed = discord.Embed(title="Reminder!", color=color)

                startHour = datetime.datetime.strptime(i["start"], dateFormat).strftime("%H:%M")
                endHour = datetime.datetime.strptime(i["end"], dateFormat).strftime("%H:%M")
                embed.add_field(name=i["title"], value=f"{startHour} - {endHour} GMT", inline=False)

                await messageChannel.send(embed=embed)
                print(f"Sent announcement message: {i['title']}")

class Client(discord.Client):
    async def on_ready(self):
        print(f'[{datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}] Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        elif message.content.startswith('!hello'):
            await message.channel.send(f'Hello {message.author.mention}!')

        elif message.content.startswith('!agenda-full'):
            currentDate = datetime.datetime.today()
            agenda = json.load(open(config("SCHEDULES_FILE_NAME")))
            serverID = message.guild.id

            for j in agenda:
                if (j["server_id"] == serverID):
                    embed = discord.Embed(title="Full agenda".format(currentDate.strftime("%Y-%m-%d")), color=color)
                    for i in j["schedule"]:
                        startHour = datetime.datetime.strptime(i["start"], dateFormat).strftime("%H:%M")
                        endHour = datetime.datetime.strptime(i["end"], dateFormat).strftime("%H:%M")
                        embed.add_field(name=i["title"], value=f"{startHour} - {endHour} GMT", inline=False)

                await message.channel.send(embed=embed)
                break
        
        elif message.content.startswith('!agenda'):
            agenda = json.load(open(config("SCHEDULES_FILE_NAME")))
            serverID = message.guild.id

            for j in agenda:
                if (j["server_id"] == serverID):
                    currentDate = datetime.datetime.today()

                    todaysAgenda = []
                    for i in j["schedule"]:
                        startDate = datetime.datetime.strptime(i["start"], dateFormat)
                        if (startDate.strftime("%Y-%m-%d") == currentDate.strftime("%Y-%m-%d")):
                            todaysAgenda.append(i)
                    
                    if (todaysAgenda):
                        embed = discord.Embed(title="Agenda ({})".format(currentDate.strftime("%Y-%m-%d")), color=color)
                        for i in todaysAgenda:
                            startHour = datetime.datetime.strptime(i["start"], dateFormat).strftime("%H:%M")
                            endHour = datetime.datetime.strptime(i["end"], dateFormat).strftime("%H:%M")
                            embed.add_field(name=i["title"], value=f"{startHour} - {endHour} GMT", inline=False)
                    else:
                        embed = discord.Embed(title="Today's agenda is empty!", color=color)

                    await message.channel.send(embed=embed)
                    break
        
        elif message.content.startswith('!help'):
            embed = discord.Embed(title='Available Commands', color=color)

            embed.add_field(name="!help", value="Shows available commands", inline=False)
            embed.add_field(name="!hello", value="Greets the user.", inline=False)
            embed.add_field(name="!agenda", value="Shows today's agenda", inline=False)
            embed.add_field(name="!agenda-full", value="Shows full agenda", inline=False)


            await message.channel.send(embed=embed)

# Start execution
print("Starting the bot...")
intents = discord.Intents.all()

client = Client(intents=intents)
client.run(config('BOT_TOKEN'))