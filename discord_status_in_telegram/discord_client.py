import discord
from logger_config import setup_logger

logger = setup_logger(__name__)


class DiscordClient:
    def __init__(self, token, guild_id):
        logger.info("Initializing Discord Client")
        intents = discord.Intents.default()
        intents.members = True
        self.client = discord.Client(intents=intents)
        self.token = token
        self.guild_id = int(guild_id)
        self.setup_events()

    def setup_events(self):
        logger.debug("Setting up Discord events")

        @self.client.event
        async def on_ready(self):
            logger.info(f"{self.client.user.name} has connected to Discord!")

    async def start(self):
        logger.info("Starting Discord Client")
        await self.client.start(self.token)

    async def close(self):
        logger.info("Closing Discord Client")
        await self.client.close()

    async def get_voice_channels_status(self):
        logger.info("Getting voice channels status")
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
