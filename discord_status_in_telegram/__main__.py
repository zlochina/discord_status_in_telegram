import argparse
import asyncio

from .configuration import ConfigurationHolder
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
    logger.info("Initializing Discord client")
    discord_client = DiscordClient()
    # logger.info("Initializing Telegram client")
    # telegram_client = TelegramClient(
    #     ch.telegram.token, ch.telegram.chat_id
    # )
    # discord_client.refresh_token()
    await discord_client.start()
    logger.info("Discord client started successfully")

    # debug sleep 5 seconds
    await asyncio.sleep(10)

    print(await discord_client.get_voice_channels_status())

    # while True:
    #     status = await discord_client.get_voice_channels_status()
    #     await telegram_client.send_status(status)
    #     await asyncio.sleep(int(ch.update_interval))


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
