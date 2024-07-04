import asyncio
import configparser

from discord_client import DiscordClient
from logger_config import setup_logger
from telegram_client import TelegramClient

# Set up logger
logger = setup_logger(__name__)


def load_config():
    logger.info("Loading configuration from config.ini")
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


async def main():
    config = load_config()
    logger.info("Configuration loaded successfully")

    logger.info("Initializing Discord client")
    discord_client = DiscordClient(
        config["Discord"]["token"], config["Discord"]["guild_id"]
    )
    # logger.info("Initializing Telegram client")
    # telegram_client = TelegramClient(
    #     config["Telegram"]["token"], config["Telegram"]["chat_id"]
    # )
    logger.info("Starting Discord client")
    await discord_client.start()
    logger.info("Discord client started successfully")

    print(await discord_client.get_voice_channels_status())

    # while True:
    #     status = await discord_client.get_voice_channels_status()
    #     await telegram_client.send_status(status)
    #     await asyncio.sleep(int(config["General"]["update_interval"]))


def asyncmain():
    asyncio.run(main())


if __name__ == "__main__":
    asyncmain()
