import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp
import asyncio

# Get bot token from Railway environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! I'm alive! Send /download <video_url> to download videos."
    )

# /download command
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Send a URL like this: /download <video_url>")
        return

    url = context.args[0]
    await update.message.reply_text(f"Downloading from: {url}")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': '/tmp/%(title)s.%(ext)s',
    }

    try:
        # Run yt-dlp in a separate thread to avoid blocking async loop
        loop = asyncio.get_running_loop()
        filename = await loop.run_in_executor(None, lambda: download_video(url, ydl_opts))
        await update.message.reply_text(f"Downloaded: {os.path.basename(filename)}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def download_video(url, opts):
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def main():
    # Create application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))

    # Run the bot until stopped
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
