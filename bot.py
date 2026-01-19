import os
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update, context):
    await update.message.reply_text("Hey! I'm alive!")

app.add_handler(CommandHandler("start", start))

app.run_polling()
