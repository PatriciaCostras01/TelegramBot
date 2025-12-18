🌸 SugarGlitter Telegram Bot

SugarGlitter is a playful, sparkly Telegram bot built with Python and python-telegram-bot.
She provides a mix of fun, utility, and AI-powered features:

🎀 Useful quick-link commands (YouTube, Gmail, LinkedIn, GeeksForGeeks)

💞 Random compliments and silly jokes

🎶 Mood-based song recommendations

🔎 Internal message search with SQLite indexing

🖼️ Photo analysis using YOLOv8

🛡️ Soft language moderation in private chats

📚 Automatic message storage in SQLite

All logic is neatly organized into separate modules for readability and maintainability.

📁 Project Structure

project/
│
├── main.py              # Application entry point + handler registration
├── photo.py             # Image analysis (YOLOv8 integration)
├── search.py            # Message indexing, search engine, and SQLite logic
├── mai.py               # General bot commands: /start, /help, /song
├── links.py             # Quick-link commands (/instagram, /github, etc.)
├── restrictions.py      # Text moderation rules & warning messages
│
├── jokes.py             # Random jokes generator
├── compliments.py       # Random compliments generator
├── songs.py             # Mood normalization + song recommendation logic
│
├── index.db             # SQLite database (auto-generated)
└── .env                 # Environment variables (Telegram BOT_TOKEN)


🚀 Installation & Setup
1. Install dependencies

pip install -r requirements.txt

2. Create a .env file

3. Run the bot

python main.py
