import os
import discord
from discord.ext import commands
from discord import ChannelType
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

def create_audio_files(members):
    audio_files = []
    count = 0
    for member in members:
        if member.bot:
            continue
        audio_file = BytesIO()
        name_guild = get_name_guild(member)
        msg = f'Hi {name_guild[0]}! Welcome to {name_guild[1].name}! My name\'s Brian. I am a bot here. If you need anything let me know.'
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

def get_name_guild(member):
   return (member.display_name, member.guild) 

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)
    channel = message.channel
    if channel.type == ChannelType.private:
        username = message.content.split()[0]
        print(username)
        await channel.send('Invite has been sent. Check your GitHub or your email to join the organization! :)')

#keeps track of all twitch subs
twitch_subs = []

#sends dm to get the organization enrollment process started
@client.command(name = 'invite')
@commands.has_role('Owner')
async def orginvite(ctx):
    guild = ctx.guild
    new_twitch_subs = [] 
    for member in guild.members:
        for role in member.roles:
            if 'Owner' == role.name:
                if member not in twitch_subs:
                    new_twitch_subs.append(member)
                    break
    
    for twitch_sub in new_twitch_subs:
        await twitch_sub.create_dm()
        name_guild = get_name_guild(twitch_sub)
        msg = f'Hi {name_guild[0]}! I wanted to say thanks by inviting you to {name_guild[1].name}\'s GitHub organization where you can write code and be recognized on stream. What is your GitHub username?(Please respond with just the username)'
        await twitch_sub.dm_channel.send(msg) 
        #twitch_subs.append(twitch_sub)

    await ctx.send('Invite process has been started.')

    
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