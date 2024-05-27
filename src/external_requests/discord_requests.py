import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")


async def get_voice_channel_members(channel_id):
    guild = client.guilds[0]
    voice_channel = guild.get_channel(channel_id)
    members = [member.name for member in voice_channel.members]
    return members


async def get_guild_ids(client):
    return [guild.id for guild in client.guilds]


async def get_channel_ids(client, guild_id):
    guild = client.guilds[0]
    if guild is None:
        print(f"Guild with id {guild_id} not found")
        return []
    return [channel.id for channel in guild.channels]
