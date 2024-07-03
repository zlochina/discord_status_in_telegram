import asyncio
import configparser

from discord_client import DiscordClient
from telegram_client import TelegramClient


def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


async def main():
    config = load_config()

    discord_client = DiscordClient(
        config["Discord"]["token"], config["Discord"]["guild_id"]
    )
    telegram_client = TelegramClient(
        config["Telegram"]["token"], config["Telegram"]["chat_id"]
    )

    while True:
        status = await discord_client.get_voice_channels_status()
        await telegram_client.send_status(status)
        await asyncio.sleep(int(config["General"]["update_interval"]))


if __name__ == "__main__":
    asyncio.run(main())
