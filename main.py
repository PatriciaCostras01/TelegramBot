import os
from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from jokes import random_joke
from compliments import random_compliment

from photo import analyze_photo
from search import (
    init_db,
    ASK_QUERY,
    index_message,
    search_cmd,
    search_start,
    search_receive_query,
    search_cancel,
)
from restrictions import setup_restrictions
from links import gmail_url, youtube_url, linkedIn_url, geeks_url
from mai import (
    start,
    help_cmd,
    song_mood_start,
    song_mood_receive,
    song_cancel,
    cancel_cmd,
    unknown,
    unknown_text,
    ASK_MOOD,
)

load_dotenv()

# Configure centralized logging early so all modules use the same configuration
from logging_config import configure_logging
configure_logging()

if __name__ == "__main__":
    init_db()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("❌ BOT_TOKEN not found in environment! Check your .env file.")

    app = ApplicationBuilder().token(token).build()



    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("gmail", gmail_url))
    app.add_handler(CommandHandler("youtube", youtube_url))
    app.add_handler(CommandHandler("linkedin", linkedIn_url))
    app.add_handler(CommandHandler("geeks", geeks_url))
    app.add_handler(CommandHandler("joke", random_joke))
    app.add_handler(CommandHandler("compliment", random_compliment))

    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, analyze_photo))

    app.add_handler(CommandHandler("search", search_cmd))

    search_conv = ConversationHandler(
        entry_points=[CommandHandler("searchwords", search_start)],
        states={
            ASK_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_receive_query)]
        },
        fallbacks=[CommandHandler("cancel", search_cancel)],
        allow_reentry=True,
    )
    app.add_handler(search_conv)

    song_conv = ConversationHandler(
        entry_points=[CommandHandler("song", song_mood_start)],
        states={
            ASK_MOOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, song_mood_receive)]
        },
        fallbacks=[CommandHandler("cancel", song_cancel)],
        allow_reentry=True,
    )
    app.add_handler(song_conv)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, index_message))

    app.add_handler(CommandHandler("cancel", cancel_cmd))

    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))
    # Enable moderation handlers and /rules command
    setup_restrictions(app)
    app.run_polling()

