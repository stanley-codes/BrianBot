import os
import discord
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

class BrianClient(discord.Client):
    async def on_ready(self):
     print(f'{self.user} has connected to Discord!')

client = BrianClient() 
client.run(BOT_TOKEN)