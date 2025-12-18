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
<<<<<<< HEAD
=======
from restrictions import setup_restrictions
>>>>>>> 0ed699c (Update SugarGlitter project)
from links import gmail_url, youtube_url, linkedIn_url, geeks_url
from mai import (
    start,
    help_cmd,
    song_mood_start,
    song_mood_receive,
<<<<<<< HEAD
=======
    song_cancel,
>>>>>>> 0ed699c (Update SugarGlitter project)
    unknown,
    unknown_text,
    ASK_MOOD,
)

load_dotenv()

<<<<<<< HEAD
if __name__ == "__main__":
    init_db()

=======
# Configure centralized logging early so all modules use the same configuration
from logging_config import configure_logging
configure_logging()

if __name__ == "__main__":
    init_db()

>>>>>>> 0ed699c (Update SugarGlitter project)
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("❌ BOT_TOKEN not found in environment! Check your .env file.")

    app = ApplicationBuilder().token(token).build()


<<<<<<< HEAD
    # Commands simple
=======

>>>>>>> 0ed699c (Update SugarGlitter project)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("gmail", gmail_url))
    app.add_handler(CommandHandler("youtube", youtube_url))
    app.add_handler(CommandHandler("linkedin", linkedIn_url))
    app.add_handler(CommandHandler("geeks", geeks_url))
    app.add_handler(CommandHandler("joke", random_joke))
    app.add_handler(CommandHandler("compliment", random_compliment))

<<<<<<< HEAD
    # Photo handler
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, analyze_photo))

    # /search cu argument
    app.add_handler(CommandHandler("search", search_cmd))

    # Conversation pentru /searchwords
=======
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, analyze_photo))

    app.add_handler(CommandHandler("search", search_cmd))

>>>>>>> 0ed699c (Update SugarGlitter project)
    search_conv = ConversationHandler(
        entry_points=[CommandHandler("searchwords", search_start)],
        states={
            ASK_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_receive_query)]
        },
        fallbacks=[CommandHandler("cancel", search_cancel)],
        allow_reentry=True,
    )
    app.add_handler(search_conv)
<<<<<<< HEAD
=======

    song_conv = ConversationHandler(
        entry_points=[CommandHandler("song", song_mood_start)],
        states={
            ASK_MOOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, song_mood_receive)]
        },
        fallbacks=[CommandHandler("cancel", song_cancel)],
        allow_reentry=True,
    )
    app.add_handler(song_conv)
>>>>>>> 0ed699c (Update SugarGlitter project)

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
<<<<<<< HEAD

    # Text necunoscut (atenție: cu handler-ul de mai sus, acesta s-ar putea să nu fie atins
    # pentru că index_message consumă deja TEXT & ~COMMAND, dar îl las exact ca în codul tău inițial)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))
=======
>>>>>>> 0ed699c (Update SugarGlitter project)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))
    # Enable moderation handlers and /rules command
    setup_restrictions(app)
    app.run_polling()
<<<<<<< HEAD
=======

>>>>>>> 0ed699c (Update SugarGlitter project)
