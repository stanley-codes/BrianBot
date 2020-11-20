import os
import discord
from discord.ext import commands
import time
from gtts import gTTS
from ctypes.util import find_library
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents(members = True, messages = True, guilds = True, presences = True, voice_states = True)
discord.opus.load_opus(find_library('opus'))
client = commands.Bot(intents = intents, command_prefix = '!')

@client.event
async def on_ready():
    print(f'{client.user} is ready!')

@client.event
async def on_member_join(member):
    guild = str(member.guild)
    name = member.mention
    msg = f"Hi {name}! Welcome to {guild}! My name is Brian, I'm a bot here. If you need anything let me know by pinging !help"
    await member.guild.get_channel(706419344070148147).send(msg)

@client.event    
async def on_message(message):
    channel = str(message.channel)
    if message.content == '!help':
        await message.channel.send('!help is currently not available')
    if channel == "testing-bots" and message.author != client.user:
        await message.channel.send('Hi my name is Brian!')

def create_audio_files(members):
    audio_files = []
    count = 0
    for member in members:
        if member.bot:
            continue
        audio_file = BytesIO()
        guild = str(member.guild)
        name = member.display_name
        msg = f'Hi {name}! Welcome to {guild}! My name\'s Brian. I am a bot here. If you need anything let me know.'
        tts = gTTS(msg, lang = 'en')
        tts.save(f'voice{count}.mp3')
        pcm = discord.FFmpegPCMAudio(f'voice{count}.mp3')
        audio_files.append(pcm)
    return audio_files

def cleanup(audio_files):
    for i in range(len(audio_files)):
        if os.path.exists(f'voice{i}.mp3'):
            os.remove(f'voice{i}.mp3')

def get_vc(member):
    guild = member.guild
    voice_client = None
    for vc in client.voice_clients:
        print(vc)
        if guild == vc.guild:
            voice_client = vc
    return voice_client

@client.command(name = 'invite')
async def orginvite(self, ctx):
    await ctx.send('hello Stanley')
    
@client.event
async def on_voice_state_update(member, before, after):
    voice_channel = after.channel
    voice_client = get_vc(member)
    if voice_channel and member != client.user and not voice_client:
        await voice_channel.connect()
        voice_client = get_vc(member)
    if voice_channel:
        audio_files = create_audio_files(voice_channel.members)
        if not discord.opus.is_loaded():
            print('Opus not loaded!')
            await voice_client.disconnect()
            return
        print('Voice connected!')
        for file in audio_files:
            voice_client.play(file)
            time.sleep(20)
        if not voice_client.is_playing():
            await voice_client.disconnect()
            voice_client = None
            cleanup(audio_files)
    
client.run(BOT_TOKEN)