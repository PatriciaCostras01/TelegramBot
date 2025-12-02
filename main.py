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
from links import gmail_url, youtube_url, linkedIn_url, geeks_url
from mai import (
    start,
    help_cmd,
    song_mood_start,
    song_mood_receive,
    unknown,
    unknown_text,
    ASK_MOOD,
)

load_dotenv()

if __name__ == "__main__":
    init_db()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("❌ BOT_TOKEN not found in environment! Check your .env file.")

    app = ApplicationBuilder().token(token).build()


    # Commands simple
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("gmail", gmail_url))
    app.add_handler(CommandHandler("youtube", youtube_url))
    app.add_handler(CommandHandler("linkedin", linkedIn_url))
    app.add_handler(CommandHandler("geeks", geeks_url))
    app.add_handler(CommandHandler("joke", random_joke))
    app.add_handler(CommandHandler("compliment", random_compliment))

    # Photo handler
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, analyze_photo))

    # /search cu argument
    app.add_handler(CommandHandler("search", search_cmd))

    # Conversation pentru /searchwords
    search_conv = ConversationHandler(
        entry_points=[CommandHandler("searchwords", search_start)],
        states={
            ASK_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_receive_query)]
        },
        fallbacks=[CommandHandler("cancel", search_cancel)],
    )
    app.add_handler(search_conv)

    # Conversation pentru /song
    song_conv = ConversationHandler(
        entry_points=[CommandHandler("song", song_mood_start)],
        states={
            ASK_MOOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, song_mood_receive)]
        },
        fallbacks=[CommandHandler("cancel", search_cancel)],
    )
    app.add_handler(song_conv)

    # Indexare mesaje text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, index_message))

    # Comenzi necunoscute
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Text necunoscut (atenție: cu handler-ul de mai sus, acesta s-ar putea să nu fie atins
    # pentru că index_message consumă deja TEXT & ~COMMAND, dar îl las exact ca în codul tău inițial)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))

    app.run_polling()
