import asyncio

from .discord_client import DiscordClient
from .logger_config import setup_logger
from .telegram_client import TelegramClient

# Set up logger
logger = setup_logger(__name__)


async def main():
    logger.info("Initializing Telegram client")
    telegram_client = TelegramClient()

    logger.info("Initializing Discord client")
    discord_client = DiscordClient(telegram_client)

    logger.info("Starting discord client...")
    await discord_client.start()


def asyncmain():
    logger.info("Starting async main")
    asyncio.run(main())


if __name__ == "__main__":
    logger.debug("Starting application")
    asyncmain()
