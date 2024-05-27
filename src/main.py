import asyncio

import external_requests.telegram_requests as telegram_requests
from constants import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TOKEN
from external_requests.discord_requests import client


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel is None:
            await telegram_requests.send_message(
                TELEGRAM_CHAT_ID,
                f"{member.name} left the voice channel {before.channel.name}",
            )
        else:
            await telegram_requests.send_message(
                TELEGRAM_CHAT_ID,
                f"{member.name} joined the voice channel {after.channel.name}",
            )


async def start_bot():
    print("Starting discord bot")
    await client.start(TOKEN)


async def main():
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
