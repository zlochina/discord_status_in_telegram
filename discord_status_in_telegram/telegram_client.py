import telegram

from .configuration import ConfigurationHolder


class TelegramClient:
    def __init__(self):
        ch = ConfigurationHolder()
        self.bot = telegram.Bot(token=ch.telegram.token)
        self.chat_id = ch.telegram.chat_id

    async def send_status(self, status):
        message = "Discord Voice Channels Status:\n\n"
        for channel in status:
            message += f"{channel['name']}:\n"
            if channel["members"]:
                message += ", ".join(channel["members"])
            else:
                message += "Empty"
            message += "\n\n"

        await self.bot.send_message(chat_id=self.chat_id, text=message)

    async def send_message(self, message):
        await self.bot.send_message(chat_id=self.chat_id, text=message)
