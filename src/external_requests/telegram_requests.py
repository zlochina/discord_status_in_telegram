from discord_requests import get_voice_channel_members
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ..constants import TELEGRAM_BOT_TOKEN, VOICE_CHANNEL_ID

application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! I'm a bot."
    )


async def voice_channel_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Replace with your desired guild and channel IDs
    members = await get_voice_channel_members(VOICE_CHANNEL_ID)
    member_list = ", ".join(members)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Members in the voice channel: {member_list}",
    )


async def send_message(chat_id: str, text: str):
    await application.bot.send_message(chat_id=chat_id, text=text)


# async def start_application():
#     # start_handler = CommandHandler("start", start)
#     voice_channel_handler = CommandHandler("voicechannel", voice_channel_members)
#     # application.add_handler(start_handler)
#     application.add_handler(voice_channel_handler)
#     application.run_polling()

if __name__ == "__main__":
    voice_channel_handler = CommandHandler("voicechannel", voice_channel_members)
    application.add_handler(voice_channel_handler)
    application.run_polling()
