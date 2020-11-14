import os
import discord
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents(members = True, messages = True, guilds = True, presences = True)


class BrianBot(discord.Client):


    async def on_ready(self):
        print(f'{self.user} is ready!')

    async def on_member_join(self, member):
        guild = str(member.guild)
        name = member.mention
        msg = f"Hi {name}! Welcome to {guild}! My name is Brian, I'm a bot here. If you need anything let me know by pinging !help"
        await member.guild.get_channel(706419344070148147).send(msg)
        
    async def on_message(self, message):
        channel = str(message.channel)
        if channel == "testing-bots" and message.author != client.user:
            await message.channel.send('Hi my name is Brian!')
client = BrianBot(intents = intents)
client.run(BOT_TOKEN)