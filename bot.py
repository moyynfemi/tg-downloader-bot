import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Example command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, world! 🚀")

async def main():
    # Build the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))

    # Run the bot until Ctrl+C
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
