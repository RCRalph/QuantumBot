import discord
import datetime
from decouple import config



class Client(discord.Client):

    async def on_ready(self):
        print(f'[{datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}] Logged in as {self.user}')


    async def on_message(self, message):
        if message.author == self.user:
            return

        elif message.content.startswith('!hello'):
            await message.channel.send('Hello!')
        
        elif message.content.startswith('!agenda'):
            if datetime.date.today == datetime.date(2021, 9, 25):
                embed=discord.Embed(title="Hackathon Agenda (25.09)", color=0x7845d1)
                embed.add_field(name="Kick-off Lecture", value="12:00 - 13:00", inline=False)
                embed.add_field(name="Matchmaking", value="13:00 - 14:00", inline=False)
                embed.add_field(name="Quantum Games - Piotr Biskupi", value="14:00 - 15:00", inline=False)
                embed.add_field(name="Quantum Computing - Piotr Gawron", value="15:00 - 16:00", inline=False)
                embed.add_field(name="JavaScript Programming Language- Piotr Migdał", value="17:00 - 19:00", inline=False)
            elif datetime.date.today == datetime.date(2021, 9, 26):
                embed = discord.Embed(title="Hackathon Agenda (26.09)", color=0x7845d1)
                embed.add_field(name='Playablity - Artur Roszczyk (Orbital Knight)', value='12:00 - 13:00', inline=False)
                embed.add_field(name='\"Linear algebra is actually a fun videogame: Quantum Odyssey\"', value='14:00 - 15:00', inline=False)
                embed.add_field(name='User Experience - Klem Jankiewicz', value='17:00 -18:00', inline=False)
            else:
                embed = discord.Embed(title="Work on you projects!", color=0x7845d1)
            await message.channel.send(embed=embed)
        
        elif message.content.startwith('!help'):
            embed = discord.Embed(title='Available Commands', color=0x000000)

    async def on_member_join(self, member):
        guest = discord.utils.get(member.guild.roles, name="Guest")
        await member.add_roles(guest)

    async def on_raw_reaction_add(self, payload):
        #Add roles after reaction to specific message
        if str(payload.message_id) != config('MESSAGE_ID'):
            return
        if str(payload.emoji) == '❤️':
            print('czerwone')
        elif str(payload.emoji) == '💙':
            print('niebieskie')
        

intents = discord.Intents.all() #TODO: set intents


client = Client(intents=intents)
client.run(config('BOT_TOKEN'))