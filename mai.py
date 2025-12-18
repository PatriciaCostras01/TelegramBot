from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from songs import normalize_mood, pick_song_for_mood
import logging

_logger = logging.getLogger(__name__)
import os

ASK_MOOD = 2


async def song_mood_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _logger.debug("song_mood_start triggered by user %s", update.effective_user and update.effective_user.id)
    await update.message.reply_text(
        "🎧✨ How are you feeling today, sweet soul?\n"
        "You can say things like: `sad`, `happy`, `in love`, `angry`, `chill`… 💖",
        parse_mode="Markdown"
    )
    return ASK_MOOD


async def song_mood_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    _logger.debug("Received song mood input: %r from %s", text, update.effective_user and update.effective_user.id)
    mood = normalize_mood(text)
    _logger.debug("Normalized mood: %r", mood)
    # Temporary visible debug for troubleshooting in Telegram chat
    if os.getenv("DEBUG_TELEGRAM") == "1":
        await update.message.reply_text(f"DEBUG: received={text!r} normalized={mood!r}")

    if not mood:
        await update.message.reply_text(
            "🌸 SugarGlitter couldn’t quite feel your vibe yet.\n"
            "Try using moods like: *sad*, *love*, *party*, *chill* 💖",
            parse_mode="Markdown"
        )
        return ASK_MOOD

    song = pick_song_for_mood(mood)
    if not song:
        await update.message.reply_text(
            "✨ SugarGlitter doesn’t have songs for this exact mood yet, but she’s learning! 💖"
        )
        return ConversationHandler.END

    title, link = song

    mood_label = {
        "sad": "💔 Sad manele vibes detected…",
        "love": "💖 Love & romantic manele in the air…",
        "party": "🎉 Chef & party mode ON!",
        "chill": "🌙 Chill, nostalgic manele vibes…",
    }.get(mood, "✨ Mood detected…")

    await update.message.reply_text(
        f"{mood_label}\n\n"
        f"🎶 SugarGlitter picked this song for you:\n"
        f"*{title}*\n"
        f"{link}",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


async def song_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎶 The song selection was cancelled. If you want another tune, try /song again! 💖"
    )
    return ConversationHandler.END


async def cancel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌸 SugarGlitter is going to sleep now… "
        "If you want her back, run the bot again and use /start 💖"
    )

    _logger.warning("Global /cancel called – stopping application from chat %s", update.effective_chat.id)

    await context.application.stop()
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌸 Hiii! SugarGlitter just sprinkled into the chat! ✨💖\n"
        "Use /help to see all the magical things I can do! 🎀"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💖✨ *SugarGlitter’s Magical Command Menu* ✨💖\n\n"

        "🍬 /start – Wake up this sweet girl SugarGlitter and let the magic begin!\n"
        "🌸 /help – Show this adorable little guide\n"
        "🎀 /youtube – A sparkly doorway to YouTube\n"
        "💗 /linkedin – Your professional glitter profile\n"
        "💌 /gmail – Your shiny Gmail link\n"
        "📚 /geeks – A nerdy sprinkle from GeeksforGeeks\n"
        "💞 /compliment – SugarGlitter gives you a cute sparkly compliment!\n"
        "🤣 /joke – Get a silly little SugarGlitter-style joke\n"
        "🎶 /song – SugarGlitter picks a random song for your vibe\n\n"

        "🔎✨ *Search Spells:* ✨🔍\n"
        "💎 /search <term> – Instantly search messages (e.g. `/search grey car`)\n"
        "🌈 /searchwords – SugarGlitter asks what magical thing you want to search for\n"
        "🍭 /cancel – Cancel the current search enchantment\n\n"

        "🖼️💫 *Image Magic:* 💫🖼️\n"
        "Send SugarGlitter a photo and she’ll try her best to recognize what’s inside!\n"
        "✨ (people, pets, cars, objects… and everything sparkly & cute) ✨",
        parse_mode="Markdown"
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🍬 *'{update.message.text}'* isn’t in SugarGlitter’s candy jar of commands! "
        f"Try /help for something yummy! 💗",
        parse_mode="Markdown"
    )


async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🧁 Aww… *'{update.message.text}'* doesn’t make much sense to SugarGlitter. "
        f"Try something a bit clearer? 💗",
        parse_mode="Markdown"
    )
