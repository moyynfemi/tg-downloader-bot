import os
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Make sure BOT_TOKEN exists
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# Create the bot application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Example /start command
async def start(update, context):
    await update.message.reply_text("Hey! I'm alive!")

app.add_handler(CommandHandler("start", start))

# Run the bot
app.run_polling()
