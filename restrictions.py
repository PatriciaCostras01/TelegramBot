import re
import logging
from enum import IntEnum

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

logger = logging.getLogger(__name__)


class Severity(IntEnum):
    OK = 0
    HIGH = 2

BAD_PATTERNS = [
    r"\b(fuck|shit|bitch|asshole)\b",
    r"\b(idiot|moron|stupid)\b",
]

BAD_REGEX = re.compile("|".join(BAD_PATTERNS), re.IGNORECASE)

SEND_WARNINGS = True


COMMUNITY_RULES = """
📜 *Community Rules (Private Chat)*:

1. Be respectful. No insults, hate speech or harassment. (She will cry otherwise!😢)
2. No offensive or toxic language. (Preety please!🙏)
3. Images and links are allowed. (only if they are sparkly and nice!✨)
4. This chat may warn you if your message contains not-so-sweet words.
"""


async def rules_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMMUNITY_RULES, parse_mode="Markdown")


def classify_text(text: str) -> Severity:
    if not text:
        return Severity.OK

    if BAD_REGEX.search(text):
        return Severity.HIGH
    return Severity.OK


async def moderate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    text = msg.text or ""

    if chat.type != "private":
        return

    severity = classify_text(text)
    if severity == Severity.OK:
        return

    if SEND_WARNINGS:
        await msg.reply_text("✨ Oopsie! SugarGlitter spotted a not-so-sweet word… let’s keep things sugar-friendly! 🍬")


def setup_restrictions(app: Application) -> None:
    app.add_handler(CommandHandler("rules", rules_cmd))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
            moderate_text,
        )
    )
