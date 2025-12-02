import random

JOKES = [
    "✨ Why did the cookie cry? Because its mom was a wafer too long! 🍪😭",
    "💖 Why don’t eggs tell jokes? They’d crack each other up! 🥚😂",
    "🌸 What do you call a bear with no teeth? A gummy bear! 🧸🍬",
    "✨ Why was the computer cold? Because it forgot to close its Windows! 🖥️❄️",
    "🎀 What do you call fake spaghetti? An impasta! 🍝😄",
]

async def random_joke(update, context):
    joke = random.choice(JOKES)
    await update.message.reply_text(f"{joke}")
