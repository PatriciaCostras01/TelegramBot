from telegram import Update
from telegram.ext import ContextTypes


async def gmail_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your gmail link here (not sharing mine)")


async def youtube_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Youtube Link => https://www.youtube.com/")


async def linkedIn_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "LinkedIn URL => https://www.linkedin.com/in/username/"
    )


async def geeks_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "GeeksforGeeks URL => https://www.geeksforgeeks.org/"
    )
