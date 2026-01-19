from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yt_dlp
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("Downloading... ⏳")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await update.message.reply_video(open(file, "rb"))
                os.remove(file)
                break

    except:
        await update.message.reply_text("That link said no 💀")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
