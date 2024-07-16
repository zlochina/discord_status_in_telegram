import argparse
import asyncio

from .discord_app import DiscordApp
from .discord_client import DiscordClient
from .logger_config import setup_logger
from .telegram_client import TelegramClient

# Set up logger
logger = setup_logger(__name__)


def init_app():
    logger.info("Running in initialization mode")
    discord_app = DiscordApp()
    discord_app.start_authorization_flow()


async def main():
    logger.info("Initializing Telegram client")
    telegram_client = TelegramClient()

    logger.info("Initializing Discord client")
    discord_client = DiscordClient(telegram_client)

    logger.info("Starting discord client...")
    await discord_client.start()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Discord Status in Telegram")
    parser.add_argument(
        "-i", "--init", action="store_true", help="Run in initialization mode"
    )
    return parser.parse_args()


def asyncmain():
    logger.info("Starting async main")
    asyncio.run(main())


if __name__ == "__main__":
    args = parse_arguments()
    logger.debug("Starting application")
    if args.init:
        init_app()
    else:
        asyncmain()
