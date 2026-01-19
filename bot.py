import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

# Get the bot token from Railway environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# Create the bot application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! I'm alive! Send /download <video_url> to download videos.")

# /download command
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Send a URL like this: /download <video_url>")
        return

    url = context.args[0]
    await update.message.reply_text(f"Downloading from: {url}")

    # yt-dlp options
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_text(f"Downloaded: {os.path.basename(filename)}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("download", download))

# Run the bot
app.run_polling()
