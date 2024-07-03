import discord


class DiscordClient:
    def __init__(self, token, guild_id):
        self.client = discord.Client(intents=discord.Intents.default())
        self.token = token
        self.guild_id = int(guild_id)
        self.setup_events()

    def setup_events(self):
        @self.client.event
        async def on_ready(self):
            print(f"{self.client.user.name} has connected to Discord!")

    async def start(self):
        await self.client.start(self.token)

    async def close(self):
        await self.client.close()

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
