import random

COMPLIMENTS = [
    "💖 SugarGlitter thinks your smile could light up a whole galaxy! ✨🌌",
    "🌸 You shine brighter than 10,000 sparkles on a pink sunset! 💕",
    "🎀 You're sweeter than strawberry icing on a magical cupcake! 🧁✨",
    "💗 Your presence feels like a warm pastel cloud hugging the world! ☁️💖",
    "✨ SugarGlitter says your energy is pure stardust and kindness! 🌟",
    "🌈 You’re the human version of a rainbow with extra glitter! ✨💞",
    "🍬 You’re cute, charming, and full of sweet magic! SugarGlitter *adores* it! 💖",
    "💫 You glow in ways SugarGlitter can’t even measure—absolutely enchanting! 💕",
    "🦋 Your vibe is soft, dreamy, and captivating… a whole aesthetic! ✨",
    "🌟 Your heart sparkles in the most beautiful way, lovely! 💗✨",
    "🥺 You’re the kind of person who makes everything feel a little more magical. 💖",
    "🧁 SugarGlitter is convinced you’re 90% sweetness and 10% stardust! ✨💕",
    "🌸 You bring cuteness into the universe just by existing! 💮💗",
]

async def random_compliment(update, context):
    compliment = random.choice(COMPLIMENTS)
    await update.message.reply_text(compliment)
