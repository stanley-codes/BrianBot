import os
import discord
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents(members = True, messages = True, guilds = True, presences = True)
client = discord.Client(intents)

@client.event
async def on_ready():
    print(f'{client.user} is ready!')

    
@client.event
async def on_g_join(member):
    guild = str(member.guild)
    name = str(member.displayname)
    msg = f"Hi {name}! Welcome to {guild}! My name is Brian, I'm a bot here. If you need anything let me know by pinging !help"
    print(msg)
    await member.guild.get_channel(706419344070148147).send_message(msg)
        
@client.event
async def on_message(message):
        channel = str(message.channel)
        if channel == "testing-bots" and message.author != client.user:
            await message.channel.send('Hi my name is Brian!')

client.run(BOT_TOKEN)