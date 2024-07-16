import time

import discord
import requests
from discord.ext import commands

from .configuration import ConfigurationHolder
from .logger_config import setup_logger
from .telegram_client import TelegramClient

logger = setup_logger(__name__)

API_ENDPOINT = "https://discord.com/api/v10"


class DiscordClient:
    def __init__(self, telegramClient: TelegramClient):
        logger.info("Initializing Discord Client")
        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True
        intents.message_content = True
        self.ch = ConfigurationHolder()
        self.client = commands.Bot(command_prefix="!", intents=intents)
        self.token = self.ch.discord.token
        self.guild_id = int(self.ch.discord.guild_id)
        self.telegramClient = telegramClient
        self.setup_events()

    def setup_events(self):
        logger.debug("Setting up Discord events")
        client = self.client

        @client.event
        async def on_ready():
            logger.info(f"{self.client.user.name} has connected to Discord!")

        @client.event
        async def on_voice_state_update(member, before, after):
            if before.channel != after.channel:
                logger.info(f"Voice state update: {member.name}.")
                message = None | str
                if after.channel is None:
                    message = (
                        f"{member.name} left the voice channel {before.channel.name}"
                    )
                else:
                    message = (
                        f"{member.name} joined the voice channel {after.channel.name}"
                    )

                # send message
                await self.telegramClient.send_message(message)

        @client.event
        async def on_message(message):
            logger.info(f"Message received at {message.channel}")
            message = f"""{message.author} sent message to {message.channel}:
{message.content}"""
            await self.telegramClient.send_message(message)

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

    def refresh_token(self):
        logger.info("Refreshing Discord token")
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.ch.discord.refresh_token,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(
                f"{API_ENDPOINT}/oauth2/token",
                data=data,
                headers=headers,
                auth=(self.ch.discord.client_id, self.ch.discord.client_secret),
            )
            response.raise_for_status()

            token_data = response.json()
            logger.debug(f"Retrieved response: {token_data}")

            # Update the token in the client
            self.token = token_data["access_token"]

            # Update the configuration
            self.ch.set("Discord", "token", self.token)
            self.ch.set("Discord", "refresh_token", token_data["refresh_token"])
            self.ch.set(
                "Discord",
                "expiration_timestamp",
                str(int(time.time()) + token_data["expires_in"]),
            )

            logger.info("Successfully refreshed Discord token")
        except requests.RequestException as e:
            logger.error(f"Retrieved failed response: {response.json()}")
            logger.error(f"Failed to refresh Discord token: {str(e)}")
            raise
