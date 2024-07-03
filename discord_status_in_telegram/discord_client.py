import discord


class DiscordClient:
    def __init__(self, token, guild_id):
        self.client = discord.Client(intents=discord.Intents.default())
        self.token = token
        self.guild_id = int(guild_id)

    async def get_voice_channels_status(self):
        await self.client.login(self.token)
        guild = self.client.get_guild(self.guild_id)

        status = []
        for channel in guild.voice_channels:
            status.append(
                {
                    "name": channel.name,
                    "members": [member.name for member in channel.members],
                }
            )

        await self.client.close()
        return status
