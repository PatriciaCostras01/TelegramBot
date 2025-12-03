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
├── main.py              # App entry point & handler registration
├── photo.py             # Image analysis using YOLOv8
├── search.py            # Message indexing, search, and SQLite logic
├── mai.py               # General commands: /start, /help, /song
├── links.py             # Quick-link commands
├── restrictions.py      # Text moderation rules and warnings
│
├── jokes.py             # Random jokes
├── compliments.py       # Random compliments
├── songs.py             # Mood normalization + song selection
│
├── index.db             # SQLite database (auto-generated)
└── .env                 # Telegram BOT_TOKEN


🚀 Installation & Setup
1. Install dependencies

pip install -r requirements.txt

2. Create a .env file

3. Run the bot

python main.py
